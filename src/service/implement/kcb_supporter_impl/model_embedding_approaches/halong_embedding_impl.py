from sentence_transformers import SentenceTransformer
import torch

class HaLongEmbedding():
    def __init__(
        self, 
        model_id: str
    ) -> None:
        super(HaLongEmbedding, self).__init__()
        self.model_id = model_id
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_id).to(device=self.device)
        self.query_embedding = None
        
        
    def encode(self, query: str, **kwargs) -> None:
        self.query_embedding = self.model.encode(query)

    def get_embedding(self, **kwargs) -> torch.Tensor:
        return self.query_embedding
