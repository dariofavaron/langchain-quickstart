import streamlit as st

import json
import pandas as pd

# import helper files to scrape Notion API
from GeneralFunctions.vector_metadata_creation import create_area_vector_with_extracted_data, create_project_vector_with_extracted_data, create_task_vector_with_extracted_data, create_new_note_vector_with_extracted_data
from GeneralFunctions.dataframe_creation import visualize_notion_db_properties, visualize_notion_database_row_object, visualize_retrieved_vectors

# import and define the input file md with the prompt ans import it as a json
from prompt.prompt import Prompts

# Assume NotionAPI class is defined elsewhere and imported here
from API.NotionAPI import NotionAPI
from API.OpenAiAPI import OpenAiAPI
from API.PineconeAPI import PineconeAPI

# Set page title and favicon.
st.set_page_config(page_title="Home", page_icon="🦜️🔗")
st.title('Notion Database Explorer')

st.markdown(
    """
    the goal of this app is to explore the notion database and create a knowledge graph

    """
)

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

if 'areas_dataframe' not in st.session_state:
    st.session_state.areas_dataframe = {}
if 'projects_dataframe' not in st.session_state:
    st.session_state.projects_dataframe = {}
if 'tasks_dataframe' not in st.session_state:
    st.session_state.tasks_dataframe = {}


st.session_state.only_areas = st.checkbox("Only Areas")
st.session_state.only_4 = st.checkbox("Only 4")

st.session_state.db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
st.session_state.db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
st.session_state.db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"
st.session_state.db_id_note_inbox = "50d49cabe62146689b61932004d5687c"

prompt = Prompts()


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

if st.button("Button 1.1 - Get Data from Notion and save them in a dataframe"):
    with st.spinner('retrieving notion'):
        try:
            #areas
            st.session_state.areas_dataframe = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_areas)
            #projects
            st.session_state.projects_dataframe = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_projects)
            #tasks
            st.session_state.tasks_dataframe = notionClass.query_database(0, st.session_state.only_4, st.session_state.db_id_tasks)

            st.json(st.session_state.areas_dataframe, expanded=False)
            st.json(st.session_state.projects_dataframe, expanded=False)
            st.json(st.session_state.tasks_dataframe, expanded=False)

            area_dataframe = pd.DataFrame(st.session_state.areas_dataframe["results"])

            st.dataframe(area_dataframe)

        except Exception as e:
            st.error (f"Error while extracting everything from Notion: {e}")

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

                #inbox_content = notionClass.query_database(1, st.session_state.only_4, st.session_state.db_id_note_inbox)

                #ovewrite during development
                inbox_content = notionClass.query_database(1, st.session_state.only_4, st.session_state.db_id_note_inbox)

                st.write("extracted data from note inbox: ")
                st.json(inbox_content, expanded=False)

                # Get first element of the inbox
                inbox_note_to_review = inbox_content["results"][0]
                #st.write("inbox_note_to_review: ")
                #st.json(inbox_note_to_review, expanded=False)

                note_inbox_id = inbox_note_to_review["id"]
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
                
                page_content = notionClass.get_page_content(st, note_inbox_id)
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