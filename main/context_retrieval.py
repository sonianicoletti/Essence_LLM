import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

K = 4  # Number of results you need to retrieve (each result is an embedding)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': 'cpu'})
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=K)

    for i, result in enumerate(search_results, 1):
        # print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
        context += result.page_content + "\n"
    
    return context

def generate_rag_prompt(query, context):
    escaped_context = context.replace("'", "").replace('"', "").replace("\n", " ")
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
              If you can't answer a question from the provided context, do NOT say you can't answer it, just answer it to the best of your abilities, using your own knowledge. 
              Do NOT directly quote the context text provided (e.g., do not say "The text says...", "The context you provided is about...").
              Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
              Be sure to break down complicated concepts and strike a friendly and conversational tone. 
              QUESTION: '{query}'
              CONTEXT: '{context}'
              ANSWER:
              """).format(query=query, context=escaped_context)
    return prompt
