import os
import sys
import shutil
import time

from dependency_injector.wiring import Provide, inject
from flask import Flask
from py_profiler.profiler_controller import profiler_blueprint
from waitress import serve
from src.module.application_container import ApplicationContainer
from src.service.interface.kcb_service.kcb_service import KCBService
from src.controller import kcb_controller
import warnings
warnings.filterwarnings('ignore')

import logging

def setup_di_modules(environment: str):
    modules = [
        sys.modules[__name__],
        kcb_controller
    ]
    logging.info(f"Mode: {environment}")
    logging.info(f"Loaded config: config/{environment}.yml")
    logging.info(f"Modules: {modules}")
    application_container = ApplicationContainer()
    application_container.config.from_yaml(f"config/{environment}.yml")
    application_container.config.from_yaml(f"config/chunking_config.yml")
    application_container.config.from_yaml(f"config/model_embedding_config.yml")
    application_container.wire(modules)
    logging.info("Wire completed")

inject
def run(

        kcb_service: KCBService = Provide[ApplicationContainer.kcb_service]
):
    kcb_service.run()



if __name__ == "__main__":
    os.environ['APP_MODE'] = sys.argv[1] if len(sys.argv) > 1 else 'development'
    setup_di_modules(os.environ['APP_MODE'])
    run()
    

