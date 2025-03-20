from pymongo import MongoClient
from passlib.context import CryptContext

# 🔹 Conexão com o MongoDB (substitua pela sua URL do Mongo se necessário)
MONGO_URI = "mongodb://mongo:lgRNTOxptmDhURNKzWXSsyWDmZzHjVwD@yamanote.proxy.rlwy.net:51370"  # Caso esteja rodando localmente
DB_NAME = "barbershop"  # Nome do seu banco de dados

# Criando conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# 🔹 Criar o hash da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

# 🔹 Dados do Administrador
admin_data = {
    "whatsapp": "55981295683",  # Substitua pelo número do admin
    "password": hash_password("admin123"),  # Substitua pela senha desejada
}

# 🔹 Inserir Admin no Banco
def add_admin():
    existing_admin = db.admins.find_one({"whatsapp": admin_data["whatsapp"]})
    if existing_admin:
        print("❌ Admin já cadastrado!")
    else:
        db.admins.insert_one(admin_data)
        print("✅ Admin cadastrado com sucesso!")

# Executar a função
if __name__ == "__main__":
    add_admin()
