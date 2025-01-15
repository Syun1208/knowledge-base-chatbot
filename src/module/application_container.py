from dependency_injector import containers, providers
from thespian.actors import ActorSystem
from langchain_text_splitters import MarkdownHeaderTextSplitter


from src.utils.logger import Logger
from src.service.interface.llm import LLM
from src.service.interface.web_crawler import WebCrawler
from src.service.interface.data_loader import DataLoader
from src.service.interface.vector_database import VectorDatabase
from src.service.implement.halong_embedding import HaLongEmbedding
from src.service.implement.html_loader import HTMLLoader
from src.service.implement.ollama import Ollama
from src.service.implement.faiss_db import FaissDB
from src.service.interface.chunking import Chunking
from src.service.implement.markdown_chunking import MarkdownChunking
from src.service.implement.google_crawler import GoogleCrawler
from src.utils.constants import HEADERS_TO_SPLIT_ON


class ApplicationContainer(containers.DeclarativeContainer):
    # set up to get config
    wiring_config = containers.WiringConfiguration(modules=["src.controller.endpoint"])
    
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)
    
    logger = providers.Singleton(
        providers.Singleton(
            Logger,
            log_dir=config.logger.log_dir,
            log_clear_days=config.logger.log_clear_days
        )

    )
    
    halong_embedding = providers.AbstractSingleton(LLM)
    halong_embedding.override(
        providers.Singleton(
            HaLongEmbedding,
            model_id=config.huggingface.model_embedding
        )

    )
    
    markdown_splitter = providers.Singleton(
        MarkdownHeaderTextSplitter,
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False
    )
    
    html_loader = providers.AbstractSingleton(DataLoader)
    html_loader.override(
        providers.Singleton(
            HTMLLoader,
            markdown_splitter=markdown_splitter            
        )

    )
    
    markdown_chunking = providers.AbstractSingleton(Chunking)
    markdown_chunking.override(
        providers.Singleton(
            MarkdownChunking
        )
    )
    
    google_crawler = providers.AbstractSingleton(WebCrawler)
    google_crawler.override(
        providers.Singleton(
            GoogleCrawler, 
            markdown_splitter=markdown_splitter 
        )
    )
    
    llama2 = providers.AbstractSingleton(LLM)
    llama2.override(
        providers.Singleton(
            Ollama
        )
    )
    
    faiss_db = providers.AbstractSingleton(VectorDatabase)
    faiss_db.override(
        providers.Singleton(
            FaissDB,
            model_embedding=halong_embedding,
            model_dim=config.huggingface.model_dim,
            document_loader=html_loader,
            web_crawler=google_crawler,
            chunking=markdown_chunking,
            logger=logger,
            path_loads=config.knowledge_base.url,
            path_save_documents=config.knowledge_base.path_save_documents,
            path_save_db=config.vector_db.path_save_db,
            top_k=config.vector_db.top_k,
            show_time_compute=config.timer.show_time_compute
        )
    )
    
    # prompter = providers.Singleton(PromptTemplate)
    
    # naive_rag = providers.AbstractSingleton(RAG)
    # naive_rag.override(
    #     providers.Singleton(
    #         NaiveRAG,
    #         llm=llama2,
    #         vector_db=faiss_db,
    #         prompter=prompter,
    #         template=config.prompter.template
    #     )
    # )