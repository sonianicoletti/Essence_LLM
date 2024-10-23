import os
from dotenv import load_dotenv
from groq import Groq
from context_retrieval import generate_rag_prompt, get_relevant_context_from_db

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# MODEL_NAME = "llama3-70b-8192" # Limit: 6000 tokens per request
MODEL_NAME = "llama-3.1-70b-versatile" # Limit: 128k tokens per request
MAX_TOKENS = 1000
TEMPERATURE = 1.2

client = Groq(
    api_key=GROQ_API_KEY,
)

# Set the system prompt
system_prompt = {
    "role": "system",
    "content":
    """You are Essence Coach, a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices.
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
    Be sure to break down complicated concepts and strike a friendly and conversational tone."""
}

# Initialize the chat history
chat_history = [system_prompt]

def process_query_groq(user_input):
    context = get_relevant_context_from_db(user_input) 
    prompt = user_input + "\n" + "CONTEXT: " + context
    chat_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=MODEL_NAME,
                                            messages=chat_history,
                                            max_tokens=MAX_TOKENS,
                                            temperature=TEMPERATURE)
    # Append the response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    answer = response.choices[0].message.content
    print("************************ PROMPT: ************************\n" + prompt + "\n*********************************************************\n")
    print("************************ ANSWER: ************************\n" + answer + "\n*********************************************************\n")
    return answer

""" while True:
  # Get user input from the console
  user_input = input("You: ")
  context = get_relevant_context_from_db(user_input)
  prompt = user_input + "\n" + "CONTEXT: " + context
  # Append the user input to the chat history
  chat_history.append({"role": "user", "content": prompt})
  response = client.chat.completions.create(model=MODEL_NAME,
                                            messages=chat_history,
                                            max_tokens=MAX_TOKENS,
                                            temperature=TEMPERATURE)
  # Append the response to the chat history
  chat_history.append({
      "role": "assistant",
      "content": response.choices[0].message.content
  })
  # Print the response
  print("Assistant:", response.choices[0].message.content) """