import os
import logging
import faiss
import traceback
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.controller.kcb_endpoint_filter import EndpointFilter
from src.service.interface.kcb_service.kcb_service import KCBService
from src.service.interface.kcb_service.kcb_db_service import DataService
from src.utils.utils import get_confident_context
from src.module.application_container import ApplicationContainer




kcb_router = APIRouter()
   
@kcb_router.get('/')
async def health_check() -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({
            'message': 'OK', 
            'status_code': 200}), 
            status_code=200
        )

@kcb_router.get('/indexing/knowledge')
@inject
async def indexing_knowledge(
    request: Request,
    kcb_service: KCBService = Depends(Provide[ApplicationContainer.kcb_service])
) -> JSONResponse:
    try:
        params = await request.json()
        kcb_service.indexing_knowledge(chunking_approach_id = params['chunking_approach_id'], model_embedding_approach_id = params['model_embedding_approach_id'])
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Update new informations into vector database successfully'
            }),
            status_code=200
        )
        
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))



@kcb_router.post('/indexing/web')
@inject
async def indexing_web(
    request: Request,
    kcb_service: KCBService = Depends(Provide[ApplicationContainer.kcb_service])
) -> JSONResponse:

    try:
        params = await request.json()
        kcb_service.indexing_web(urls = params['urls'], 
                                chunking_approach_id = params['chunking_approach_id'], 
                                model_embedding_approach_id = params['model_embedding_approach_id'])
        
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
  
  
   
@kcb_router.post('/searching')
@inject
async def searching(
    request: Request,
    kcb_service: KCBService = Depends(Provide[ApplicationContainer.kcb_service])
) -> JSONResponse:
    
    try:
        params = await request.json()
        searching_results = kcb_service.searching(params['query'], params['model_embedding_approach_id'])
        #print(searching_results)

        return JSONResponse(
            content=jsonable_encoder({
                'urls': searching_results.urls,
                'contexts': searching_results.contexts
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@kcb_router.get('/experiment')
@inject
async def searching(
    kcb_service: KCBService = Depends(Provide[ApplicationContainer.kcb_service])
) -> JSONResponse:
    
    try:
        response = kcb_service.run()
        #print(searching_results)

        return JSONResponse(
            content=jsonable_encoder({
                'urls': response.urls,
                'contexts': response.contexts
            }),
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@kcb_router.get('/insert_feedback')
@inject
async def searching(
    request: Request,
    kcb_data_service: DataService = Depends(Provide[ApplicationContainer.kcb_data_service])
) -> JSONResponse:
    
    try:
        params = await request.json()
        kcb_data_service.insert_feedback(question = params['question'],
                                         answer = params['answer'],
                                         feedback = params['feedback'])

        return JSONResponse(
            content= "Insert feedback successfully",
            status_code=200
        )
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@kcb_router.post('/get_feedback')
@inject
async def searching(
    request: Request,
    kcb_data_service: DataService = Depends(Provide[ApplicationContainer.kcb_data_service])
) -> JSONResponse:
    
    try:
        response = kcb_data_service.get_feedback()
        response_json = response.to_json(orient="records")
        return JSONResponse(content=response_json, status_code=200)
        
    except Exception as e:
        # If any exception occurs, raise an HTTP 500 Internal Server Error
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
