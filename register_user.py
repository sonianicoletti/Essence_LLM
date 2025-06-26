import os
import pymongo
import bcrypt
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Set up MongoDB client and database
client = pymongo.MongoClient(MONGO_URI)
db = client["chatbot"]
users_collection = db["users"]

def register_user(email, password, role):
    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return False

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user document
    user_data = {
        "email": email,
        "password": hashed_password,
        "role": role,
        "registration_time": datetime.utcnow()
    }

    # Insert user into the database
    users_collection.insert_one(user_data)
    print("New user registered:", email)
    return True
