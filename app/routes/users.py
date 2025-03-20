from fastapi import APIRouter, HTTPException
from app.database import db
from app.security import hash_password, verify_password, create_jwt
from app.models import User

router = APIRouter()

@router.post("/register")
async def register(user: User):
    existing_user = await db.users.find_one({"whatsapp": user.whatsapp})  # 🔹 Agora verifica pelo WhatsApp
    if existing_user:
        raise HTTPException(status_code=400, detail="WhatsApp já registrado")

    user.password = hash_password(user.password)
    new_user = await db.users.insert_one(user.dict())
    return {"message": "Usuário registrado com sucesso"}

@router.post("/login")
async def login(user: User):
    existing_user = await db.users.find_one({"whatsapp": user.whatsapp})  # 🔹 Login por WhatsApp
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_jwt(existing_user["whatsapp"])  # 🔹 Token gerado com base no WhatsApp
    return {"access_token": token}
