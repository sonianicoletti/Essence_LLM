import os
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Set up MongoDB client and database
client = pymongo.MongoClient(MONGO_URI)
db = client["chatbot_db"]
collection = db["chats"]

def store_chat_response(model, temperature, retriever, user_question, context, answer):
    # Store the user's question, the retrieved context, and the assistant's answer in MongoDB.
    chat_data = {
        "model": model,
        "temperature": temperature,
        "retriever": retriever,
        "user_question": user_question,
        "context": context,
        "answer": answer
    }
    collection.insert_one(chat_data)
    print("Chat data stored in MongoDB:", chat_data)
