from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Barber
from typing import List

router = APIRouter()

# 🔹 Cadastrar um novo barbeiro (gerando horários automaticamente)
@router.post("/barbers", response_model=dict)
async def create_barber(barber: Barber):
    existing_barber = await db.barbers.find_one({"whatsapp": barber.whatsapp})
    if existing_barber:
        raise HTTPException(status_code=400, detail="Barbeiro já cadastrado com este WhatsApp.")

    # Garante que os horários sempre sejam gerados corretamente
    barber.available_times = Barber().available_times

    await db.barbers.insert_one(barber.dict())
    return {"message": "Barbeiro cadastrado com sucesso!"}

# 🔹 Listar todos os barbeiros
@router.get("/barbers", response_model=List[Barber])
async def get_barbers():
    barbers = await db.barbers.find().to_list(100)
    return barbers

# 🔹 Buscar barbeiro pelo ID
@router.get("/barbers/{barber_id}", response_model=Barber)
async def get_barber_by_id(barber_id: str):
    barber = await db.barbers.find_one({"_id": barber_id})
    if not barber:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    return barber

# 🔹 Atualizar informações de um barbeiro
@router.put("/barbers/{barber_id}", response_model=dict)
async def update_barber(barber_id: str, updated_data: Barber):
    updated_barber = await db.barbers.update_one({"_id": barber_id}, {"$set": updated_data.dict()})
    if updated_barber.modified_count == 0:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado ou dados iguais.")
    return {"message": "Barbeiro atualizado com sucesso!"}

# 🔹 Remover um barbeiro
@router.delete("/barbers/{barber_id}", response_model=dict)
async def delete_barber(barber_id: str):
    deleted_barber = await db.barbers.delete_one({"_id": barber_id})
    if deleted_barber.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    return {"message": "Barbeiro removido com sucesso!"}
