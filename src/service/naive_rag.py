from langchain_core.prompts.string import StringPromptTemplate
from typing import List

from src.interface.vector_database import VectorDatabase
from src.interface.llm import LLM
from src.interface.rag import RAG

class NaiveRAG(RAG):
    
    def __init__(
        self,
        llm: LLM,
        vector_db: VectorDatabase,
        prompter: StringPromptTemplate,
        template: str
    ):
        self.vector_db = vector_db
        self.prompter = prompter
        self.llm = llm
        self.template = template
        self.conversations = []

        
    def invoke(self, query: str) -> None:
        
        self.vector_db.load_bin()
        self.vector_db.load_json()
        
        searching_info = self.vector_db.searching(
            query=query
        )
        
        context = searching_info.texts
        
        prompt_template = self.prompter.from_template(
            self.template
        )
        prompt = prompt_template.format(
            query=query,
            context=context
        )
        
        response = self.llm.generate(
            prompt=prompt,
            conversation=self.conversations
        )
        
        self.conversations = response['context']
        
        return response['response']
        
        
        
        