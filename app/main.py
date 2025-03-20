from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, services, bookings, barbers  # 🔹 Adicionando barbeiros

app = FastAPI(title="API de Agendamento")

# 🔹 Permite chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 Modifique para ["http://localhost:5173"] no ambiente de produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users")
app.include_router(services.router, prefix="/services")
app.include_router(bookings.router, prefix="/bookings")
app.include_router(barbers.router, prefix="/barbers")  # 🔹 Nova rota

@app.get("/")
async def home():
    return {"message": "API de Agendamento Rodando!"}
