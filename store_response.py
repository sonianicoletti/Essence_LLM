import os
import pymongo
from dotenv import load_dotenv
from datetime import datetime
from flask import session

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Set up MongoDB client and database
client = pymongo.MongoClient(MONGO_URI)
db = client["chatbot"]
collection = db["messages"]

def store_chat_response(user_question, contexts, answer, event):

    user_email = session.get("email") or "guest@example.com"
    user_role = session.get("role") or "Guest"

    chat_data = {
        "user_question": user_question,
        "contexts": contexts if isinstance(contexts, list) else [contexts],  # Ensure it's a list
        "answer": answer,
        "user_email": user_email,
        "user_role": user_role,
        "event": event,
        "timestamp": datetime.utcnow()
    }

    collection.insert_one(chat_data)
    # print("Chat data stored in MongoDB:", chat_data)
