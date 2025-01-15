import faiss
import torch
import tqdm
import torch.nn as nn
import json
from redis import Redis
import numpy as np
from typing import Any, Dict, List

from src.service.interface.vector_database import VectorDatabase
from src.service.interface.model_embedding import ModelEmbedding
from src.service.interface.data_loader import DataLoader
from src.model.knowledge_info import KnowledgeInfo
from src.model.searching_info import SearchingInfo
from src.service.interface.web_crawler import WebCrawler
from src.utils.logger import Logger
from src.service.interface.chunking import Chunking

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
        self.logger = logger.get_tracking(__name__)
        self.show_time_compute = show_time_compute
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.path_loads = path_loads
        self.path_save_documents = path_save_documents
        self.path_save_db = path_save_db
        self.top_k = top_k
       
       
    @staticmethod
    def write_json(documents, path: str):
        with open(path, 'w') as json_file:
            json.dump(documents, json_file)
           
            
    def load_json(self) -> Dict[str, Any]:
        with open(self.path_save_documents, 'r') as json_file:
            documents = json.load(json_file)
        return documents
    
    
    def load_bin(self) -> faiss.IndexFlatIP:
        cpu_index = faiss.read_index(self.path_save_db) 
        return cpu_index
 
    
    def indexing(
        self,
        cpu_index: faiss.IndexFlatIP,
        documents: List[KnowledgeInfo]
    ) -> None:
        
        # Chunking
        chunked_documents = self.chunking.chunk(documents)
        
        # Save documents
        self.write_json(documents=chunked_documents, path=self.path_save_documents)
        self.logger.info(f"Saved documents successfully at: {self.path_save_documents}")

        # Encode documents
        content_documents = [chunked_document['content'] for chunked_document in chunked_documents]
        self.model_embedding.encode(content_documents)
        for embedding in tqdm.tqdm(self.model_embedding.get_embedding(), colour='green', desc='Indexing'):
            embedding = embedding.astype(np.float32).reshape(1, -1)
            cpu_index.add(embedding)
        
        # Save vector database
        faiss.write_index(cpu_index, self.path_save_db)
        self.logger.info(f"Saved vector db successfully at: {self.path_save_db}")
    
    
    
    def searching(
        self, 
        cpu_index: faiss.IndexFlatIP,
        documents: List[KnowledgeInfo],
        query: str
    ) -> SearchingInfo:
        
        if cpu_index is None:
            AssertionError("Could not find vector database, please index it before searching !")
            return SearchingInfo(
                scores=None,
                texts=None,
                indices=None
            )
        
        if documents is None:
            AssertionError("Please load your local documents before searching !")
            return SearchingInfo(
                scores=None,
                texts=None,
                indices=None
            )
        
        self.model_embedding.encode([query])
        prompt_embedding = self.model_embedding.get_embedding()
        prompt_embedding = np.array(prompt_embedding)
        scores, indices = cpu_index.search(prompt_embedding, k=self.top_k)
        urls = [documents[i]['url'] for i in indices.flatten().tolist()]
        contexts = [documents[i]['content'] for i in indices.flatten().tolist()]
        
        return SearchingInfo(
            scores=scores.flatten().tolist(),
            urls=urls,
            contexts=contexts,
            indices=indices.flatten().tolist()
        )
        