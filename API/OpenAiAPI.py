import requests
import tiktoken

class OpenAiAPI:
    """
    A class that provides methods for interacting with the OpenAI Embeddings API.

    Args:
        api_key (str): The API key for accessing the OpenAI Embeddings API.
        max_tokens (int, optional): The maximum number of tokens allowed for a text. Defaults to 2046.

    Attributes:
        api_key (str): The API key for accessing the OpenAI Embeddings API.
        max_tokens (int): The maximum number of tokens allowed for a text.
        headers (dict): The headers used for making API requests.

    Methods:
        count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
            Returns the number of tokens in a text string using a specified tokenizer encoding.

        is_within_token_limit(text: str) -> bool:
            Checks if the text string is within the specified token limit.

        generate_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
            Generates an embedding for a given text using a specified OpenAI embedding model.
            Checks if the text is within the token limit before generating the embedding.
    """

    def __init__(self, api_key: str, max_tokens: int = 2046):
        self.validate_api_key(api_key)
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def validate_api_key(self, api_key):
        if not api_key:
            raise ValueError("Open API key is missing or invalid")

    def count_tokens(self, text: str, encoding_name: str = "cl100k_base") -> int:
        """
        Returns the number of tokens in a text string using a specified tokenizer encoding.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    def is_within_token_limit(self, text: str) -> bool:
        """
        Checks if the text string is within the specified token limit.
        """
        return self.count_tokens(text) <= self.max_tokens

    def generate_embedding(self, text: str, model: str = "text-embedding-ada-002") -> list:
        """
        Generates an embedding for a given text using a specified OpenAI embedding model.
        Checks if the text is within the token limit before generating the embedding.
        """
        #add exceptions management
        
        if self.is_within_token_limit(text):
            payload = {
                "input": text,
                "model": model
            }
            response = requests.post(
                "https://api.openai.com/v1/embeddings", 
                headers=self.headers, 
                json=payload,
                timeout=10
                )
            
            return response.json()['data'][0]['embedding']
        else:
            raise ValueError("Text exceeds the maximum token limit.")

    def generate_text_completion(self, model: str, messages: str, max_tokens: int = 150, temperature: float = 0.7):
        """
        Generates text completions using the specified model and prompt.
        """
        try:
            payload = {
                "model":model,
                "messages":messages,
                "max_tokens":max_tokens,
                "temperature":temperature
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=10
                )
            return response.json()
        
        except Exception as e:
            print(f"An error occurred generate_text_completion: {e}")
            return None