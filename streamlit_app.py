import streamlit as st

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = ""

if 'serper_api_key' not in st.session_state:
	st.session_state.serper_api_key = ""
	
st.set_page_config(page_title="Home", page_icon="🦜️🔗")

st.header("Welcome to LangChain! 👋")

st.title('🦜🔗 Quickstart App')

st.markdown(
    """
    This is the beginning of MVP for LangChain.    

    """
)

with st.sidebar:
    openai_api_key_Test = st.text_input("OpenAI API key", value="", type="password")
    st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")