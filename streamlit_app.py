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
    st.caption("*Required*")
    # Get PINECONE keys
    pinecone_api_key = st.text_input("Pinecone API Key", value=st.session_state.pinecone_api_key, type="password")
    pinecone_env = st.text_input("Pinecone Enviroment", value=st.session_state.pinecone_env, type="password")
    pinecone_index = st.text_input("Pinecone Index Name", value=st.session_state.pinecone_index, type="password")
    st.caption("*Required*")
    # Get Notion keys
    notion_api_key = st.text_input("Notion API Key", value=st.session_state.notion_api_key, type="password")
    st.caption("*Required*")



if st.button("Get Areas structure"):
    fetch_and_display_notion_structure(notion_api_key, 'c5fd05abfaca44f99b4e90358c3ed701')

if st.button("Get Projects structure"):
    fetch_and_display_notion_structure(notion_api_key, 'c20d87c181634f18bcd14c2649ba6e06')

if st.button("Get Tasks structure"):
    fetch_and_display_notion_structure(notion_api_key, '72c034d6343f4d1e926048b7dcbcbc2b')


if st.button("Test embeddings"):
    db_id_areas = "c5fd05abfaca44f99b4e90358c3ed701"
    db_id_projects = "c20d87c181634f18bcd14c2649ba6e06"
    db_id_tasks = "72c034d6343f4d1e926048b7dcbcbc2b"

    #agent = NotionQueryAgent(notion_api_key, db_id_areas)

    embeddingClass = OpenAIEmbeddingsAPI(openai_api_key)

    prompt = "What are the areas?"
    result = embeddingClass.generate_embedding(prompt)
    st.success(result)

