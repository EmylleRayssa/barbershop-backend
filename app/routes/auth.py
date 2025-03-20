from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
from core.security import create_access_token, verify_password  # Funções auxiliares para JWT e senha
from db import db  # Conexão com o MongoDB

router = APIRouter()

class AdminLogin(BaseModel):
    whatsapp: str   
    password: str

@router.post("/admin/login")
async def admin_login(data: AdminLogin):
    admin = await db.admins.find_one({"whatsapp": data.whatsapp})
    if not admin or not verify_password(data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": admin["whatsapp"]}, expires_delta=timedelta(days=1))
    return {"access_token": access_token, "token_type": "bearer"}
