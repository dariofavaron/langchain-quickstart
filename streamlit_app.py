import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import BaseLLM
from langchain_agents import NotionQueryAgent
import requests
import json
# import helper files to scrape Notion API
from helper_files import get_all_pages, get_page, get_page_content
from notion_functions import fetch_and_display_notion_structure
from GeneralFunctions.vector_management import create_area_vector_with_extracted_data, create_project_vector_with_extracted_data

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
    openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
    # Get PINECONE keys
    pinecone_api_key = st.text_input("Pinecone API Key", value=st.session_state.pinecone_api_key, type="password")
    pinecone_env = st.text_input("Pinecone Enviroment", value=st.session_state.pinecone_env, type="password")
    pinecone_index = st.text_input("Pinecone Index Name", value=st.session_state.pinecone_index, type="password")
    # Get Notion keys
    notion_api_key = st.text_input("Notion API Key", value=st.session_state.notion_api_key, type="password")


db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"

'''
Main fucntion: Get Data from Notion
- Streamlit UI - click button 1
- Notion API - Get Tasks, Project, Areas, and Knowledge DB content
- Open API - embed each row with OpenAI embeddings
- Pinecone API - Store it in a Pinecone DB
'''
if st.button("Button 1 - Get Data from Notion"):
    try:
        #Notion API - Get Areas DB content
        with st.spinner('Fetching data from Notion...'):
            st.write("Fetching data from Notion...")
            notionClass = NotionAPI(notion_api_key)

            areas_content = notionClass.query_database(db_id_areas)
            projects_content = notionClass.query_database(db_id_projects)
            tasks_content = notionClass.query_database(db_id_tasks)

            st.write(f"Number of rows retrieved for areas: {len(areas_content['results'])}")
            st.write(f"Number of rows retrieved for projects: {len(projects_content['results'])}")
            st.write(f"Number of rows retrieved for tasks: {len(tasks_content['results'])}")


        # Open API - embed each row with OpenAI embeddings
        with st.spinner('creating vector and Embedding data with OpenAI...'):
            st.write("creating vector and Embedding areas content:")
            embeddingClass = OpenAIEmbeddingsAPI(openai_api_key)

            st.write("areas:")
            areas_vectors = []
            for result in areas_content["results"]:
                st.write("result: ")
                st.json(result, expanded=False)
                vector = create_area_vector_with_extracted_data(result, embeddingClass)
                areas_vectors.append(vector)
                st.write("vector: ")
                st.json(vector, expanded=False)
            st.write(f"Number of rows embedded for areas: {len(areas_vectors)}")

            st.write("projects:")
            projects_vectors = []
            for result in projects_content["results"]:
                st.write("result: ")
                st.json(result, expanded=False)
                vector = create_project_vector_with_extracted_data(result, embeddingClass)
                projects_vectors.append(vector)
                st.write("vector: ")
                st.json(vector, expanded=False)
            st.write(f"Number of rows embedded for projects: {len(projects_vectors)}")


        st.success("Data from Notion, OpenAI, and Pinecone successfully retrieved and stored.")

    except ValueError as e:
        st.error(f"Error: {e}")

    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error(f"Error details: {e}")

if st.button("Get Areas structure"):
    fetch_and_display_notion_structure(notion_api_key, db_id_areas)

if st.button("Get Projects structure"):
    fetch_and_display_notion_structure(notion_api_key, db_id_projects)

if st.button("Get Tasks structure"):
    fetch_and_display_notion_structure(notion_api_key, db_id_tasks)


if st.button("Test embeddings"):
    try:
        embeddingClass = OpenAIEmbeddingsAPI(openai_api_key)
        prompt = "What are the areas?"
        result = embeddingClass.generate_embedding(prompt)
        st.success(result)
    except ValueError as e:  # Catching invalid or missing API key error
        st.error(f"Error: {e}")
    except Exception as e:  # Catching other potential errors (e.g., network issues, API errors)
        st.error(f"An unexpected error occurred: {e}")

