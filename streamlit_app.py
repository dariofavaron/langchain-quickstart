import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import BaseLLM

import requests

# import helper files to scrape Notion API
from helper_files import get_all_pages, get_page, get_page_content
from notion_functions import fetch_and_display_notion_structure
from GeneralFunctions.vector_management import create_area_vector_with_extracted_data, create_project_vector_with_extracted_data, create_task_vector_with_extracted_data

# Assume NotionAPI class is defined elsewhere and imported here
from API.NotionAPI import NotionAPI  # Replace 'your_notion_api_module' with the actual module name
from API.OpenAiAPI import OpenAIEmbeddingsAPI, OpenAITextCompletionAPI  # Replace 'your_openai_api_module' with the actual module name
from API.PineconeAPI import PineconeAPI  # Replace 'your_pinecone_api_module' with the actual module name


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


st.set_page_config(page_title="Home", page_icon="🦜️🔗")
st.title('Notion Database Explorer')

st.markdown(
    """
    the goal of this app is to explore the notion database and create a knowledge graph

    """
)

#get secret keys
with st.sidebar:
    # Get API keys
    st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
    # Get PINECONE keys
    st.session_state.pinecone_api_key = st.text_input("Pinecone API Key", value=st.session_state.pinecone_api_key, type="password")
    st.session_state.pinecone_env = st.text_input("Pinecone Enviroment", value=st.session_state.pinecone_env, type="password")
    st.session_state.pinecone_index = st.text_input("Pinecone Index Name", value=st.session_state.pinecone_index, type="password")
    st.session_state.pinecone_project_id = st.text_input("Pinecone Project ID", value=st.session_state.pinecone_project_id, type="password")
    # Get Notion keys
    st.session_state.notion_api_key = st.text_input("Notion API Key", value=st.session_state.notion_api_key, type="password")




db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"

'''
Main function: Get Data from Notion
- Streamlit UI - click button 1
- Notion API - Get Tasks, Project, Areas, and Knowledge DB content
- Open API - embed each row with OpenAI embeddings
- Pinecone API - Store it in a Pinecone DB
'''
# Toggle for "Only Areas"
only_areas = st.checkbox("Only Areas")
only_4 = st.checkbox("Only 4")



if st.button("Button 1 - START"):
    st.write("Button 1 - pressed")
    try:
        # Notion API - Get Areas DB content
        st.subheader("Retrieve data from Notion:")
        with st.spinner('Initializing notion connection...'):
            notionClass = NotionAPI(st.session_state.notion_api_key)

        with st.spinner('Areas'):
            try:
                areas_content = notionClass.query_database(only_4, db_id_areas)

                st.text(f"- Number of rows retrieved for areas: {len(areas_content['results'])}")
            except Exception as e:
                st.error (f"Area ready query notion: {e}")
        # Skip projects and tasks if "Only Areas" is checked
        if not only_areas:
            with st.spinner('Projects'):
                projects_content = notionClass.query_database(only_4, db_id_projects)
                st.text(f"- Number of rows retrieved for projects: {len(projects_content['results'])}")

            with st.spinner('Tasks'):
                tasks_content = notionClass.query_database(only_4, db_id_tasks)
                st.text(f"- Number of rows retrieved for tasks: {len(tasks_content['results'])}")

        # Open AI API - Embed each row with OpenAI embeddings
        st.subheader("Open API - embed each row with OpenAI embeddings")
        with st.spinner('Initializing Embedding data with OpenAI...'):
            embeddingClass = OpenAIEmbeddingsAPI(st.session_state.openai_api_key)

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

        # Upsert AREAS vectors into Pinecone index
        st.json(areas_vectors, expanded=False)
        st.json(projects_vectors, expanded=False)
        st.json(tasks_vectors, expanded=False)
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

# add space in the UI
st.text("")
st.text("")
st.text("")


if st.button("Get Areas structure"):
    fetch_and_display_notion_structure(st.session_state.notion_api_key, db_id_areas)