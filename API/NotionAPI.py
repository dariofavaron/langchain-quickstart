import requests

# Modularization of Notion API interactions
class NotionAPI:
    """
    A class representing the Notion API.

    Attributes:
        headers (dict): The headers used for API requests.
            Contains the authorization token, content type, and Notion version.

    Methods:
        __init__(api_key): Initializes the NotionAPI object with the provided API key.
        get_database_structure(database_id): Retrieves the structure of a Notion database.
        query_database(database_id, filter, sort): Queries a Notion database with optional filter and sort parameters.
    """

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Notion API key is required")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

    def get_database_structure(self, database_id):
        """
        Retrieves the structure of a Notion database.

        Args:
            database_id (str): The ID of the database.

        Returns:
            Response: The response object containing the database structure.
        """
        try:
            response = requests.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers=self.headers
            )
            return response.json()
        except Exception as e:
            raise ValueError("An error occurred: {e}")

    def query_database(self, database_id):
        """
        Queries a Notion database with optional filter and sort parameters.

        Args:
            database_id (str): The ID of the database.
            filter (dict, optional): The filter parameters for the query. Defaults to None.
            sort (list, optional): The sort parameters for the query. Defaults to None.

        Returns:
            Response: The response object containing the query results.
        """
        try:
            body = {
                #"page_size": 4
            }

            response = requests.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers=self.headers,
                json=body
            )
            return response.json()
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")
