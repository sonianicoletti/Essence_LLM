# huggingface-cli login

import signal
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
from main.alternative_strategies.context_retrieval_similarity_search import generate_rag_prompt, get_relevant_context_from_db

# Constants
GENERATIVE_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
TEMPERATURE = 1.0 

def signal_handler(sig, frame):
    print('\nThank you for using Essence Coach :)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Load the Llama model and tokenizer from Hugging Face
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(GENERATIVE_MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(GENERATIVE_MODEL_NAME).to(device)

def generate_answer(prompt):
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate response using the model
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=2048,  # Adjust the maximum length according to the model's capability
            temperature=TEMPERATURE,
            do_sample=True,  # Enables sampling, which introduces creativity based on temperature
            top_p=0.95,  # Top-p sampling (nucleus sampling)
            top_k=50,    # Top-k sampling
        )
    
    # Decode the generated tokens to text
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def process_query_llama(user_input):
    context = get_relevant_context_from_db(user_input) 
    prompt = generate_rag_prompt(query=user_input, context=context)
    answer = generate_answer(prompt=prompt)
    
    print("************************ PROMPT: ************************\n" + prompt + "\n*********************************************************\n")
    print("************************ ANSWER: ************************\n" + answer + "\n*********************************************************\n")
    
    return answer

while True:
    print("-------------------------------------------------------------")
    print("What would you like to ask?")
    query = input("Query: ") 
    context = get_relevant_context_from_db(query)  
    prompt = generate_rag_prompt(query=query, context=context)
    answer = generate_answer(prompt=prompt)
    print("CONTEXT: " + context)
    print("ANSWER: " + answer)