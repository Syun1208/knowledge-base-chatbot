from langchain_text_splitters import MarkdownHeaderTextSplitter
from typing import List, Dict
from markdown import markdown
from bs4 import BeautifulSoup
import re

from src.model.knowledge_info import KnowledgeInfo
from src.interface.chunking import Chunking


class MarkdownChunking(Chunking):
    
    def __init__(self):
        super().__init__()
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
        ]
        
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on, 
            strip_headers=False
        ) 
        
        
    def chunk(self, infomations: List[KnowledgeInfo]) -> List[Dict[str, str]]:
        
        chunks = []
        for info in infomations:
        
            md_header_splits = self.markdown_splitter.split_text(info.page_content)

            for md_header_split in md_header_splits:
                html = markdown(md_header_split.page_content)
                page_content = ''.join(BeautifulSoup(html).findAll(text=True))
                page_content = re.sub(r'\| --- \| --- \| --- \|', '', page_content)
                page_content = re.sub(r'\n+', '\n', page_content).strip()
                chunks.append({
                    'url': info.url,
                    'content': page_content
                })
               
        return chunks