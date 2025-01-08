from abc import ABC, abstractmethod
from typing import List, Any
from langchain.schema import Document

class DataLoader(ABC):
    
    @abstractmethod
    def load(self, path: List[str]) -> List[Any]:
        pass