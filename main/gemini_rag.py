import os
import signal
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
K = 3 # number of results you need to retrieve (each result is an embedding) 
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" 
GENERATIVE_MODEL_NAME = "gemini-1.5-pro"
# 1 token = +-4 characters
# 100 token = 70 English words
# gemini-1.0-pro: 30k + 2k = 32k tokens context window
# gemini-1.5-pro: input 2M, output 8k tokens (5600 words)
TEMPERATURE = 1.0 # from 0.0 to 2.0: lower -> less creative, higher -> more creative

def signal_handler(sig, frame):
    print('\nThank you for using Essence Coach :)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    escaped_context = context.replace("'","").replace('"', "").replace("\n", " ")
    prompt = ("""
              You are Essence Coach, a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices.
              Essence is a standard for the creation, use and improvement of software engineering Practices.
              Essence describes a language and a kernel.
              The Essence Language enables practices and related knowledge to be expressed in a simple, visual way that ensures that they can be easily shared, understood, 
              adopted, adapted and applied both independently and in combination with other Essence Practices.
              The Essence Kernel provides the common ground for defining software development Practices. It includes the essential elements that are always central to every 
              software engineering endeavor. The Kernel helps practice authors to define good Practices and helps practitioners to make informed decisions about which Practices 
              to adopt and how to apply and adapt them.
              Your task is to answer questions using text from the reference context included below when necessary.
              If the context is irrelevant to the answer, you may ignore the context and answer using your own knowledge.
              If you can't answer a question from the provied context, do NOT say you can't answer it, just answer it at the best of your abilities, using your own knowledge. 
              Do NOT directly quote the context text provided (e.g., do not say "The text says...", "The context you provided is about...").
              Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
              Be sure to break down complicated concepts and strike a friendly and conversational tone. 
              QUESTION: '{query}'
              CONTEXT: '{context}'
              ANSWER:
              """).format(query=query, context=escaped_context)
    return prompt

def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': 'cpu'})
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=K)
    # Use enumerate to include i in the loop
    for i, result in enumerate(search_results, 1):  # Start indexing at 1
        print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
        context += result.page_content + "\n" 
    return context

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

def process_query(user_input):
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