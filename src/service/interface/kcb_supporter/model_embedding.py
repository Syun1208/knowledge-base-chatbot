from abc import ABC, abstractmethod
import torch

class ModelEmbedding(ABC):
    
    @abstractmethod
    def encode(self, approach_id: int, query: str, **kwargs) -> None:
        pass
    
    @abstractmethod
    def get_embedding(self, approach_id: int,**kwargs) -> torch.Tensor:
        pass

    @abstractmethod
    def get_model_dim(self, approach_id: int) -> int:
        pass