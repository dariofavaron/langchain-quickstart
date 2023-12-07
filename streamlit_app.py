import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
# import helper files to scrape Notion API
from helper_files import get_all_pages, get_page, get_page_content

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

## JUST TO SEE IF IT WORKS

source_text = st.text_area("Source Text", label_visibility="collapsed", height=200)

# If the 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key.strip() or not source_text.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner('Please wait...'):
              # Split the source text
              text_splitter = CharacterTextSplitter()
              texts = text_splitter.split_text(source_text)

              # Create Document objects for the texts (max 3 pages)
              docs = [Document(page_content=t) for t in texts[:3]]

              # Initialize the OpenAI module, load and run the summarize chain
              llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
              chain = load_summarize_chain(llm, chain_type="map_reduce")
              summary = chain.run(docs)

              st.success(summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")



#- Streamlit UI - click button 1
#- Notion API - Get Tasks, Project, Areas, and Knowledge DB

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

              # get all pages we have access to with the integration
              pages = get_all_pages(headers)

              st.success(pages)
        except Exception as e:
            st.exception(f"An error occurred: {e}")