from abc import ABC, abstractmethod
from typing import List

from src.model.web_search_info import WebSearchInfo


class Chunking(ABC):
    
    @abstractmethod
    def chunk(self, infomations: List[WebSearchInfo]) -> List[WebSearchInfo]:
        pass