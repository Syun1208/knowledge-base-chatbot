import faiss
import torch
import tqdm
import torch.nn as nn
import json
from redis import Redis
import numpy as np
from typing import Any, Dict, List

from src.interface.vector_database import VectorDatabase
from src.interface.model_embedding import ModelEmbedding
from src.interface.data_loader import DataLoader
from src.model.searching_info import SearchingInfo
from src.interface.web_crawler import WebCrawler
from src.utils.logger import Logger
from src.interface.chunking import Chunking

class FaissDB(VectorDatabase):
    
    def __init__(
        self,
        model_embedding: ModelEmbedding,
        model_dim: int,
        document_loader: DataLoader,
        web_crawler: WebCrawler,
        chunking: Chunking,
        logger: Logger,
        path_loads: List[str],
        path_save_documents: str,
        path_save_db: str,
        top_k: int,
        show_time_compute: bool = False
    ) -> None:
        super(FaissDB, self).__init__()
        
        self.model_embedding = model_embedding
        self.model_dim = model_dim
        self.document_loader = document_loader
        self.web_crawler = web_crawler
        self.chunking = chunking
        self.cpu_index = None
        self.logger = logger.get_tracking(__name__)
        self.show_time_compute = show_time_compute
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.documents = None
        self.path_loads = path_loads
        self.path_save_documents = path_save_documents
        self.path_save_db = path_save_db
        self.top_k = top_k
       
    def write_json(self, path: str):
        with open(path, 'w') as json_file:
            json.dump(self.documents, json_file)
          
            
    def load_json(self) -> Dict[str, Any]:
        with open(self.path_save_documents, 'r') as json_file:
            self.documents = json.load(json_file)
    
    
    def load_bin(self) -> None:
        self.cpu_index = faiss.read_index(self.path_save_db) 
 
    
    def indexing(
        self,
        query: str = None
    ) -> None:
        self.cpu_index = faiss.IndexFlatIP(self.model_dim)
        
        # load documents and chunking
        if query is not None:
            self.documents = self.document_loader.load(self.path_loads)
            
        else:
            self.documents = self.web_crawler.crawl(query=query)
        
        self.documents = self.chunking.chunk(self.documents)
        
        # Save documents
        self.write_json(path=self.path_save_documents)
        self.logger.info(f"Saved documents successfully at: {self.path_save_documents}")
        
        # Encode documents
        self.model_embedding.encode(self.documents)
        for embedding in tqdm.tqdm(self.model_embedding.get_embedding(), colour='green', desc='Indexing'):
            embedding = embedding.astype(np.float32).reshape(1, -1)
            self.cpu_index.add(embedding)
        
        # Save vector database
        faiss.write_index(self.cpu_index, self.path_save_db)
        self.logger.info(f"Saved vector db successfully at: {self.path_save_db}")
    
    
    
    def searching(self, query: str) -> SearchingInfo:
        
        if self.cpu_index is None:
            AssertionError("Could not find vector database, please index it before searching !")
            return SearchingInfo(
                scores=None,
                texts=None,
                indices=None
            )
        
        if self.documents is None:
            AssertionError("Please load your local documents before searching !")
            return SearchingInfo(
                scores=None,
                texts=None,
                indices=None
            )
        
        self.model_embedding.encode([query])
        prompt_embedding = self.model_embedding.get_embedding()
        prompt_embedding = np.array(prompt_embedding)
        scores, indices = self.cpu_index.search(prompt_embedding, k=self.top_k)
        contexts = [self.documents[i] for i in indices.flatten().tolist()]
        
        return SearchingInfo(
            scores=scores.flatten().tolist(),
            contexts=contexts,
            indices=indices.flatten().tolist()
        )
        