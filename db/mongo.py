from pymongo import MongoClient
from core.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db["users"]

users_collection.create_index("email", unique=True)

events_collection = db["events"]

# Helpful indexes (not mandatory but good)
events_collection.create_index("organizer_id")
events_collection.create_index("date")
events_collection.create_index("attendees.user_id")