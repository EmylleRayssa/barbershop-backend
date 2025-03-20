from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .utils import generate_available_times

# Modelo de Usuário (Login e Cadastro)
class User(BaseModel):
    username: str
    whatsapp: str  # 🔹 Agora o WhatsApp é a chave única
    password: str
    email: Optional[str] = None  # 🔹 Email agora é opcional

# Modelo de Barbeiro
class Barber(BaseModel):
    name: str  # Nome do barbeiro
    whatsapp: str  # WhatsApp para contato
    available_times: List[str] = generate_available_times()  # Horários padrão de 30 em 30 min

    class Config:
        orm_mode = True

# Modelo de Serviço (Cortes, Barba, etc.)
class Service(BaseModel):
    name: str
    price: float
    duration: int  # Duração em minutos
    image: Optional[str] = None

# Modelo de Agendamento
class Booking(BaseModel):
    customer_name: str  # Nome do cliente
    customer_whatsapp: str  # WhatsApp do cliente
    barber_id: str  # ID do barbeiro
    service: str  # Serviço escolhido
    date: str  # Data do agendamento (YYYY-MM-DD)
    time: str  # Horário do agendamento (HH:MM)
    status: Optional[str] = "Pendente"  # Status do agendamento

    class Config:
        orm_mode = True