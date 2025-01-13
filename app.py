import os
from flask import Flask, request, render_template
from groq_response import process_query_groq
from dotenv import load_dotenv
from store_response import store_chat_response

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint that receives the user's query and returns the LLM response
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('query')          # Get the query from the request

        response_data = process_query_groq(user_input)
        model = response_data["model"]
        temperature = response_data["temperature"]
        retriever = response_data["retriever"]
        user_question = response_data["user_input"]
        context = response_data["context"]
        answer = response_data["answer"]
        
        try:
            # Store the data in MongoDB if the user has set a MongoDB URI
            if MONGO_URI and MONGO_URI != "xxxxx":
                store_chat_response(model, temperature, retriever, user_question, context, answer)
        except Exception:
            print("There was an error saving the response in MongoDB.")

        return answer

    except Exception as e:
        print(e)
        return "Error from app.py"

if __name__ == '__main__':
    app.run(debug=True)
