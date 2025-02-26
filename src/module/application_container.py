from dependency_injector import containers, providers
from thespian.actors import ActorSystem


from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.repository.DataAccess.data_access_connection import BaseRepository
from src.repository.DataAccess.data_access_connection import WasaAiMl

from src.service.interface.kcb_supporter.data_crawler import DataCrawler 
from src.service.interface.kcb_supporter.data_chunker import DataChunker
from src.service.interface.kcb_supporter.model_embedding import ModelEmbedding
from src.service.interface.kcb_service.kcb_service import KCBService
from src.service.interface.kcb_service.kcb_db_service import DataService


from src.service.implement.kcb_supporter_impl.kcb_data_crawler_impl import KCBDataCrawlerImpl
from src.service.implement.kcb_supporter_impl.kcb_data_chunker_impl import KCBDataChunkerImpl
from src.service.implement.kcb_supporter_impl.kcb_model_embedding_impl import KCBModelEmbeddingImpl
from src.service.implement.kcb_service_impl.kcb_service_impl import KCBServiceImpl
from src.service.implement.kcb_service_impl.kcb_db_service_impl import KCBDataServiceImpl

from src.utils.constants import HEADERS_TO_SPLIT_ON
from src.utils.logger import Logger, LoggerImpl

class ApplicationContainer(containers.DeclarativeContainer):
    # set up to get config 
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)

    wasa_aiml_connector = providers.AbstractSingleton(BaseRepository)
    wasa_aiml_connector.override(
        providers.Singleton(
            WasaAiMl,
            database_name=config.db.aiml_mysql.database_name,
            username=config.db.aiml_mysql.username,
            password=config.db.aiml_mysql.password,
            host=config.db.aiml_mysql.host,
            port=config.db.aiml_mysql.port,
            dbms_name=config.db.aiml_mysql.dbms_name,
        )
    )



    markdown_splitter = providers.Singleton(
        MarkdownHeaderTextSplitter,
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False
    )
    
    logger = providers.AbstractSingleton(Logger)
    logger.override(
        providers.Singleton(
            LoggerImpl,
            logger_config = config.logger
        )
    )


    data_crawler = providers.AbstractSingleton(DataCrawler)
    data_crawler.override(
        providers.Singleton(
            KCBDataCrawlerImpl,
            markdown_splitter = markdown_splitter
        )
    )

    data_chunker = providers.AbstractSingleton(DataChunker)
    data_chunker.override(
        providers.Singleton(
            KCBDataChunkerImpl,
            chunking_config = config.chunking_config,
            logger = logger
        )
    )

    model_embedding = providers.AbstractSingleton(ModelEmbedding)
    model_embedding.override(
        providers.Singleton(
            KCBModelEmbeddingImpl,
            model_embedding_config = config.model_embedding_config,
            logger = logger
        )
    )

    kcb_data_service = providers.AbstractSingleton(DataService)
    kcb_data_service.override(
        providers.Singleton(
            KCBDataServiceImpl,
            service_id=config.default.service_id,
            wasa_aiml_connector=wasa_aiml_connector
        )
    )


    kcb_service = providers.AbstractSingleton(KCBService)
    kcb_service.override(
        providers.Singleton(
            KCBServiceImpl,
            data_crawler = data_crawler,
            data_chunker = data_chunker,
            model_embedding = model_embedding,
            knowledge_config = config.knowledge_base,
            vector_db_config = config.vector_db
        )
    )
