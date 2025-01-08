import os
import logging
import traceback

from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.controller.endpoint_filter import EndpointFilter
from src.service.faiss_db import FaissDB
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



@router.get('/indexing')
@inject
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
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
   
  
   
@router.post('/searching')
@inject
async def searching(
    request: Request, 
    faiss_db: FaissDB = Depends(Provide[ApplicationContainer.faiss_db])
) -> JSONResponse:
    
    faiss_db.load_bin()
    faiss_db.load_json()
    
    try:
        info = await request.json()
        searching_info = faiss_db.searching(query=info['query'])
        
        searching_info = get_confident_context(
            searching_info=searching_info, 
            threshold=0.9
        )
        
        return JSONResponse(
            content=jsonable_encoder({
                'contexts': searching_info.contexts
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    