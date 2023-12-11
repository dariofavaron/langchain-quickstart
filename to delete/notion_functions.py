import streamlit as st
import requests
from data_handle import visualize_notion_db_properties

def fetch_and_display_notion_structure(notion_api_key, database_id):
    """
    Fetches and displays the structure of a Notion database.
    
    Parameters:
    notion_api_key (str): The API key for Notion.
    database_id (str): The ID of the database to fetch.
    """
    if not notion_api_key.strip():
        st.error("Please provide the missing fields.")
        return
    try:
        with st.spinner('Please wait...'):
            headers = {
                "Authorization": f"Bearer {notion_api_key}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-02-22",
            }
            db_content = requests.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers=headers
            )
            st.json(db_content.json(), expanded=False)

            df_properties = visualize_notion_db_properties(db_content.json())
            st.dataframe(df_properties)

    except Exception as e:
        st.exception(f"An error occurred: {e}")
