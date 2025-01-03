import os
import logging


from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.controller.endpoint_filter import EndpointFilter
from src.service.faiss_db import FaissDB
from src.module.application_container import ApplicationContainer

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(path="/"))


router = APIRouter()
   
@router.get('/')
async def health_check() -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({
            'message': 'OK', 
            'status_code': 200}), 
            status_code=200
        )



@router.get('/indexing')
async def indexing(
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:

    try:
        faiss_db.indexing()
        
        return JSONResponse(
            content=jsonable_encoder({
            'message': 'Update new informations into vector database successfully'
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))
   
  
   
@router.get('/searching')
async def chat(
    request: Request, 
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:
    
    try:
        info = await request.json()
        searching_info = faiss_db.searching(query=info['query'])
        
        return JSONResponse(
            content=jsonable_encoder({
                'contexts': searching_info.contexts
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))
    