import unittest
from unittest.mock import patch
from notion_functions import fetch_notion_database

class TestFetchNotionDatabase(unittest.TestCase):
    @patch('notion_functions.requests.post')
    def test_fetch_notion_database_success(self, mock_post):
        # Mock the response from the API
        mock_post.return_value.json.return_value = {
            "DB_all": [],
            "DB_row": {}
        }

        # Call the function with sample data
        result = fetch_notion_database("API_KEY", "DATABASE_ID", filter={}, sort=[])

        # Assert that the API was called with the correct parameters
        mock_post.assert_called_once_with(
            "https://api.notion.com/v1/databases/DATABASE_ID/query",
            headers={
                "Authorization": "Bearer API_KEY",
                "Content-Type": "application/json",
                "Notion-Version": "2022-02-22"
            },
            json={
                "filter": {},
                "sorts": []
            }
        )

        # Assert that the function returned the expected result
        self.assertEqual(result, {
            "DB_all": [],
            "DB_row": {}
        })

    @patch('notion_functions.requests.post')
    def test_fetch_notion_database_error(self, mock_post):
        # Mock an exception being raised
        mock_post.side_effect = Exception("API Error")

        # Call the function with sample data
        result = fetch_notion_database("API_KEY", "DATABASE_ID", filter={}, sort=[])

        # Assert that the function returned None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()