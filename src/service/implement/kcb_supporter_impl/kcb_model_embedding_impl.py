from sentence_transformers import SentenceTransformer
import torch

from src.service.interface.kcb_supporter.model_embedding import ModelEmbedding
from src.service.implement.kcb_supporter_impl.model_embedding_approaches.halong_embedding_impl import HaLongEmbedding
from src.utils.logger import Logger 

class KCBModelEmbeddingImpl(ModelEmbedding):
    def __init__(self, model_embedding_config: dict, logger: Logger = None):
        self.model_embedding_config = model_embedding_config
        self.logger = logger

    def encode(self, approach_id: int, query: str, **kwargs) -> None:
        # call class by string
        model_embedding_class = globals()[self.model_embedding_config[approach_id]['class_name']] 
        self.model_embedding_tool = model_embedding_class(**self.model_embedding_config[approach_id]['class_params'])

        # call function by string
        encode_params = self.model_embedding_config[approach_id]['encode_params']
        if encode_params is None:
            encode_params = {}
        self.model_embedding_tool.encode(query = query, **encode_params)

    def get_embedding(self, approach_id: int, **kwargs) -> torch.Tensor:
        # call function by string
        get_embedding_params = self.model_embedding_config[approach_id]['get_embedding_params']
        if get_embedding_params is None:
            get_embedding_params = {}
        query_embedding = self.model_embedding_tool.get_embedding(**get_embedding_params)
        return query_embedding
    
    def get_model_dim(self, approach_id: int) -> int:
        return self.model_embedding_config[approach_id]['model_dim']
        
        


