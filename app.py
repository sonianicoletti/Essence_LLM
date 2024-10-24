from flask import Flask, request, render_template
from groq_response import process_query_groq

app = Flask(__name__)

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint that receives the user's query and returns the LLM response
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('query')       # Get the query from the request
        response = process_query_groq(user_input)    # Process the query using the chosen LLM
        return response
    except Exception as e:
        return "Error from app.py"

if __name__ == '__main__':
    app.run(debug=True)
