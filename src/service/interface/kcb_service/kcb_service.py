from src.model.searching_information import SearchingInformation
from src.model.knowledge_information import KnowledgeInformation

class KCBService:
    def indexing_knowledge(self, chunking_approach_id: int, model_embedding_approach_id: int) -> None:
        pass
    def indexing_web(self, urls: list[str], chunking_approach_id: int, model_embedding_approach_id: int) -> None:
        pass
    def searching(self, 
                query: str, 
                model_embedding_approach_id) -> SearchingInformation:
        pass

