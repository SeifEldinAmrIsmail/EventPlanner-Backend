import os
from dotenv import load_dotenv

load_dotenv()

#MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin123@mongo:27017/eventplanner")
DB_NAME = os.getenv("DB_NAME", "eventplanner")

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_change_me")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
