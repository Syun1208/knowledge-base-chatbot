from langchain_text_splitters import MarkdownHeaderTextSplitter
from abc import ABC, abstractmethod
from typing import List, Dict
from markdown import markdown
from bs4 import BeautifulSoup
import re
import json
from src.model.knowledge_information import KnowledgeInformation
from src.service.implement.kcb_supporter_impl.chunking_approaches.markdown_chunking_impl import MarkdownChunking
from src.service.interface.kcb_supporter.data_chunker import DataChunker
from src.utils.logger import Logger 

class KCBDataChunkerImpl(DataChunker):
    def __init__(self, chunking_config: dict, logger: Logger = None):
        self.chunking_config = chunking_config
        self.logger = logger

    def chunk(self, approach_id: int, documents: List[KnowledgeInformation], save_path: str = None) -> List[Dict[str, str]]:
        # call class by string
        chunking_class = globals()[self.chunking_config[approach_id]['class_name']]
        chunking_tool = chunking_class()

        # call function by string
        method = getattr(chunking_tool, self.chunking_config[approach_id]['function_name'])
        function_params = self.chunking_config[approach_id]['function_params']

        # get all chunks
        chunks = method(documents = documents, **function_params)
        
        # Save documents
        if save_path is not None:
            self.write_json(documents=chunks, path=save_path)

        return chunks

    def write_json(self, documents, path: str):
        try:
            with open(path, 'w') as json_file:
                json.dump(documents, json_file)
        except Exception as e:
            print("ERROR: ", str(e))








