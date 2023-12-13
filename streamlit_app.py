import streamlit as st

import json
import pandas as pd

# import helper files to scrape Notion API
from GeneralFunctions.vector_metadata_creation import create_area_vector_with_extracted_data, create_project_vector_with_extracted_data, create_task_vector_with_extracted_data, create_new_note_vector_with_extracted_data
from GeneralFunctions.dataframe_creation import visualize_notion_db_properties, visualize_notion_database_row_object


# Assume NotionAPI class is defined elsewhere and imported here
from API.NotionAPI import NotionAPI  # Replace 'your_notion_api_module' with the actual module name
from API.OpenAiAPI import OpenAIEmbeddingsAPI, OpenAITextCompletionAPI  # Replace 'your_openai_api_module' with the actual module name
from API.PineconeAPI import PineconeAPI  # Replace 'your_pinecone_api_module' with the actual module name

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

db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"
db_id_note_inbox = "50d49cabe62146689b61932004d5687c"

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
            embeddingClass = OpenAIEmbeddingsAPI(st.session_state.openai_api_key)
            st.write("- OpenAI API connection established")
    except Exception as e:
        st.error(f"Failed to connect to OpenAI: {e}")
else:
    st.warning("OpenAI API key not provided.")

# Initialize Pinecone API if API key is provided
if st.session_state.pinecone_api_key:
    try:
        with st.spinner('inizializing index in Pinecone...'):
            pineconeClass = PineconeAPI(st.session_state.pinecone_api_key, st.session_state.pinecone_index, st.session_state.pinecone_project_id, st.session_state.pinecone_env)
            index_stats = pineconeClass.DescribeIndexStats()
            st.write(f"- Pinecone Index Stats: {(index_stats)}")
    
    except Exception as e:
        st.error(f"Failed to retrieve Pinecone index stats: {e}")
else:
    st.warning("Pinecone API key not provided. Please enter the API key to check index stats.")

# Toggle for "Only Areas"
only_areas = st.checkbox("Only Areas")
only_4 = st.checkbox("Only 4")


if st.button("Button 1 - Get Data from Notion "):
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
                areas_content = notionClass.query_database(0, only_4, db_id_areas)

                st.text(f"- Number of rows retrieved for areas: {len(areas_content['results'])}")
            except Exception as e:
                st.error (f"Area ready query notion: {e}")
        # Skip projects and tasks if "Only Areas" is checked
        if not only_areas:
            with st.spinner('Projects'):
                projects_content = notionClass.query_database(0, only_4, db_id_projects)
                st.text(f"- Number of rows retrieved for projects: {len(projects_content['results'])}")

            with st.spinner('Tasks'):
                tasks_content = notionClass.query_database(0, only_4, db_id_tasks)
                st.text(f"- Number of rows retrieved for tasks: {len(tasks_content['results'])}")

        # Open AI API - Embed each row with OpenAI embeddings
        st.subheader("Open API - embed each row with OpenAI embeddings")

        with st.spinner('Areas'):
            areas_vectors = []
            for result in areas_content["results"]:
                vector = create_area_vector_with_extracted_data(result, embeddingClass)
                areas_vectors.append(vector)
            st.text(f"- Number of rows embedded for areas: {len(areas_vectors)}")

        if not only_areas:
            with st.spinner('Projects'):
                projects_vectors = []
                for result in projects_content["results"]:
                    vector = create_project_vector_with_extracted_data(result, embeddingClass)
                    projects_vectors.append(vector)
                st.text(f"- Number of rows embedded for projects: {len(projects_vectors)}")

            with st.spinner('Tasks'):
                tasks_vectors = []
                for result in tasks_content["results"]:
                    vector = create_task_vector_with_extracted_data(result, embeddingClass)
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

        if not only_areas:
            with st.spinner('Projects'):
                try:
                    vectors_upserted = pineconeClass.upsert(projects_vectors, "projects")
                    st.text(f"- Number of rows upserted for projects: {(vectors_upserted)}")
                except Exception as e:
                    st.error(f"Failed to upsert vectors for projects: {e}")
            
        if not only_areas:
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


#inbox_note_to_review = {}
#page_content = ""

if st.button("Button 2 - Get one element from Note Inbox"):

# - Analyze one Note Inbox
#     - Streamlit UI - click button 2
#     - Notion API - Get one element of Note Inbox DB and show it on the screen
    
    try:
        # Notion API - Get Areas DB content
        st.subheader("Retrieve Inbox from Notion:")

        with st.spinner('retrieving inbox'):
            try:
                inbox_content = notionClass.query_database(1, only_4, db_id_note_inbox)

                st.write("extracted data from note inbox: ")
                st.json(inbox_content, expanded=False)

                # Get first element of the inbox
                inbox_note_to_review = inbox_content["results"][0]

                page_content = notionClass.get_page_content(inbox_note_to_review["id"])

                dataframe_to_visualize = visualize_notion_database_row_object(inbox_note_to_review)

                
                st.write("page_name: ")
                st.dataframe(dataframe_to_visualize)
                st.write("page_content: ")
                st.write(page_content)
                
                st.success("Extracted inbox note!")


                with st.spinner('Embedding the note inbox'):
                    st.json(inbox_note_to_review, expanded=False)
                    vector = create_new_note_vector_with_extracted_data(inbox_note_to_review, page_content, embeddingClass)

                    input_notes_vectors=[vector]
                    st.text(f"- Number of rows embedded for inbox notes: {len(input_notes_vectors)}")

                with st.spinner('Extracting relevant docs from Pinecone'):
                    
                    st.json(input_notes_vectors, expanded=False)

                    st.json(input_notes_vectors[0], expanded=False)

                    areas_response = pineconeClass.query(query_vector=input_notes_vectors[0]["values"], topK=10, namespace="areas")
                    projects_response = pineconeClass.query(input_notes_vectors[0]["values"], 10, "projects")
                    tasks_response = pineconeClass.query(input_notes_vectors[0]["values"], 10, "tasks")

                    st.write("areas_response: ")
                    st.json(areas_response, expanded=False)
                    st.write("projects_response: ")
                    st.json(projects_response, expanded=False)
                    st.write("tasks_response: ")
                    st.json(tasks_response, expanded=False)

                    st.success("Extracted relevant docs from Pinecone!")


            except Exception as e:
                st.error (f"Error: {e}")

    except ValueError as e:
        st.error(f"Value Error: {e}")
    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"General exception: {e}")


if st.button("Button 3 - Get relevant docs from Pinecone"):
# - Extract relevant docs from pinecone
#     - Streamlit UI - click button 3
#     - OpenAI API - transform into vectors the visualized Note Inbox,
#     - Pinecone API - extract from Pinecone DB the most relevant documents
#     - Streamlit - show on screen [note inbox]+[prompt]+[relevant docs]

    try:
        
        with st.spinner('Embedding the note inbox'):
            st.json(inbox_note_to_review, expanded=False)
            vector = create_new_note_vector_with_extracted_data(inbox_note_to_review, page_content, embeddingClass)
            input_notes_vectors=[vector]
            st.text(f"- Number of rows embedded for inbox notes: {len(input_notes_vectors)}")

        with st.spinner('Extracting relevant docs from Pinecone'):
            areas_response = pineconeClass.query(input_notes_vectors[0]["values"], 10, "areas")
            projects_response = pineconeClass.query(input_notes_vectors[0]["values"], 10, "projects")
            tasks_response = pineconeClass.query(input_notes_vectors[0]["values"], 10, "tasks")

            st.write("areas_response: ")
            st.json(areas_response, expanded=False)
            st.write("projects_response: ")
            st.json(projects_response, expanded=False)
            st.write("tasks_response: ")
            st.json(tasks_response, expanded=False)

            st.success("Extracted relevant docs from Pinecone!")
    
    except ValueError as e:
        st.error(f"Value Error: {e}")


# add space in the UI
st.text("")
st.text("")
st.text("")


if st.button("Get Areas structure"):
    #fetch_and_display_notion_structure(st.session_state.notion_api_key, db_id_areas)
    area_structure = notionClass.get_database_structure(db_id_areas)
    df_properties = visualize_notion_db_properties(area_structure)
    st.dataframe(df_properties)
