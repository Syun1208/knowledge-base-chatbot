
# for monitor
import os
import pandas as pd

import torch
import faiss
import json
import tqdm
import numpy as np
from typing import Any, Dict, List

from src.service.interface.kcb_supporter.data_crawler import DataCrawler 
from src.service.interface.kcb_supporter.data_chunker import DataChunker
from src.service.interface.kcb_supporter.model_embedding import ModelEmbedding
from src.service.interface.kcb_service.kcb_service import KCBService
from src.model.knowledge_information import KnowledgeInformation
from src.model.searching_information import SearchingInformation
from src.utils.utils import *

class KCBServiceImpl(KCBService):
    def __init__(self,
                 data_crawler: DataCrawler,
                 data_chunker: DataChunker,
                 model_embedding: ModelEmbedding,
                 knowledge_config: dict,
                 vector_db_config: dict):
        self.data_crawler = data_crawler 
        self.data_chunker = data_chunker
        self.model_embedding = model_embedding
        self.knowledge_config = knowledge_config
        self.vector_db_config = vector_db_config

    def __indexing(self, 
                urls: list[str],
                chunking_approach_id: int, 
                model_embedding_approach_id: int,
                is_new_knowledge: bool = False):
        # crawl data
        # documents = self.data_crawler.crawl_by_url(urls)
        documents = []
        paths = ['./data/employee-handbook-2.md', './data/nexcel-career-development-handbook.md']
        urls = ['https://nexcel.info/employee-handbook-2/', 'https://nexcel.info/nexcel-career-development-handbook/']
        for p, u in zip(paths, urls):
            with open(p, "r", encoding="utf-8") as f:
                page_content = f.read()

            documents.append(KnowledgeInformation(page_content=page_content, url=u))

        # special handle for new knowledge
        if is_new_knowledge:
            old_documents = self.__load_json(self.knowledge_config['path_save_documents'])
            old_documents = [
                KnowledgeInformation(
                    url=old_document['url'],
                    page_content=old_document['content']
                ) for old_document in old_documents
            ]
            documents = old_documents + documents
        
        # indexing and store to db
        # chunking data
        chunked_documents = self.data_chunker.chunk(approach_id = chunking_approach_id, 
                                                    documents = documents, 
                                                    save_path = self.knowledge_config['path_save_documents'])
        # encode documents
        content_documents = [chunked_document['content'] for chunked_document in chunked_documents]
        self.model_embedding.encode(approach_id = model_embedding_approach_id, 
                                    query = content_documents)
        
        # indexing
        cpu_index = faiss.IndexFlatIP(self.model_embedding.get_model_dim(model_embedding_approach_id))
        for embedding in tqdm.tqdm(self.model_embedding.get_embedding(model_embedding_approach_id), colour='green', desc='Indexing'):
            embedding = embedding.astype(np.float32).reshape(1, -1)
            cpu_index.add(embedding)
        
        # Save vector database
        faiss.write_index(cpu_index, self.vector_db_config['path_save_db'])

    def indexing_knowledge(self, chunking_approach_id: int, model_embedding_approach_id: int) -> None:
        self.__indexing(self.knowledge_config['urls'], chunking_approach_id, model_embedding_approach_id)

    def indexing_web(self, urls: list[str], chunking_approach_id: int, model_embedding_approach_id: int) -> None:
        self.__indexing(urls, chunking_approach_id, model_embedding_approach_id, True)
    
    def searching(self, query: str, model_embedding_approach_id:int ) -> SearchingInformation:
        query = detect_and_translate(query)
        print("After translate: ", query)
        cpu_index = self.__load_bin(self.vector_db_config['path_save_db'])
        documents = self.__load_json(self.knowledge_config['path_save_documents'])
        
        if cpu_index is None:
            AssertionError("Could not find vector database, please index it before searching !")
            return SearchingInformation(
                scores=None,
                texts=None,
                indices=None
            )
        
        if documents is None:
            AssertionError("Please load your local documents before searching !")
            return SearchingInformation(
                scores=None,
                texts=None,
                indices=None
            )
        
        self.model_embedding.encode(approach_id = model_embedding_approach_id, query = [query])
        prompt_embedding = self.model_embedding.get_embedding(approach_id = model_embedding_approach_id)
        prompt_embedding = np.array(prompt_embedding)
        scores, indices = cpu_index.search(prompt_embedding, k=self.vector_db_config['top_k'])
        urls = [documents[i]['url'] for i in indices.flatten().tolist()]
        contexts = [documents[i]['content'] for i in indices.flatten().tolist()]

        if os.path.exists("./searching_results.csv"):
            searching_results_df = pd.read_csv("./searching_results.csv")
            max_id = searching_results_df['QueryID'].max()
        else:
            searching_results_df = pd.DataFrame()
            max_id = 0

        searching_result_df_i = pd.DataFrame()
        searching_result_df_i['Score'] = scores[0]
        searching_result_df_i['Context'] = contexts
        searching_result_df_i['Query'] = query
        searching_result_df_i['QueryID'] = max_id+1

        searching_results_df = pd.concat([searching_results_df, searching_result_df_i], ignore_index=True)
        searching_results_df.to_csv("./searching_results.csv", index=False)

        
        
        return SearchingInformation(
            scores=scores.flatten().tolist(),
            urls=urls,
            contexts=contexts,
            indices=indices.flatten().tolist()
        )

    def __load_json(self, path) -> Dict[str, Any]:
        with open(path, 'r') as json_file:
            documents = json.load(json_file)
        return documents
    
    def __load_bin(self, path) -> faiss.IndexFlatIP:
        cpu_index = faiss.read_index(path) 
        return cpu_index

    def run(self):
        pass
        # data = pd.read_csv("data4tuning_shortterm_dataframe.csv")
        # start_id = 517
        # for q in tqdm.tqdm(data['Question'].values[start_id:]):
        #     try:
        #         _, id = self.searching(query= q , model_embedding_approach_id=1)
        #     except:
        #         pass
            