from eva.core.system.services.api import API
from .service import SemanticMemoryService
from typing import Any
from chromadb import QueryResult

class SemanticMemoryAPI(API):
    def __init__(self, parent_service):
        self.service: SemanticMemoryService = parent_service

    def add_memory(self, memories:str, metadata:str) -> None:
        if isinstance(memories, str):
            memories = [memories]
        elif not isinstance(memories, list):
            memories = list(memories)

        if isinstance(metadata, str):
            metadata = [metadata]
        elif not isinstance(metadata, list):
            metadata = list(metadata)

        try:
            self.service.add_to_collection(documents=memories, metadatas=metadata)
        except Exception as e:
            print(f"[SMService]: {e}")
            pass

    def get_memories(self, queries: Any, n_results:int = 2) -> QueryResult:
        if isinstance(queries, str):
            queries = [queries]
        elif not isinstance(queries, list):
            queries = list(queries)

        return self.service.get_results(queries=queries, n_results=n_results)
