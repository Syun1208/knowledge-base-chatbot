from langchain_text_splitters import MarkdownHeaderTextSplitter
from typing import List, Dict
from markdown import markdown
from bs4 import BeautifulSoup
import re


from src.model.knowledge_information import KnowledgeInformation


class MarkdownChunking():
    
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
        
        
    def chunking_by_paragraphs(self, documents: List[KnowledgeInformation], **kwargs) -> List[Dict[str, str]]:
        chunks = []
        
        for info in documents:
            md_header_splits = self.markdown_splitter.split_text(info.page_content)
            
            for md_header_split in md_header_splits:
                headers = list(md_header_split.metadata.values())
                if 'Untitled Section' in headers:
                    continue
                if not headers:  # Skip if no headers
                    continue
                
                # Convert Markdown to HTML and extract plain text
                html = markdown(md_header_split.page_content)
                page_content = ''.join(BeautifulSoup(html, "html.parser").findAll(text=True))
                
                # Clean up text
                page_content = re.sub(r'\| --- \| --- \| --- \|', '', page_content)
                page_content = re.sub(r'\n+', '\n', page_content).strip()

                # **Drop lines with only "===" or similar patterns**
                page_content = "\n".join(
                    line for line in page_content.split("\n") if not re.match(r'^[=]+$', line)
                )
                
                # **Chunk by paragraphs** (splitting by empty lines)
                paragraphs = [p.strip() for p in page_content.split("\n") if p.strip()]
                
                # **Concatenate headers to each paragraph**
                header_text = " > ".join(headers)

                for paragraph in paragraphs:
                    chunks.append({
                        'url': info.url,
                        'headers': headers,
                        'content': f"{header_text}\n{paragraph}"  # Each paragraph as a separate chunk
                    })
        
        return chunks
    
    def chunking_by_subsection_contents(self, documents: List[KnowledgeInformation],**kwargs) -> List[Dict[str, str]]:
        chunks = []
        for info in documents:
        
            md_header_splits = self.markdown_splitter.split_text(info.page_content)
            for md_header_split in md_header_splits:
                headers = list(md_header_split.metadata.values())
                html = markdown(md_header_split.page_content)
                page_content = ''.join(BeautifulSoup(html).findAll(text=True))
                page_content = re.sub(r'\| --- \| --- \| --- \|', '', page_content)
                page_content = re.sub(r'\n+', '\n', page_content).strip()
                chunks.append({
                    'url': info.url,
                    'headers': headers,
                    'content': page_content
                })
                
        return chunks
    
    def chunking_by_sentences(self, documents: List[KnowledgeInformation],**kwargs) -> List[Dict[str, str]]:
        chunks = []
        for info in documents:
        
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
