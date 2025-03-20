import jwt
import bcrypt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM

# Função para criar JWT com WhatsApp
def create_jwt(whatsapp: str):
    expiration = datetime.utcnow() + timedelta(days=1)
    payload = {"sub": whatsapp, "exp": expiration}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Funções para hash de senha
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
