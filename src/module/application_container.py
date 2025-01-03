from dependency_injector import containers, providers
from thespian.actors import ActorSystem
from langchain.prompts import PromptTemplate


from src.utils.logger import Logger
from src.interface.llm import LLM
from src.interface.rag import RAG
from src.interface.data_loader import DataLoader
from src.interface.vector_database import VectorDatabase
from src.service.halong_embedding import HaLongEmbedding
from src.service.html_loader import HTMLLoader
from src.service.ollama import Ollama
from src.service.faiss_db import FaissDB
from src.service.naive_rag import NaiveRAG


class ApplicationContainer(containers.DeclarativeContainer):
    # set up to get config
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)
    
    logger = providers.Singleton(
        Logger,
        log_dir=config.logger.log_dir,
        log_clear_days=config.logger.log_clear_days
    )
    
    halong_embedding = providers.AbstractSingleton(LLM)
    halong_embedding.override(
        HaLongEmbedding,
        model_id=config.huggingface.model_embedding
    )
    
    html_loader = providers.AbstractSingleton(DataLoader)
    html_loader.override(
        HTMLLoader
    )
    
    llama2 = providers.AbstractSingleton(LLM)
    llama2.override(
        Ollama
    )
    
    faiss_db = providers.AbstractSingleton(VectorDatabase)
    faiss_db.override(
        FaissDB,
        model_embedding=halong_embedding,
        model_dim=config.hugging_face.model_dim,
        document_loader=html_loader,
        logger=logger,
        path_loads=config.knowledge_base.url,
        path_save_documents=config.knowledge_base.path_save_documents,
        path_save_db=config.vector_db.path_save_db,
        chunk_size=config.knowledge_base.chunk_size,
        chunk_overlap=config.knowledge_base.chunk_overlap,
        show_time_compute=config.timer.show_time_compute
    )
    
    prompter = providers.Singleton(PromptTemplate)
    
    naive_rag = providers.AbstractSingleton(RAG)
    naive_rag.override(
        NaiveRAG,
        llm=llama2,
        vector_db=faiss_db,
        prompter=prompter,
        template=config.prompter.template
    )