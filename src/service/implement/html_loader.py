import requests
from typing import List
from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.service.interface.data_loader import DataLoader
from src.model.knowledge_info import KnowledgeInfo
from src.utils.utils import convert_html2markdown


class HTMLLoader(DataLoader):
    
    def __init__(
        self,
        markdown_splitter: MarkdownHeaderTextSplitter
    ) -> None:
        super(HTMLLoader, self).__init__()
        self.markdown_splitter = markdown_splitter
    
    
    
    def load(self, paths: List[str]) -> List[KnowledgeInfo]:

        info = []
        for path in paths:
            
            response = requests.get(path)
            
            if response.status_code == 200:
                html_content = response.text
                markdown_content = convert_html2markdown(html_content)
                info.append(
                    KnowledgeInfo(
                        page_content=markdown_content,
                        url=path
                    )
                )
                
            else:
                raise ValueError(f"Failed to fetch the URL: {response.status_code}")
        
        return info 
