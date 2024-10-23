from flask import Flask, request, jsonify, render_template
#from gemini_response import process_query_gemini  # Import the function from gemini_rag.py
#from llama_response import process_query_llama
from groq_response import process_query_groq

app = Flask(__name__)

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint that receives the user's query and returns the LLM response
@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('query')  # Get the query from the request
    response = process_query_groq(user_input)    # Process the query using the LLM
    return jsonify({'response': response})  # Send the response back to the user

if __name__ == '__main__':
    app.run(debug=True)
