from abc import ABC, abstractmethod
from typing import List, Dict

from src.model.knowledge_info import KnowledgeInfo


class Chunking(ABC):
    
    @abstractmethod
    def chunk(self, infomations: List[KnowledgeInfo]) -> List[Dict[str, str]]:
        pass