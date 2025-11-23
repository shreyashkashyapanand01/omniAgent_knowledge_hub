import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra
import cassio
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        self.astra_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.astra_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.hf_token = os.getenv("HF_TOKEN")
        
        if not self.astra_token or not self.astra_endpoint:
            raise ValueError("AstraDB credentials missing in .env")

        # Initialize CassIO
        cassio.init(token=self.astra_token, database_id=self.astra_endpoint)
        
        # Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Initialize Vector Store
        self.vector_store = Cassandra(
            embedding=self.embeddings,
            table_name="omni_agent_knowledge_hub",
            session=None,
            keyspace=None
        )

    def add_documents(self, documents):
        """Adds a list of documents to the vector store."""
        self.vector_store.add_documents(documents)

    def as_retriever(self):
        """Returns the vector store as a retriever."""
        return self.vector_store.as_retriever()

# Singleton instance
vector_store_instance = VectorStore()
