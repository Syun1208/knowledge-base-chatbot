import os
import logging
import faiss
import traceback

from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.controller.endpoint_filter import EndpointFilter
from src.service.faiss_db import FaissDB
from src.model.knowledge_info import KnowledgeInfo
from src.utils.utils import get_confident_context
from src.module.application_container import ApplicationContainer

# uvicorn_logger = logging.getLogger("uvicorn.access")
# uvicorn_logger.addFilter(EndpointFilter(path="/"))


router = APIRouter()
   
@router.get('/')
async def health_check() -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({
            'message': 'OK', 
            'status_code': 200}), 
            status_code=200
        )



@router.get('/indexing/knowledge')
@inject
async def indexing_knowledge(
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:

    try:
        cpu_index = faiss.IndexFlatIP(faiss_db.model_dim)
        
        documents = faiss_db.document_loader.load(faiss_db.path_loads)
        faiss_db.indexing(
            cpu_index=cpu_index,
            documents=documents
        )
        
        return JSONResponse(
            content=jsonable_encoder({
            'message': 'Update new informations into vector database successfully'
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))



@router.post('/indexing/web')
@inject
async def indexing_web(
    request: Request,
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:

    try:
        info = await request.json()
        
        cpu_index = faiss.IndexFlatIP(faiss_db.model_dim)
    
        documents = faiss_db.web_crawler.crawl(query=info['query'])
        old_documents = faiss_db.load_json()
        old_documents = [
            KnowledgeInfo(
                url=old_document['url'],
                page_content=old_document['content']
            ) for old_document in old_documents
        ]
        documents = old_documents + documents
        faiss_db.indexing(
            cpu_index=cpu_index,
            documents=documents
        )
        
        return JSONResponse(
            content=jsonable_encoder({
            'message': 'Update new informations into vector database successfully'
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
  
  
   
@router.post('/searching')
@inject
async def searching(
    request: Request, 
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:
    
    cpu_index = faiss_db.load_bin()
    documents = faiss_db.load_json()
    
    try:
        info = await request.json()
        searching_info = faiss_db.searching(
            cpu_index=cpu_index,
            documents=documents,
            query=info['query']
        )
        
        searching_info = get_confident_context(
            searching_info=searching_info, 
            threshold=0.9
        )
        
        return JSONResponse(
            content=jsonable_encoder({
                'urls': searching_info.urls,
                'contexts': searching_info.contexts
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    