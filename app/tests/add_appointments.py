from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# 🔗 Conexão com o MongoDB
client = MongoClient("mongodb://mongo:lgRNTOxptmDhURNKzWXSsyWDmZzHjVwD@yamanote.proxy.rlwy.net:51370")  # ou sua URL do Railway
db = client["barbershop"]
appointments = db["bookings"]

# 🔧 Dados de exemplo
barbers = ["Felipe", "Pedro", "Gustavo"]
services = [
    "Corte degradê na 0",
    "Corte com tesoura",
    "Barba",
    "Corte + Barba",
    "Alisamento"
]
times = ["09:00", "09:30", "10:00", "10:30", "11:00", "14:00", "14:30", "15:00", "15:30", "16:00"]

# 📅 Gera agendamentos em fevereiro de 2025
start_date = datetime(2025, 2, 1)
end_date = datetime(2025, 2, 28)
delta = timedelta(days=1)

current_date = start_date
inserted = 0

while current_date <= end_date:
    # Gera de 2 a 5 agendamentos por dia
    for _ in range(random.randint(2, 5)):
        appointment = {
            "customer_name": f"Cliente {random.randint(1, 100)}",
            "customer_whatsapp": f"55981{random.randint(100000, 999999)}",
            "barber_id": random.choice(barbers),
            "service": random.choice(services),
            "date": current_date.strftime("%Y-%m-%d"),
            "time": random.choice(times),
        }
        appointments.insert_one(appointment)
        inserted += 1

    current_date += delta

print(f"✅ Inseridos {inserted} agendamentos no mês de fevereiro.")
