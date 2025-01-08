from googlesearch import search, SearchResult
from typing import List
import requests
from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.interface.web_crawler import WebCrawler
from src.model.knowledge_info import KnowledgeInfo
from src.utils.utils import convert_html2markdown


class GoogleCrawler(WebCrawler):
    
    def __init__(
        self,
        markdown_splitter: MarkdownHeaderTextSplitter
    ) -> None:
        super(GoogleCrawler, self).__init__()
        self.markdown_splitter = markdown_splitter
    
        
        
    def crawl(self, query: str) -> List[KnowledgeInfo]:
        search_results = list(search(query, num_results=6, advanced=True))
        
        info = []
        for search_result in search_results:
            
            response = requests.get(search_result.url)
            
            if response.status_code == 200:
                html_content = response.text
                markdown_content = convert_html2markdown(html_content)
                info.append(
                    KnowledgeInfo(
                        page_content=markdown_content,
                        url=search_result.url
                    )
                )
            
            else:
                raise ValueError(f"Failed to fetch the URL: {response.status_code}")
        
        return info 