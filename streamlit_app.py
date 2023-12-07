import streamlit as st
from langchain.llms import OpenAI
st.set_page_config(page_title="🦜🔗 Quickstart App")
st.title('🦜🔗 Quickstart App')

st.markdown(
    """
    This is the beginning of MVP for LangChain.    

    """
)

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = ""

if 'serper_api_key' not in st.session_state:
	st.session_state.serper_api_key = ""