from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document

class DataLoader(ABC):
    
    @abstractmethod
    def load(self, path: str) -> None:
        pass
    
    @abstractmethod
    def chunk(self, chunk_size: int, chunk_overlap: int) -> List[Document]:
        pass