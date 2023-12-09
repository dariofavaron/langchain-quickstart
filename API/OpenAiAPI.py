import requests, openai
import tiktoken

class OpenAIEmbeddingsAPI:
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
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

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
        if self.is_within_token_limit(text):
            payload = {
                "input": text,
                "model": model
            }
            response = requests.post("https://api.openai.com/v1/embeddings", headers=self.headers, json=payload)
            return response.json()['data'][0]['embedding']
        else:
            raise ValueError("Text exceeds the maximum token limit.")

# Example usage
# openai_embeddings_api = OpenAIEmbeddingsAPI(api_key="your_openai_key")
# if openai_embeddings_api.is_within_token_limit("Your text string goes here"):
#     embedding = openai_embeddings_api.generate_embedding("Your text string goes here")
# else:
#     print("Text is too long for embedding.")


class OpenAITextCompletionAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_text_completion(self, model: str, prompt: str, max_tokens: int = 150, temperature: float = 0.7):
        """
        Generates text completions using the specified model and prompt.
        - model: The model to use for the completion (e.g., "gpt-3.5-turbo-instruct").
        - prompt: The prompt to send to the model.
        - max_tokens: The maximum number of tokens to generate.
        - temperature: Controls the randomness of the output (0.0-1.0).
        """
        try:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
# Replace 'your_openai_api_key' with your actual OpenAI API key
openai_text_completion_api = OpenAITextCompletionAPI(api_key="your_openai_api_key")
prompt = "Write a short story about a robot learning to love."
model = "gpt-3.5-turbo-instruct"

# Generate text completion
completion = openai_text_completion_api.generate_text_completion(model=model, prompt=prompt)
print(completion)
