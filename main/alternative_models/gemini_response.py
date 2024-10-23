import os
import signal
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from context_retrieval import generate_rag_prompt, get_relevant_context_from_db

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GENERATIVE_MODEL_NAME = "gemini-1.5-pro"
# gemini-1.0-pro: 30k + 2k = 32k tokens context window
# gemini-1.5-pro: input 2M, output 8k tokens (5600 words)
TEMPERATURE = 1.0 # from 0.0 to 2.0: lower -> less creative, higher -> more creative

def signal_handler(sig, frame):
    print('\nThank you for using Essence Coach :)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_answer(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name=GENERATIVE_MODEL_NAME)
    answer = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=8000,
        temperature=TEMPERATURE,
    ),)
    return answer.text

def process_query_gemini(user_input):
    context = get_relevant_context_from_db(user_input) 
    prompt = generate_rag_prompt(query=user_input, context=context)
    answer = generate_answer(prompt=prompt)
    print("************************ PROMPT: ************************\n" + prompt + "\n*********************************************************\n")
    print("************************ ANSWER: ************************\n" + answer + "\n*********************************************************\n")
    return answer

""" while True:
    print("-------------------------------------------------------------")
    print("What would you like to ask?")
    query = input("Query: ") 
    context = get_relevant_context_from_db(query)  
    prompt = generate_rag_prompt(query=query, context=context)
    answer = generate_answer(prompt=prompt)
    print("CONTEXT: " + context)
    print("ANSWER: " + answer) """
