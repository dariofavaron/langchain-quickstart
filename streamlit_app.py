import streamlit as st

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = ""
	
st.set_page_config(page_title="Home", page_icon="🦜️🔗")

st.header("Welcome to LangChain! 👋")

st.title('🦜🔗 Quickstart App')

st.markdown(
    """
    This is the beginning of MVP for LangChain.    

    """
)

with st.sidebar:
    # Get API keys
    openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
    st.caption("*Required for all apps; get it [here](https://platform.openai.com/account/api-keys).*")