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
        #Notion API - Get Tasks, Project, Areas, and Knowledge DB content
        notionClass = NotionAPI(notion_api_key)

        areas_content = notionClass.query_database(db_id_areas, {"page_size": 10})
        project_content = notionClass.query_database(db_id_projects, {"page_size": 10})
        tasks_content = notionClass.query_database(db_id_tasks, {"page_size": 10})

        # Open API - embed each row with OpenAI embeddings
        embeddingClass = OpenAIEmbeddingsAPI(openai_api_key)

        areas_embedded = []
        for row in areas_content:
            embedded_row = embeddingClass.generate_embedding(row)
            areas_embedded.append(embedded_row)
            st.write(embedded_row)

        project_embedded = []
        for row in project_content:
            embedded_row = embeddingClass.generate_embedding(row)
            project_embedded.append(embedded_row)

        tasks_embedded = []
        for row in tasks_content:
            embedded_row = embeddingClass.generate_embedding(row)
            tasks_embedded.append(embedded_row)

        # Log the number of rows embedded
        st.write(f"Number of rows embedded for areas: {len(areas_embedded)}")
        st.write(f"Number of rows embedded for projects: {len(project_embedded)}")
        st.write(f"Number of rows embedded for tasks: {len(tasks_embedded)}")

        #vizualize in streamlit the content of the first row per table
        st.write("First row of areas content:")
        st.write(areas_content[1])
        st.write("First row of projects content:")
        st.write(project_content[1])
        st.write("First row of tasks content:")
        st.write(tasks_content[1])

        #Pinecone API - Store it in a Pinecone DB
        #pineconeClass = PineconeAPI(pinecone_api_key, "your_project_id", pinecone_env)
        #pineconeClass.upsert(pinecone_index, areas_embedded, "areas")
        #pineconeClass.upsert(pinecone_index, project_embedded, "projects")
        #pineconeClass.upsert(pinecone_index, tasks_embedded, "tasks")

        st.success("Data from Notion, OpenAI, and Pinecone successfully retrieved and stored.")

    except ValueError as e:
        st.error(f"Error: {e}")

    except Exception as e:
        # Handle other exceptions, possibly API related
        st.error("Failed to retrieve data from Notion.")
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

