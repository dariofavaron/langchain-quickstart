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
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            raise ValueError(f"Error - get_database_structure : {e}")

    def query_database(self, amount, only_4, database_id):
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
                "sorts": [
                    {
                    "timestamp": "last_edited_time",
                    "direction": "descending"
                    }
                ]
            }
            
            if only_4:
                body["page_size"] = 4
            if amount:
                if amount!=0:
                    body["page_size"] = amount


            response = requests.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers=self.headers,
                json=body,
                timeout=10
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Error - query_database: {e}")

    def get_page_content(self, st, page_id):
        """
        Get and return the page content from the Notion API    
        """
        try:
            
            # get all the block for page associated with created_id
            response = requests.get(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers=self.headers,
                timeout=10
            )
            st.write("get_page_content request response: ")
            st.json(response.json(), expanded=False)

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(f"API request failed with status code: {response.status_code}")


            # string to store the page content of current page
            page_content = ""
            blocks = response.json().get("results", [])
            #st.write(blocks)

            # Iterate over the blocks
            for block in blocks:
                block_type = block.get("type")

                if block[block_type]["rich_text"]:
                    content = block[block_type]["rich_text"][0]["text"]["content"]
                    page_content += content + "\n"  # Append content with a newline
                else:
                    # Skip the block if it doesn't contain the expected keys
                    continue
            # return the page content
            return page_content
        
        except Exception as e:
            raise Exception(f"Error - get_page_content: {e}")

    def create_page(self, database_id, properties, children=None, icon=None, cover=None):
        """
        Creates a new page in a Notion database.

        Args:
            database_id (str): The ID of the parent database.
            properties (dict): The properties of the new page.
            children (list, optional): A list of children blocks for page content. Defaults to None.
            icon (dict, optional): Icon of the page. Defaults to None.
            cover (dict, optional): Cover of the page. Defaults to None.

        Returns:
            dict: The response from the Notion API.
        """

        # Construct the request payload
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        if children:
            data["children"] = children
        if icon:
            data["icon"] = icon
        if cover:
            data["cover"] = cover

        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.headers,
                json=data,
                timeout=10
            )

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(f"API request failed with status code: {response.status_code}")

            return response.json()

        except Exception as e:
            raise Exception(f"Error - create_page: {e}")