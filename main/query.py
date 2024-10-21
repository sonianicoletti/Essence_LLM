import os
import signal
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCYBOykSOL_ToRpPJ81VWxS2bgIEb56PtE"
K = 3 # number of results you need to retrieve (each result is an embedding)  
MODEL_NAME = "gemini-1.5-pro"
# 1 token = +-4 characters
# 100 token = 70 English words
# gemini-1.0-pro: 30k + 2k = 32k tokens context window
# gemini-1.5-pro: input 2M, output 8k tokens (5600 words)
TEMPERATURE = 0.1 # from 0.0 to 2.0: lower -> less creative, higher -> more creative

def signal_handler(sig, frame):
    print('\nThank you for using Essence Coach :)')
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
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=K)
    # Use enumerate to include i in the loop
    for i, result in enumerate(search_results, 1):  # Start indexing at 1
        #print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
        context += result.page_content + "\n" 
    return context

def generate_answer(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    answer = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=8000,
        temperature=1.0,
    ),)
    return answer.text

while True:
    print("-------------------------------------------------------------")
    print("What would you like to ask?")
    query = input("Query: ") 
    context = get_relevant_context_from_db(query)  
    prompt = generate_rag_prompt(query=query, context=context)
    answer = generate_answer(prompt=prompt)
    # print("CONTEXT: " + context)
    print("ANSWER: " + answer)