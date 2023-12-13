import requests

class PineconeAPI:
    """
    A class that provides methods to interact with the Pinecone API.

    Args:
        api_key (str): The API key for authentication.
        project_id (str): The ID of the project.
        environment (str): The environment of the Pinecone service.

    Attributes:
        api_key (str): The API key for authentication.
        project_id (str): The ID of the project.
        environment (str): The environment of the Pinecone service.
        headers (dict): The headers for API requests.

    Methods:
        query(index_name, query_vector, topK, namespace, include_metadata=False):
            Queries the Pinecone database using a query vector and retrieves similar item ids along with their scores.

        upsert(index_name, vectors, namespace):
            Upserts vectors into the Pinecone database in the specified namespace.
            Each vector should contain an 'id', 'values', and optional 'metadata'.
    """

    def __init__(self, api_key: str, index_name:str, project_id: str, environment: str):
        self.validate_api_key(api_key)
        self.api_key = api_key
        self.index_name = index_name
        self.project_id = project_id
        self.environment = environment
        self.headers = {"Api-Key": api_key}


    def validate_api_key(self, api_key):
        if not api_key:
            raise ValueError("Pinecone API key is missing or invalid")


    def DescribeIndexStats(self):
        """
        Returns the statistics of the index.
        """
        url = f"https://{self.index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/describe_index_stats"
        response = requests.post(url, headers=self.headers, timeout=10)
        return response.json()

    
    def query(self, query_vector: list, topK: int = 10, namespace: str, include_metadata: bool = False):
        """
        Queries the Pinecone database using a query vector and retrieves similar item ids along with their scores.

        Args:
            index_name (str): The name of the index to query.
            query_vector (list): The query vector.
            topK (int): The number of similar items to retrieve.
            namespace (str): The namespace of the index.
            include_metadata (bool, optional): Whether to include metadata in the response. Defaults to False.

        Returns:
            dict: The response JSON containing similar item ids and scores.
        """
        url = f"https://{self.index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/query"
        payload = {
            "namespace": namespace,
            "topK": topK,
            "vector": query_vector,
            "filter": {},
            "includeValues": "false",
            "includeMetadata": "false"
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=10)
        return response.json()

    def upsert(self, vectors:list, namespace: str):
        """
        Upserts vectors into the Pinecone database in the specified namespace.
        Each vector should contain an 'id', 'values', and optional 'metadata'.

        Args:
            index_name (str): The name of the index to upsert vectors into.
            vectors (list): The list of vectors to upsert.
            namespace (str): The namespace of the index.

        Returns:
            dict: The response JSON containing the upsert result.
        """
        url = f"https://{self.index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/vectors/upsert"
        payload = {
            "vectors": vectors,
            "namespace": namespace
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=10)
        return response.json()
