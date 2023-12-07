import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
import requests
import json
# import helper files to scrape Notion API
from helper_files import get_all_pages, get_page, get_page_content
from data_handle import visualize_notion_db_properties

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
st.title('🦜🔗 Quickstart App')

st.markdown(
    """
    This is the beginning of MVP for LangChain.    

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


#- Streamlit UI - click button 1
#- Notion API - Get Tasks, Project, Areas, and Knowledge DB

# Get Areas
if st.button("Get Tasks"):
    # Validate inputs
    if not notion_api_key.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner('Please wait...'):
              
              # set the headers
              headers = {
                  "Authorization": f"Bearer {notion_api_key}",
                  "Content-Type": "application/json",
                  "Notion-Version": "2022-02-22",
              }
              database_id = 'c5fd05abfaca44f99b4e90358c3ed701'
              area_db_content = requests.get(
                   f"https://api.notion.com/v1/databases/{database_id}",
                    headers=headers
              )
              st.json(area_db_content.json(), expanded=False)

              df_properties = visualize_notion_db_properties(area_db_content.json())
              st.dataframe(df_properties)

        except Exception as e:
            st.exception(f"An error occurred: {e}")


# Get Areas
if st.button("Get Tasks"):
    # Validate inputs
    if not notion_api_key.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner('Please wait...'):
              
              # set the headers
              headers = {
                  "Authorization": f"Bearer {notion_api_key}",
                  "Content-Type": "application/json",
                  "Notion-Version": "2022-02-22",
              }
              database_id = 'c20d87c181634f18bcd14c2649ba6e06'
              area_db_content = requests.get(
                   f"https://api.notion.com/v1/databases/{database_id}",
                    headers=headers
              )
              st.json(area_db_content.json(), expanded=False)

              df_properties = visualize_notion_db_properties(area_db_content.json())
              st.dataframe(df_properties)

        except Exception as e:
            st.exception(f"An error occurred: {e}")