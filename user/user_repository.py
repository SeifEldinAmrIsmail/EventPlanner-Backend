from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from db.mongo import users_collection

def create_user(email: str, password_hash: str):

    doc = {
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow()
    }

    try:
        result = users_collection.insert_one(doc)
        return {
            "_id": str(result.inserted_id),
            "email": email
        }
    except DuplicateKeyError:
        return None

def find_user_by_email(email: str):

    user = users_collection.find_one({"email": email})
    if not user:
        return None
    user["_id"] = str(user["_id"])
    return user

def find_user_by_id(user_id: str):

    u = users_collection.find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    u["_id"] = str(u["_id"])
    return u
