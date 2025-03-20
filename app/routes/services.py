from fastapi import APIRouter, Depends
from app.database import db
from typing import List
from app.models import Service


router = APIRouter()

@router.get("/services")
async def get_services():
    services_cursor = db.services.find({})  # Obtém os serviços (cursor assíncrono)
    services = await services_cursor.to_list(length=100)  # Converte para lista

    for service in services:
        service["id"] = str(service["_id"])  # Converte ObjectId para string
        service.pop('_id', None)

    return services

@router.post("/services")
async def create_service(service: Service):
    new_service = await db.services.insert_one(service.dict())
    return {"message": "Serviço cadastrado"}
