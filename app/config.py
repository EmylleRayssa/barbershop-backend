import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/barbershop")
JWT_SECRET = os.getenv("JWT_SECRET", "meusecretjwt")
JWT_ALGORITHM = "HS256"
