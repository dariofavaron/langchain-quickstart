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


import requests
import streamlit as st

def fetch_notion_database(notion_api_key, database_id, filter=None, sort=None):
    """
    Fetches data from a Notion database based on specified filter and sort criteria.
    
    Parameters:
    notion_api_key (str): The API key for Notion.
    database_id (str): The ID of the database to fetch.
    filter (dict): The filter criteria for querying the database.
    sort (list): The sorting criteria for the query results.
    
    Returns:
    dict: Database rows (DB_all, DB_row)
    """
    if not notion_api_key.strip():
        st.error("Please provide the Notion API key.")
        return
    try:
        with st.spinner('Fetching data from Notion...'):
            headers = {
                "Authorization": f"Bearer {notion_api_key}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-02-22",
            }
            body = {
                "filter": filter if filter else {},
                "sorts": sort if sort else []
            }
            response = requests.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers=headers,
                json=body
            )
            return response.json()  # Returns DB_all, DB_row
    except Exception as e:
        st.exception(f"An error occurred: {e}")
