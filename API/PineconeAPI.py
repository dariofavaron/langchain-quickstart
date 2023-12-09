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

    def __init__(self, api_key: str, project_id: str, environment: str, namespaces: list = []):
        self.validate_api_key(api_key)
        self.api_key = api_key
        self.project_id = project_id
        self.environment = environment
        self.headers = {"Api-Key": api_key}

        updated_indexes = self.list_indexes_and_create_if_not_exists(api_key, namespaces)

        if updated_indexes != namespaces:
            raise ValueError("Indexes were not created correctly")
        
        return updated_indexes


    def validate_api_key(self, api_key):
        if not api_key:
            raise ValueError("Pinecone API key is missing or invalid")

    def list_indexes_and_create_if_not_exists(self, api_key, namespaces):
        indexes = self.list_indexes()
        for namespace in namespaces:
            if namespace not in indexes:
                self.create_index(namespace, dimension=1536)
        return self.list_indexes()


    def list_indexes(self):
        """
        Lists the indexes in the Pinecone project.
        list_indexes
        GET
        https://controller.us-east1-gcp.pinecone.io/databases
        This operation returns a list of your Pinecone indexes.
        Returns:
            list: The list of indexes.
        """
        url = f"https://{index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/databases"
        response = requests.get(url, headers=self.headers)
        indexes = []
        for index in response.json():
            indexes.append(index["name"])
            
        return indexes
    
    def query(self, index_name: str, query_vector: list, topK: int, namespace: str, include_metadata: bool = False):
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
        url = f"https://{index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/query"
        payload = {
            "namespace": namespace,
            "topK": topK,
            "filter": {
                "includeMetadata": include_metadata,
                "vector": query_vector
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def upsert(self, index_name: str, vectors: list, namespace: str):
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
        url = f"https://{index_name}-{self.project_id}.svc.{self.environment}.pinecone.io/vectors/upsert"
        payload = {
            "vectors": vectors,
            "namespace": namespace
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()
