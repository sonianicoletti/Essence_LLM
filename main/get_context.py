# Generates the context taking information from the vector database
# Model used: sentence-transformers/all-MiniLM-L6-v2

import os
import signal
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def signal_handler(sig, frame):
    print('\nBye bye :)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    escaped_context = context.replace("'","").replace('"', "").replace("\n", " ")
    prompt = ("""
              You are a helpful and informative bot that answers questions using text from the reference context included below when necessary. \
              Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
              However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
              strike a friendle and conversational tone. \
              You are an expert of Essence, a software engineering standard.
              If the context is irrelevant to the answer, you may ignore it. 
              QUESTION: '{query}'
              CONTEXT: '{context}'

              ANSWER:
              """).format(query=query, context=escaped_context)
    return prompt

def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=3)  # k is the number of results you need to retrieve (each result is an embedding)  
    # Use enumerate to include i in the loop
    for i, result in enumerate(search_results, 1):  # Start indexing at 1
        print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
        context += result.page_content + "\n" 
    return context

def generate_answer(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

while True:
    print("-------------------------------------------------------------")
    print("What would you like to ask?")
    query = input("Query: ") 
    context = get_relevant_context_from_db(query)