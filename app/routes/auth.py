from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import timedelta
# from core.security import create_access_token, verify_password  # Funções auxiliares para JWT e senha
from db import db  # Conexão com o MongoDB
from datetime import datetime, timedelta
import jwt

router = APIRouter()

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta para JWT
SECRET_KEY = "SUA_CHAVE_SECRETA"  # 🔹 Mude para algo seguro!
ALGORITHM = "HS256"

class AdminLogin(BaseModel):
    whatsapp: str   
    password: str

# Endpoint para login
@router.post("/auth/login")
async def login(data: dict):
    whatsapp = data.get("whatsapp")
    password = data.get("password")


    print("whatsapp: ", whatsapp)
    print("password: ", password)

    # Buscar admin no banco
    admin = db.admins.find_one({"whatsapp": whatsapp})
    if not admin:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    # Verificar senha
    if not pwd_context.verify(password, admin["password"]):
        raise HTTPException(status_code=400, detail="Senha incorreta.")

    # Criar token JWT
    token_data = {"sub": whatsapp, "exp": datetime.utcnow() + timedelta(hours=2)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"token": token}

# @router.post("/admin/login")
# async def admin_login(data: AdminLogin):

#     print(">>>>>>> ", data)

#     admin = await db.admins.find_one({"whatsapp": data.whatsapp})

#     print(">>>>>>> ", admin)

#     if not admin or not verify_password(data.password, admin["password"]):
#         raise HTTPException(status_code=401, detail="Credenciais inválidas")

#     access_token = create_access_token(data={"sub": admin["whatsapp"]}, expires_delta=timedelta(days=1))
#     return {"access_token": access_token, "token_type": "bearer"}
