from abc import ABC, abstractmethod
from typing import Dict, Any

from src.model.searching_info import SearchingInfo

class VectorDatabase(ABC):
    
    @abstractmethod
    def write_json(self) -> None:
        pass
    
    @abstractmethod
    def load_json(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def searching(self, query: str) -> SearchingInfo:
        pass
    
    @abstractmethod
    def load_bin(self) -> None:
        pass
    
    @abstractmethod
    def indexing(self, query: str = None) -> None:
        pass