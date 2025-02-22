import streamlit as st

import json
import pandas as pd

# import helper files to scrape Notion API
from GeneralFunctions.vector_metadata_creation import create_area_vector_with_extracted_data, create_project_vector_with_extracted_data, create_task_vector_with_extracted_data, create_new_note_vector, create_full_task_vector
from GeneralFunctions.dataframe_creation import visualize_notion_db_properties, visualize_notion_database_row_object, visualize_retrieved_vectors
from GeneralFunctions.CreateTaskDataframe import create_task_table, create_project_table, create_task_row_properties, create_note_table

from ingest_notion import extract_dataframe_structure

# import and define the input file md with the prompt ans import it as a json
from prompt.prompt import Prompts

# Assume NotionAPI class is defined elsewhere and imported here
from API.NotionAPI import NotionAPI
from API.OpenAiAPI import OpenAiAPI
from API.PineconeAPI import PineconeAPI

def refresh_databases():
    """
    import notion databases
    creates dataframes
    embed them
    upsert tasks in pinecone
    """

    with st.spinner('retrieving notion'):
        try:
            #Retrieve Databases of areas, projects, tasks, and notes
            st.session_state.areas_json = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_areas)
            st.session_state.projects_json = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_projects)
            st.session_state.tasks_json = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_tasks)
            st.session_state.new_notes_json = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_note_inbox)
        except Exception as e:
            st.error (f"Error while retrieving notion: {e}")
    with st.spinner('creating dataframes'):
        try:
            #create Dataframes
            #create a dataframe with all the tasks
            #TASKS dataframe columns: "Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"
            st.session_state.tasks_dataframe = create_task_table(st,
                st.session_state.areas_json,
                st.session_state.projects_json,
                st.session_state.tasks_json
            )
                        
            #create a dataframe with all the projects
            #dataframes columns: "Project Name", "Area Related", "Area Type", "Project ID", "Area ID", "Project Description"
            st.session_state.projects_dataframe = create_project_table(st,
                st.session_state.areas_json,
                st.session_state.projects_json
            )

            st.json(st.session_state.new_notes_json, expanded=False)

            #create a dataframe with all the notes
            #dataframes columns: "Note Name", "Note URL", "Note Content", "Note Status" "Note ID"
            st.session_state.notes_dataframe = create_note_table(
                st,
                notionClass,
                st.session_state.new_notes_json,
                only_one_note=False
            )
        except Exception as e:
            st.error (f"Error while creating dataframes: {e}")

    with st.spinner('embedding tasks'):
        try:
            #embed all the tasks from the dataframe
            full_tasks_vectors = create_full_task_vector(st.session_state.tasks_dataframe, openAiClass)
            
            #deleting all vectors in the namespace
            response = pineconeClass.delete_all("fulltasks")

            #upload the tasks to pinecone
            vectors_upserted = pineconeClass.upsert(full_tasks_vectors, "fulltasks")
            st.write(f"- Number of tasks upserted: {(vectors_upserted)}")
        except Exception as e:
            st.error (f"Error while creating embedding tasks: {e}")


def new_task_draft():
    """
    Get Data from Notion and save them in a dataframe. one line per Task, 
    upsert in Pinecone, 
    extract the notes and save them in a dataframe,
    extract the projects and save them in a dataframe,
    For each note of the dataframe,
        embed it in OpenAI,
        extract from Pinecone the most relevant docs
        send to open AI function 
            the prompt and examples (new task dataframe)
            the note and the relevant docs
            the full list of projects with related areas and type, as a dataframe
        extract the answer as a dataframe
        load the dataframe to Notion as a new task
    """

    with st.spinner('embedding notes'):
        try:

            #extract a single note from the note dataframe
            #st.session_state.note_in_analysis = st.session_state.notes_dataframe.iloc[0]

            #extract the first note with status "New" from the note dataframe
            st.session_state.note_in_analysis = st.session_state.notes_dataframe[st.session_state.notes_dataframe["Note Status"] == "New"].iloc[0]

            #create new note inbox vector and embed it
            note_inbox_vector = [
                create_new_note_vector(
                    st.session_state.note_in_analysis["Note ID"],
                    st.session_state.note_in_analysis["Note Name"],
                    st.session_state.note_in_analysis["Note URL"],
                    st.session_state.note_in_analysis["Note Content"],
                    openAiClass
                )
            ]

            #extract the relevant docs of the note from Pinecone
            relevant_docs = pineconeClass.query(note_inbox_vector[0]["values"], topK=20, namespace="fulltasks", include_metadata=True)

            st.write("Extracted relevant docs from Pinecone")
        except Exception as e:
            st.error (f"Error while embedding notes inbox: {e}")

    with st.spinner('Extract relevant docs and create prompt for OpenAI'):
        try:

            #create a dictonary with the relevant docs
            relevant_tasks = []
            for doc in relevant_docs["matches"]:
                relevant_tasks.append([
                    doc["metadata"]["Task Name"] if "Task Name" in doc["metadata"] else None,
                    doc["metadata"]["Project Related"] if "Project Related" in doc["metadata"] else None,
                    doc["metadata"]["Area Related"] if "Area Related" in doc["metadata"] else None,
                    doc["metadata"]["Area Type"] if "Area Type" in doc["metadata"] else None,
                    doc["metadata"]["Task ID"] if "Task ID" in doc["metadata"] else None,
                    doc["metadata"]["Project ID"] if "Project ID" in doc["metadata"] else None,
                    doc["metadata"]["Area ID"] if "Area ID" in doc["metadata"] else None,
                    doc["metadata"]["Task Description"] if "Task Description" in doc["metadata"] else None
                ])
            
            #relevant_tasks_df = pd.DataFrame(relevant_tasks, columns=["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"])
            #st.write("relevant docs dataframe: ")
            #st.dataframe(relevant_tasks_df)

            #create a dictonary with all the projects
            # dataframes columns: "Project Name", "Area Related", "Area Type", "Project ID", "Area ID", "Project Description"
            all_projects = []
            for _,doc in st.session_state.projects_dataframe.iterrows():
                all_projects.append([
                    doc["Project Name"] if "Project Name" in doc else None,
                    doc["Area Related"] if "Area Related" in doc else None,
                    doc["Area Type"] if "Area Type" in doc else None,
                    doc["Project ID"] if "Project ID" in doc else None,
                    doc["Area ID"] if "Area ID" in doc else None,
                    doc["Project Description"] if "Project Description" in doc else None
                ])

            #prepare the message
            #the prompt and examples (new task dataframe)
            messages = []
            messages.append(prompt.task_extraction_from_note_inbox_system)

            # note, relevant docs and projects
            messages.append({
                "role": "user",
                "content":
                    f"""
All Projects for context: columns: ["Project Name", "Area Related", "Area Type", "Project ID", "Area ID", "Project Description"] {all_projects}
            """})

            messages.append(prompt.task_extraction_from_note_inbox_example_request)
            messages.append(prompt.task_extraction_from_note_inbox_example_assistant)
            messages.append(prompt.task_extraction_from_note_inbox_example_request_2)
            messages.append(prompt.task_extraction_from_note_inbox_example_assistant_2)

            messages.append({
                "role": "user",
                "content": 
                    f"""
Note Name: {st.session_state.note_in_analysis["Note Name"]}\n
Note URL: {st.session_state.note_in_analysis["Note URL"]}\n
Note Content: {st.session_state.note_in_analysis["Note Content"]}\n
Relevant tasks: columns:["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"] {relevant_tasks}
"""})

            st.write(" messages: ")
            st.json(messages, expanded=False)

        except Exception as e:
            st.error (f"Error while Extract relevant docs and create prompt for OpenAI: {e}")

    with st.spinner('Send to OpenAI'):
        try:

            #send to open AI
            response = openAiClass.generate_text_completion(
                #model="gpt-4",
                model="gpt-3.5-turbo-1106",
                messages=messages,
                max_tokens=400,
                temperature=0.5
            )

            st.write("response from openAi completition:")
            st.json(response, expanded=False)

            st.session_state.new_task_draft = json.loads(response["choices"][0]["message"]["content"])

        except Exception as e:
            st.error (f"Error while sending to OpenAI: {e}")


# Set page title and favicon.
st.set_page_config(page_title="Home", page_icon="🦜️🔗")
st.title('Notion Database Explorer')

# Initialize session state variables and API classes
#def init_session():
# Initialize session state variables
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
if 'pinecone_api_key' not in st.session_state:
    st.session_state.pinecone_api_key = ""
if 'pinecone_env' not in st.session_state:
    st.session_state.pinecone_env = ""
if 'pinecone_project_id' not in st.session_state:
    st.session_state.pinecone_project_id = ""
if 'pinecone_index' not in st.session_state:
    st.session_state.pinecone_index = ""
if 'notion_api_key' not in st.session_state:
    st.session_state.notion_api_key = ""

#get secret keys
with st.sidebar:
    # Get API keys
    all_keys_str = st.text_input("All Keys in json format", type="password")

    if all_keys_str:
        all_keys = json.loads(all_keys_str)
        st.session_state.openai_api_key = all_keys['OPENAI_API_KEY']
        st.session_state.pinecone_api_key = all_keys['PINECONE_API_KEY']
        st.session_state.pinecone_env = all_keys['PINECONE_ENV']
        st.session_state.pinecone_index = all_keys['PINECONE_INDEX_NAME']
        st.session_state.pinecone_project_id = all_keys['PINECONE_PROJECT_ID']
        st.session_state.notion_api_key = all_keys['NOTION_API_KEY']

#initailize Notion class
if st.session_state.notion_api_key:
    try:
        with st.spinner('Initializing connection...'):
            notionClass = NotionAPI(st.session_state.notion_api_key)
            st.write("- Notion API connection established")
    except Exception as e:
        st.error(f"Failed to connect to Notion: {e}")
else:
    st.warning("Notion API key not provided.")

#Initialize OpenAI API if API key is provided
if st.session_state.openai_api_key:
    try:
        with st.spinner('Initializing Embedding data with OpenAI...'):
            openAiClass = OpenAiAPI(st.session_state.openai_api_key)
            st.write("- OpenAI API connection established")
    except Exception as e:
        st.error(f"Failed to connect to OpenAI: {e}")
else:
    st.warning("OpenAI API key not provided.")

# Initialize Pinecone API if API key is provided
if st.session_state.pinecone_api_key:
    try:
        with st.spinner('inizializing index in Pinecone...'):
            pineconeClass = PineconeAPI(
                st.session_state.pinecone_api_key,
                st.session_state.pinecone_index,
                st.session_state.pinecone_project_id,
                st.session_state.pinecone_env
                )
            index_stats = pineconeClass.DescribeIndexStats()
            st.write(f"- Pinecone Index Stats: {(index_stats)}")
    
    except Exception as e:
        st.error(f"Failed to retrieve Pinecone index stats: {e}")
else:
    st.warning("Pinecone API key not provided. Please enter the API key to check index stats.")


# Global Variables

if 'only_areas' not in st.session_state:
    st.session_state.only_areas = ""
if 'only_4' not in st.session_state:
    st.session_state.only_4 = ""
if 'db_id_areas' not in st.session_state:
    st.session_state.db_id_areas = ""
if 'db_id_projects' not in st.session_state:
    st.session_state.db_id_projects = ""
if 'db_id_tasks' not in st.session_state:
    st.session_state.db_id_tasks = ""
if 'db_id_note_inbox' not in st.session_state:
    st.session_state.db_id_note_inbox = ""
if 'note_inbox_extracted' not in st.session_state:
    st.session_state.note_inbox_extracted = {}
if 'first_prompt' not in st.session_state:
    st.session_state.first_prompt = []

if 'areas_json' not in st.session_state:
    st.session_state.areas_json = {}
if 'projects_json' not in st.session_state:
    st.session_state.projects_json = {}
if 'tasks_json' not in st.session_state:
    st.session_state.tasks_json = {}
if 'new_notes_json' not in st.session_state:
    st.session_state.new_notes_json = {}
if 'tasks_dataframe' not in st.session_state:
    st.session_state.tasks_dataframe = {}
if 'projects_dataframe' not in st.session_state:
    st.session_state.projects_dataframe = {}
if 'new_task_draft' not in st.session_state:
    st.session_state.new_task_draft = {}
if 'note_in_analysis' not in st.session_state:
    st.session_state.note_in_analysis = {}


st.session_state.only_areas = st.checkbox("Only Areas")
st.session_state.only_4 = st.checkbox("Only 4")

st.session_state.db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
st.session_state.db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
st.session_state.db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"
st.session_state.db_id_note_inbox = "50d49cabe62146689b61932004d5687c"



#every time that there is no note inbox imported, start the script of the button "Create a new task draft from a note in the inbox"
st.session_state.note_in_analysis = {}



prompt = Prompts()

#here we should always retrieve first the databases from notion and create the dataframes
if st.button("Retrieve databases from Notion and create the dataframes"):
    refresh_databases()

#then we can analyze one note at the time without the need to retrieve the databases every time

if st.button(" Create a new task draft from a note in the inbox "):
#if st.session_state.note_in_analysis.get("Note Name") is None and st.session_state.note_in_analysis.get("Note URL") is None and st.session_state.note_in_analysis.get("Note Content") is None:
    new_task_draft()







# Visualize the draft and the note inbox

try:
    draftColumn1, draftColumn2 = st.columns(2)

    # Define a function to safely convert values to strings
    def safe_str(value):
        return str(value) if value is not None else "N/A"
    
    draftColumn1.subheader("Note Inbox: ")
    # Safely get and display values for Note Inbox
    note_name = safe_str(st.session_state.note_in_analysis.get("Note Name"))
    note_url = safe_str(st.session_state.note_in_analysis.get("Note URL"))
    note_content = safe_str(st.session_state.note_in_analysis.get("Note Content"))

    draftColumn1.markdown(f"NOTE NAME: {note_name}")
    draftColumn1.markdown(f"NOTE URL: {note_url}")
    draftColumn1.markdown(f"NOTE CONTENT: {note_content}")
    draftColumn2.subheader("TASK DRAFT: ")
    if len(st.session_state.new_task_draft) != 0:

        draftColumn2.json(st.session_state.new_task_draft, expanded=False)

        # Use a helper function to safely get and display values
        def safe_text(column, key, label):
            value = st.session_state.new_task_draft.get(key)
            if value is not None:
                column.markdown(f"{label}: {value}")
            else:
                column.markdown(f"{label}: N/A")

        safe_text(draftColumn2, "task_name", "TASK NAME")
        safe_text(draftColumn2, "related_project_name", "RELATED PROJECT NAME")
        safe_text(draftColumn2, "related_project_id", "RELATED PROJECT ID")
        safe_text(draftColumn2, "related_area_name", "RELATED AREA NAME")
        safe_text(draftColumn2, "task_description", "TASK DESCRIPTION")
        safe_text(draftColumn2, "duplication_check", "DUPLICATION CHECK")
        safe_text(draftColumn2, "project_selection_results", "PROJECT SELECTION RESULTS")
        safe_text(draftColumn2, "Suggestions", "SUGGESTIONS")
        safe_text(draftColumn2, "Insights", "INSIGHTS")

except Exception as e:
    st.error(f"Error printing the draft: {e}")



if st.button("Accept and load the task to notion"):
    with st.spinner('Uploading a new task'):
        try:
            task_name = st.session_state.new_task_draft["task_name"]
            related_project_id = st.session_state.new_task_draft["related_project_id"]
            task_description = st.session_state.new_task_draft["task_description"]

            #load the dataframe to Notion as a new task
            response = notionClass.create_page(
                st.session_state.db_id_tasks,
                create_task_row_properties(
                    task_name = task_name,
                    related_project_id = related_project_id,
                    description = task_description,
                    status = "Ai Generated"
                ),
                icon="https://www.notion.so/icons/checkmark_gray.svg"
            )

            st.write("response from notion create_page: ")
            st.json(response, expanded=False)

            #update the note inbox
            response = notionClass.update_page(
                st.session_state.note_in_analysis["Note ID"],
                {
                    "Task Status": {
                        "status": {
                            "name": "Imported"
                        }
                    }
                }
            )
            st.write("response from notion update_page: ")
            st.json(response, expanded=False)


            st.success("uploaded task to with notion")
        except Exception as e:
            st.error (f"Error while loading new task to Notion: {e}")

#add the management of the note to analyze with a button to discard the note input and set it with Status "Deleted";
if st.button("Discard the note input and set it with Status 'Deleted'"):
    with st.spinner('Discarding the note input and set it with Status "Deleted"'):
        try:
            response = notionClass.update_page(
                st.session_state.note_in_analysis["Note ID"],
                {
                    "Task Status": {
                        "status": {
                            "name": "Deleted"
                        }
                    }
                }
            )
            st.write("response from notion update_page: ")
            st.json(response, expanded=False)
            st.session_state.note_in_analysis = {}
            st.success("Note discarded")
        except Exception as e:
            st.error (f"Error while discarding the note: {e}")

#button to reftresh the note inbox and task draft
if st.button("Refresh the note inbox and task draft"):
    with st.spinner('Refreshing the note inbox and task draft'):
        try:
            st.session_state.note_in_analysis = {}
            st.success("Note inbox and task draft refreshed")
        except Exception as e:
            st.error (f"Error while refreshing the note inbox and task draft: {e}")

# add space in the UI
st.text("")
st.text("")
st.text("")

if st.button("Button 1 - Get Data from Notion, embed it and store it on Pinecone "):
    '''
    First step: Get Data from Notion
    - Streamlit UI - click button 1
    - Notion API - Get Tasks, Project, Areas, and Knowledge DB content
    - Open API - embed each row with OpenAI embeddings
    - Pinecone API - Store it in a Pinecone DB
    '''
    try:
        # Notion API - Get Areas DB content
        st.subheader("Retrieve data from Notion:")

        with st.spinner('Areas'):
            try:
                areas_content = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_areas)

                st.text(f"- Number of rows retrieved for areas: {len(areas_content['results'])}")
            except Exception as e:
                st.error (f"Area ready query notion: {e}")
        # Skip projects and tasks if "Only Areas" is checked
        if not st.session_state.only_areas:
            with st.spinner('Projects'):
                projects_content = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_projects)
                st.text(f"- Number of rows retrieved for projects: {len(projects_content['results'])}")

            with st.spinner('Tasks'):
                tasks_content = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_tasks)
                st.text(f"- Number of rows retrieved for tasks: {len(tasks_content['results'])}")

        # Open AI API - Embed each row with OpenAI embeddings
        st.subheader("Open API - embed each row with OpenAI embeddings")

        with st.spinner('Areas'):
            areas_vectors = []
            for result in areas_content["results"]:
                vector = create_area_vector_with_extracted_data(result, openAiClass)
                areas_vectors.append(vector)
            st.text(f"- Number of rows embedded for areas: {len(areas_vectors)}")

        if not st.session_state.only_areas:
            with st.spinner('Projects'):
                projects_vectors = []
                for result in projects_content["results"]:
                    vector = create_project_vector_with_extracted_data(result, openAiClass)
                    projects_vectors.append(vector)
                st.text(f"- Number of rows embedded for projects: {len(projects_vectors)}")

            with st.spinner('Tasks'):
                tasks_vectors = []
                for result in tasks_content["results"]:
                    vector = create_task_vector_with_extracted_data(result, openAiClass)
                    tasks_vectors.append(vector)
                st.text(f"- Number of rows embedded for tasks: {len(tasks_vectors)}")

        # Pinecone API - Store it in a Pinecone DB
        st.subheader("Pinecone API - Store it in a Pinecone DB")

        # Upsert AREAS vectors into Pinecone index
        with st.spinner('Areas'):
            try:
                vectors_upserted = pineconeClass.upsert(areas_vectors, "areas")
                st.text(f"- Number of rows upserted for areas: {(vectors_upserted)}")

            except Exception as e:
                st.error(f"Failed to upsert vectors for areas: {e}")

        if not st.session_state.only_areas:
            with st.spinner('Projects'):
                try:
                    vectors_upserted = pineconeClass.upsert(projects_vectors, "projects")
                    st.text(f"- Number of rows upserted for projects: {(vectors_upserted)}")
                except Exception as e:
                    st.error(f"Failed to upsert vectors for projects: {e}")
            
        if not st.session_state.only_areas:
            with st.spinner('Tasks'):
                try:
                    vectors_upserted = pineconeClass.upsert(tasks_vectors, "tasks")
                    st.text(f"- Number of rows upserted for tasks: {(vectors_upserted)}")
                except Exception as e:
                    st.error(f"Failed to upsert vectors for tasks: {e}")

        st.success("Data from Notion extracted, embedded with OpenAI, and uploaded to Pinecone successfully!")
    except ValueError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"Error details: {e}")
if st.button("Button 2 - Get one element from Note Inbox, embed it, and extract relevant docs from Pinecone"):

# - Analyze one Note Inbox
#     - Streamlit UI - click button 2
#     - Notion API - Get one element of Note Inbox DB and show it on the screen
#     - Pinecone API - extract from Pinecone DB the most relevant documents
    
    try:
        # Notion API - Get Areas DB content
        st.subheader("Retrieve Inbox from Notion:")

        with st.spinner('retrieving inbox'):
            try:

                #ovewrite during development
                inbox_content = notionClass.query_database(1, st.session_state.only_4, st.session_state.db_id_note_inbox)

                st.write("extracted data from note inbox: ")
                st.json(inbox_content, expanded=False)

                # Get first element of the inbox
                inbox_note_to_review = inbox_content["results"][0]
                #st.write("inbox_note_to_review: ")
                #st.json(inbox_note_to_review, expanded=False)

                note_inbox_object = inbox_note_to_review["object"]

                if len(inbox_note_to_review["properties"]["Name"]["title"]) == 0 :
                    page_name = None
                else:
                    page_name = inbox_note_to_review["properties"]["Name"]["title"][0]["text"]["content"]

                #st.write("page_name: ")
                #st.text(page_name)
                
                if len(inbox_note_to_review["properties"]["URL"]) == 0 :
                    page_properties_url = ""
                else:
                    page_properties_url = inbox_note_to_review["properties"]["URL"]["url"]
                
                #st.write("page_properties_url: ")
                #st.text(page_properties_url)
                
                page_content = notionClass.get_page_content(st, inbox_content["results"][0]["id"])
                #st.write("page_content: ")
                #st.text(page_content)
                
                dataframe_to_visualize = visualize_notion_database_row_object(page_name, page_properties_url, page_content)

                #st.write("note_inbox_object: ")
                #st.dataframe(dataframe_to_visualize)
                
                st.success("Extracted inbox note!")
            except Exception as e:
                st.error (f"Error - retrieving inbox: {e}")

            try:
                with st.spinner('Embedding the note inbox'):
                    #st.json(inbox_note_to_review, expanded=False)
                    vector = create_new_note_vector_with_extracted_data(note_inbox_id, note_inbox_object, page_name, page_properties_url, page_content, openAiClass)

                    input_notes_vectors=[vector]
                    #st.text(f"- Number of rows embedded for inbox notes: {len(input_notes_vectors)}")

                with st.spinner('Extracting relevant docs from Pinecone'):
                    
                    areas_response = pineconeClass.query(query_vector=input_notes_vectors[0]["values"], topK=20, namespace="areas", include_metadata=True)
                    projects_response = pineconeClass.query(input_notes_vectors[0]["values"], topK=20, namespace="projects", include_metadata=True)
                    tasks_response = pineconeClass.query(input_notes_vectors[0]["values"], topK=20, namespace="tasks", include_metadata=True)

                    #st.write("areas_response: ")
                    areas_retrieved_df = visualize_retrieved_vectors(areas_response)
                    #st.dataframe(areas_retrieved_df)
                    #st.write("projects_response: ")
                    projects_retrieved_df = visualize_retrieved_vectors(projects_response)
                    #st.dataframe(projects_retrieved_df)
                    #st.write("tasks_response: ")
                    tasks_retrieved_df = visualize_retrieved_vectors(tasks_response)
                    #st.dataframe(tasks_retrieved_df)

                    st.success("Extracted relevant docs from Pinecone!")
            except Exception as e:
                st.error (f"Error - Embedding the note inbox: {e}")


            st.session_state.note_inbox_extracted = {
                "note_name": page_name,
                "note_url": page_properties_url,
                "note_content": page_content,
                "areas_related": areas_retrieved_df.to_json(),
                "projects_related": projects_retrieved_df.to_json(),
                "tasks_related": tasks_retrieved_df.to_json()
            }

            st.session_state.task_extraction_from_note_inbox = prompt.task_extraction_from_note_inbox

            # RESULT OF BUTTON 2

            # st.subheader("Prompt system: ")
            # st.markdown(st.session_state.first_prompt[0]["content"])
            # st.subheader("Example user: ")
            # st.markdown(st.session_state.first_prompt[1]["content"])
            # st.subheader("Example assistant: ")
            # st.markdown(st.session_state.first_prompt[2]["content"])
            st.subheader("Note name: ")
            st.write(st.session_state.note_inbox_extracted["note_name"])
            st.subheader("Note url: ")
            st.write(st.session_state.note_inbox_extracted["note_url"])
            st.subheader("Note content: ")
            st.write(st.session_state.note_inbox_extracted["note_content"])
            
            st.subheader("Relevant docs: ")
            st.json(st.session_state.note_inbox_extracted["areas_related"], expanded=False)
            st.json(st.session_state.note_inbox_extracted["projects_related"], expanded=False)
            st.json(st.session_state.note_inbox_extracted["tasks_related"], expanded=False)

    except ValueError as e:
        st.error(f"Value Error: {e}")
    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"General exception - Button 2: {e}")
if st.button("Button 3 - send prompt to OpenAI and visualize it on the screen"):

    st.subheader("send prompt to OpenAI and visualize it on the screen")

    try:
        with st.spinner('*sending data to OpenAI*'):

            messages=st.session_state.task_extraction_from_note_inbox

            # convert to string note_inbox_extracted
            note_inbox_summary = f"""
                Note Name: {st.session_state.note_inbox_extracted["note_name"]}\n
                Note URL: {st.session_state.note_inbox_extracted["note_url"]}\n
                Note Content: {st.session_state.note_inbox_extracted["note_content"]}\n
                Already existing areas: {st.session_state.note_inbox_extracted["areas_related"]}\n
                Already existing Projects: {st.session_state.note_inbox_extracted["projects_related"]}\n
                Already existing Tasks: {st.session_state.note_inbox_extracted["tasks_related"]}
            """

            messages.append({"role": "user", "content": note_inbox_summary})

            st.write(" messages: ")
            st.json(messages, expanded=False)
            
            response = openAiClass.generate_text_completion(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                max_tokens=400,
                temperature=0
            )
            st.write("response from openAi completition:")
            st.json(response, expanded=False)
            st.success("communicated correctly with openai")

            st.markdown(response["choices"][0]["message"]["content"])



            # Streamlit UI - Confirmation and Denial Buttons
            confirmation = st.button('Confirm Task')
            denial = st.button('Deny Task')

            # Notion API Integration - Update on Confirmation
            if confirmation:
                try:
                    # parse the answer to a format for notion
                    # Extract the chat content
                    chat_content = response["choices"][0]["message"]["content"]

                    # Prepare the prompt for GPT to parse the response
                    parse_prompt = f"Parse the following information into structured data for Notion:\n\n{chat_content}\n\nThe properties are Name, Areas, Projects, Description, Status. Provide the information in a structured format suitable for updating a Notion database."



                    st.success("Update successful in Notion.")
                except Exception as e:
                    st.error(f"Update failed in Notion: {e}")

    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"General exception Button 3: {e}")



# add space in the UI
st.text("")
st.text("")
st.text("")


if st.button("Get Areas structure"):
    #fetch_and_display_notion_structure(st.session_state.notion_api_key, st.session_state.db_id_areas)
    area_structure = notionClass.get_database_structure(st.session_state.db_id_areas)
    df_properties = visualize_notion_db_properties(area_structure)
    st.dataframe(df_properties)

if st.button("Get Tasks structure"):
    #fetch_and_display_notion_structure(st.session_state.notion_api_key, st.session_state.db_id_areas)
    task_structure = notionClass.get_database_structure(st.session_state.db_id_tasks)
    df_properties = visualize_notion_db_properties(task_structure)
    st.dataframe(df_properties)

if st.button("extract one task"):
    single_task = notionClass.query_database(1, st.session_state.only_4, st.session_state.db_id_tasks)

    st.write("extracted data from task: ")
    st.json(single_task, expanded=False)

if st.button("upload a new task"):
    
    try:
        with st.spinner('uploading a new task'):

            new_task_properties = create_task_row_properties(
                "This is a test task uploaded from streamlit",
                "a2476530-b182-4c9b-b9ca-356b0b7196d8",
                "test test",
                "Ai Generated"
            )

            response = notionClass.create_page(st.session_state.db_id_tasks, new_task_properties, icon="https://www.notion.so/icons/checkmark_gray.svg")
            st.write("response from notion:")
            st.json(response, expanded=False)
            st.success("communicated correctly with notion")
    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"General exception - upload a new task: {e}")

if st.button("delete all vector in a namespace"):
    try:
        with st.spinner('deleting all vectors in a namespace'):
            response = pineconeClass.delete_all("fulltasks")
            st.write("response from pinecone:")
            st.json(response, expanded=False)
            st.success("communicated correctly with pinecone")
    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"General exception - delete all vector in a namespace: {e}")

if st.button("Notion database structure agnostic extraction"):
    structure_json = notionClass.get_database_structure(st.session_state.db_id_tasks)
    dataframe_structure = extract_dataframe_structure(structure_json)
    st.write("structure_json: ")
    st.json(structure_json, expanded=False)
    st.write("dataframe_structure: ")
    st.dataframe(dataframe_structure)
