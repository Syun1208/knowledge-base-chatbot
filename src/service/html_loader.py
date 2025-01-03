import requests
from bs4 import BeautifulSoup
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.interface.data_loader import DataLoader


class HTMLLoader(DataLoader):
    
    def __init__(self):
        self.data = None
        self.text_splitter = RecursiveCharacterTextSplitter()
    
    def chunk(
        self,
        chunk_size: int,
        chunk_overlap: int
    ) -> List[Document]:
        
        document = Document(
            page_content=self.data['text'],
            metadata={
                'title': self.data['title'],
                'links': self.data['links'],
            }
        )
        self.text_splitter._chunk_size = chunk_size
        self.text_splitter._chunk_overlap = chunk_overlap
        documents = self.text_splitter.split_documents([document])
    
        return documents
    
    def load(
        self, 
        path: str
    ) -> None:
        
        response = requests.get(path)

        if response.status_code == 200:
            html_content = response.text
        else:
            print('Failed to retrieve the html')
            
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string
        all_text = soup.get_text()
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        self.data = {
            'title': title,
            'text': all_text,
            'links': links
        }
