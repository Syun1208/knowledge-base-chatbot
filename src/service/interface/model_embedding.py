from abc import ABC, abstractmethod
import torch

class ModelEmbedding(ABC):
    
    @abstractmethod
    def encode(self, query) -> None:
        pass
    
    @abstractmethod
    def get_embedding(self) -> torch.Tensor:
        pass