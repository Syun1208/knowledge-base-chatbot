from abc import ABC, abstractmethod
from typing import List
from src.model.knowledge_information import KnowledgeInformation


class DataCrawler(ABC):
    @abstractmethod
    def crawl_by_query(self, query: str) -> List[KnowledgeInformation]:
        pass

    @abstractmethod
    def crawl_by_url(self, urls: str) -> List[KnowledgeInformation]:
        pass
