import os
from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

from groq_response import process_query_groq
from store_response import store_chat_response

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['chatbot']
users_collection = db['users']

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template(
            'index.html',
            email=session.get('email'),
            role=session.get('role')
        )
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    role = data['role']

    if users_collection.find_one({'email': email}):
        return "Email already exists", 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        'email': email,
        'password': hashed_pw,
        'role': role
    })

    return "Registered successfully", 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = users_collection.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['user_id'] = str(user['_id'])
        session['role'] = user['role']
        session['email'] = user['email']
        return "Logged in", 200
    return "Invalid email or password", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return "Unauthorised", 401

    try:
        user_input = request.json.get('query')
        role = session.get('role', 'unknown')
        event = request.json.get('event')

        response_data = process_query_groq(user_input)
        model = response_data["model"]
        temperature = response_data["temperature"]
        retriever = response_data["retriever"]
        user_question = response_data["user_input"]
        context = response_data["context"]
        answer = response_data["answer"]

        if MONGO_URI and MONGO_URI != "xxxxx":
            store_chat_response(
                user_question=user_question,
                contexts=context,
                answer=answer,
                event=event
            )
        return answer

    except Exception as e:
        print(e)
        return "Error from app.py", 500

if __name__ == '__main__':
    app.run(debug=True)
