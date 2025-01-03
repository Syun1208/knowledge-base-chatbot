import os
import sys
import uvicorn
import warnings
import logging
from multiprocessing import Pool

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependency_injector.wiring import inject
from src.module.application_container import ApplicationContainer
from src.controller.endpoint import router
from src.utils.utils import load_yaml



@inject
def create_app(env: str) -> FastAPI:
    
    config = load_yaml(f"config/{env}.yml")

    app = FastAPI(
        title=f"{config['default']['app_name']} | {config['default']['env']}", 
        description="""<h2>Made by Leon</h2>"""
    )
    
    application_container = ApplicationContainer()
    application_container.wire(modules=["src.module.application_container"])

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    env = os.environ['APP_MODE']

    application_container.config.from_yaml(f"config/{env}.yml")
    app.container = application_container
    app.include_router(router)

    logging.info("Wire completed")
    logging.basicConfig(level=logging.INFO)

    return app


app = create_app(env=os.environ['APP_MODE'])

if __name__ == "__main__":    
    uvicorn.run(
        app='main:app', 
        host='0.0.0.0', 
        port=5000, 
        reload=True, 
        workers=psutil.cpu_count(logical=False), 
        timeout_keep_alive=60 * 60 * 2
    )


