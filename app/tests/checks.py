from pymongo import MongoClient

# 🔹 Configuração: Altere a URI para se conectar ao MongoDB local ou no Docker
MONGO_URI = "mongodb://localhost:27017"  # Se o MongoDB estiver rodando localmente
# MONGO_URI = "mongodb://mongo:27017"  # Se estiver rodando via Docker

# 🔹 Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client["agendamentos"]  # Nome do banco de dados

# 🔹 Função para testar a conexão e listar dados
def test_mongo():
    print("🔹 Conectando ao MongoDB...")

    # Verificar se a conexão foi estabelecida
    print("🔹 Bancos disponíveis:", client.list_database_names())

    # Testar busca de um barbeiro pelo nome
    barber_name = "Felipe"  # 🔹 Troque pelo nome de um barbeiro cadastrado
    barber = db.barbers.find_one({"name": barber_name})

    print("\n🔹 Barbeiro encontrado:")
    print(barber)


    print("\n🔹 Agendamentos:")
    bookings = db.bookings.find().limit(5)

    date='2025-03-21'
    time='12:00'
    booked_slots = db.bookings.find_one({
        "barber_id": barber_name,
        "date": date,
        "time": time
    })

    print(booked_slots)

    
    # for booking in bookings:
    #     print(booking)

    # # Testar busca de serviços cadastrados
    # services = db.services.find().limit(5)
    # print("\n🔹 Serviços cadastrados:")
    # for service in services:
    #     print(service)

    # # Testar busca de horários agendados
    # date = "2024-04-20"  # 🔹 Troque por uma data válida no formato YYYY-MM-DD
    # booked_slots = db.appointments.find({"date": date}).limit(5)

    # print("\n🔹 Agendamentos para", date)
    # for slot in booked_slots:
    #     print(slot)

# 🔹 Executar os testes
if __name__ == "__main__":
    test_mongo()
