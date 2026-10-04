from eva.core.system.services import API
from .service import PrimaryLLMService

class PrimaryLLMAPI(API):
    def __init__(self, parent_service):
        self.service: PrimaryLLMService = parent_service

    def get_llm_response(self, query: str, memories: str = ""):
        return self.service.get_response(query=query, memories=memories)
