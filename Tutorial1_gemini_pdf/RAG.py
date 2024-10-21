# tutorial 1: https://www.youtube.com/watch?v=aTqDvi39yQg
# pip install langchain chromadb pypdf sentence-transformers google-generativeai
# pip install -U langchain-huggingface

import os
import signal
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCYBOykSOL_ToRpPJ81VWxS2bgIEb56PtE"

def signal_handler(sig, frame):
    print('\nThanks for using Gemini. :)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    escaped_context = context.replace("'","").replace('"', "").replace("\n", " ")
    prompt = ("""
              You are a helpful and informative bot that answers questions using text from the reference context included below when necessary. \
              Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
              However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
              strike a friendle and conversational tone. \
              If the context is irrelevant to the answer, you may ignore it. 
              QUESTION: '{query}'
              CONTEXT: '{context}'

              ANSWER:
              """).format(query=query, context=escaped_context)
    return prompt

def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    vector_db = Chroma(persist_directory="./chroma_db_nccn", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=6) # k is the number of results you need to retrieve (each result is an embedding)
    for result in search_results:
        context += result.page_content + "\n"
    return context

def generate_answer(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

welcome_text = generate_answer("Can you quickly introduce yourself?")
print(welcome_text)

while True:
    print("-------------------------------------------------------------")
    print("What would you like to ask?")
    query = input("Query: ") 
    context = get_relevant_context_from_db(query)  
    prompt = generate_rag_prompt(query=query, context=context)
    answer = generate_answer(prompt=prompt)
    print(answer)