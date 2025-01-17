from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from thespian.actors import ActorSystem
from src.service.interface.kcb_service.kcb_service import KCBService
from src.module.application_container import ApplicationContainer

kcb_blueprint = Blueprint("chatbot", __name__)

@kcb_blueprint.route("/chatbot", methods=["POST"])
@inject
def chatbot(
        kcb_service: KCBService = Provide[ApplicationContainer.kcb_service]
):
    return True

