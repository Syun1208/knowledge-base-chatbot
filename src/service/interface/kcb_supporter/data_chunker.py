from abc import ABC, abstractmethod
from typing import List, Dict

from src.model.knowledge_information import KnowledgeInformation


class DataChunker(ABC):
    
    @abstractmethod
    def chunk(self, infomations: List[KnowledgeInformation], is_save_chunks: bool = True ) -> List[Dict[str, str]]:
        pass
