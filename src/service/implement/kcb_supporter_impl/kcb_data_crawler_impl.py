from googlesearch import search, SearchResult
from typing import List
import requests
from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.service.interface.kcb_supporter.data_crawler import DataCrawler
from src.model.knowledge_information import KnowledgeInformation
from src.utils.utils import convert_html2markdown, split_html_into_section_dict, format_markdown


class KCBDataCrawlerImpl(DataCrawler):
    def __init__(
        self,
        markdown_splitter: MarkdownHeaderTextSplitter):
        self.markdown_splitter = markdown_splitter
    
    def crawl_by_query(self, query: str) -> List[KnowledgeInformation]:
        search_results = list(search(query, num_results=6, advanced=True))
        
        info = []
        for search_result in search_results:
            
            response = requests.get(search_result.url)
            
            if response.status_code == 200:
                html_content = response.text
                markdown_content = convert_html2markdown(html_content)
                info.append(
                    KnowledgeInformation(
                        page_content=markdown_content,
                        url=search_result.url
                    )
                )
            
            else:
                raise ValueError(f"Failed to fetch the URL: {response.status_code}")
        
        return info 
    
    def crawl_by_url(self, urls: list[str]) -> List[KnowledgeInformation]:
        info = []
        for url in urls:
            
            response = requests.get(url)
            
            if response.status_code == 200:
                html_content = response.text
                sections_dict = split_html_into_section_dict(html_content)
                markdown_content = format_markdown(sections_dict)
                info.append(
                    KnowledgeInformation(
                        page_content=markdown_content,
                        url=url
                    )
                )
                
            else:
                raise ValueError(f"Failed to fetch the URL: {response.status_code}")
        
        return info  

