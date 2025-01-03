from sentence_transformers import SentenceTransformer
import torch

from src.interface.model_embedding import ModelEmbedding

class HaLongEmbedding(ModelEmbedding):
    
    def __init__(
        self, 
        model_id: str
    ) -> None:
        super(HaLongEmbedding, self).__init__()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_id).to(device=self.device)
        self.query_embedding = None
        
        
    def encode(self, query: str) -> None:
        self.query_embedding = self.model.encode([query])

    def get_embedding(self) -> torch.Tensor:
        return self.query_embedding
