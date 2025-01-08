from abc import ABC, abstractmethod
from typing import List
from src.model.knowledge_info import KnowledgeInfo


class WebCrawler(ABC):
    
    @abstractmethod
    def crawl(self, query: str) -> List[KnowledgeInfo]:
        pass