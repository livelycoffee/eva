from eva.core.system.services import Service
import chromadb
from typing import Any
import uuid
from pathlib import Path

file_path = Path(__file__)
src_path = file_path.parents[6]
database_path = src_path / "storage/memory/svmdatabase"

class SemanticMemoryService(Service):
    def __init__(self):
        self.chroma_client = None
        self.collection = None

    def start(self):
        self.chroma_client = chromadb.PersistentClient(path=database_path)
        self.collection = self.chroma_client.get_or_create_collection(name="testcollection")
    
    def stop(self):
        self.chroma_client = None
        self.collection = None

    def add_to_collection(self, documents: list, metadatas: list = None) -> None:
        self.collection.add(documents=documents, metadatas=metadatas, ids=[str(uuid.uuid4()) for _ in documents])

    def get_results(self, queries: Any, n_results: int) -> chromadb.QueryResult:
        results = self.collection.query(
            query_texts=queries,
            n_results=n_results
        )
        return results
