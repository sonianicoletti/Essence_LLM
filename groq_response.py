import os
from dotenv import load_dotenv
from groq import Groq # Documentation: https://console.groq.com/docs/models
from ensemble_retriever import get_relevant_context_from_db, get_parameters

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# MODEL_NAME = "llama3-70b-8192" # Limit: 6000 tokens per request
MODEL_NAME = "llama-3.3-70b-versatile" # Limit: 6000 tokens per chat
# MODEL_NAME = "mixtral-8x7b-32768" # Limit: 5000 tokens per chat
MAX_TOKENS = 1000 # max number of tokens the response can be
TOKEN_LIMIT = 4000 # max number of tokens the chat can be before being trimmed
SUMMARIZATION_THRESHOLD = int(TOKEN_LIMIT * 0.8)  # Summation is triggered earlier, at 80% of the limit
TEMPERATURE = 0.7 # range: 0-2

client = Groq(
    api_key=GROQ_API_KEY,
)

# Set the system prompt
system_prompt = {
    "role": "system",
    "content":
        """
        You are Essence Coach, a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices.
        Essence is a standard for the creation, use and improvement of software engineering practices.
        Essence describes a language and a kernel.
        The Essence Language enables practices to be expressed in a simple, visual way that ensures that they can be easily shared, understood, adapted and applied 
        both independently and in combination with other Essence practices.
        In Essence, practices are described by Alphas, Activities, Work Products, Competencies and Patterns.
        The Essence Kernel provides the common ground for defining software development practices. It includes the essential elements that are always central to every 
        software engineering endeavor.
        These essential elements include the seven common Alphas (Opportunity, Stakeholders, Requirements, Software System, Work, Team and Way of Working), which are
        divided into three main areas of concern (Customer, Solution, Endeavor).
        These essential elements also include Activity Spaces and Competencies for each area of concern. 
        The Kernel helps practice authors to define good practices and helps practitioners to make informed decisions about which practices to adopt and how to apply and adapt them.
    
        Your task is to answer questions using, if necessary, text from the reference context included below.
        When appropriate, answer questions related to software engineering methods and practices by mentioning Essence elements, like the Kernal Alphas.
        If the context is irrelevant to the question, you may ignore the context and answer using your own knowledge.
        If you can't answer a question from the provided context, do NOT say you can't answer it, just answer it to the best of your abilities, using your own knowledge. 
        Do NOT directly quote the context text provided (for example, do not say "The text says...", "The context you provided is about...").
        Always reformulate the provided context when answering.
        When the question is related to previous questions, prioritize the previous context. 
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
        Be sure to break down complicated concepts and strike a friendly and conversational tone.
        """
}

# Initialize the chat history
chat_history = [system_prompt]

# Function to print chat history without context and system prompt
def print_chat_history():
    print("********** CHAT HISTORY **********")
    for message in chat_history:
        if message["role"] == "user":
            user_input = message["content"].split("\nCONTEXT:")[0] # Remove the context part
            print("USER:", user_input)
        elif message["role"] == "system":
            print("SYSTEM PROMPT:", message["content"][:20] + "...")
        elif message["role"] == "assistant":
            print("ASSISTANT:", message["content"][:20] + "...")
    print("**********************************\n")

def summarize_history():
    global chat_history
    if len(chat_history) < 4:
        return
    messages_to_summarize = chat_history[1:8]  # We take more messages for better compression
    text_to_summarize = "\n".join(msg["content"] for msg in messages_to_summarize)
    print("Summarizing messages to reduce token usage...")
    summary_prompt = "Summarize the following text keeping only the most important information:\n\n" + text_to_summarize
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=300,
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        chat_history = [{"role": "system", "content": "Sommario: " + summary}] + chat_history[-2:]  # We leave only the last 2 messages
        print("Summarization complete. Chat history optimized.")
    except Exception as e:
        print(f"Error during summarization: {e}")

def process_query_groq(user_input):
    try:
        context = get_relevant_context_from_db(user_input)
        context_text = "\n".join(context)
        prompt = user_input + "\n" + "CONTEXT: " + context_text
        chat_history.append({"role": "user", "content": prompt})
        retriever_parameters = get_parameters()

        # Check the length of chat_history and keep only the last 3 messages
        total_tokens = sum(len(message["content"].split()) for message in chat_history)
        print("TOTAL TOKENS before receiving a response: " + str(total_tokens) + "\n")
        if total_tokens > SUMMARIZATION_THRESHOLD:  # We start the summation in advance
            print("Total token count approaching limit. Summarizing chat history.")
            summarize_history()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=chat_history,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        answer = response.choices[0].message.content.strip()

        if len(chat_history) < 2 or chat_history[-1]["content"] != answer:
            chat_history.append({"role": "assistant", "content": answer})

        print_chat_history()

        response_data = {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "retriever": retriever_parameters,
            "user_input": user_input,
            "context": context,
            "answer": answer
        }

        return response_data  # Return structured data for MongoDB insertion

    except Exception as e:
        print(e)
        if "rate_limit_exceeded" in str(e):
            answer = "ERROR: TOKEN LIMIT EXCEEDED"
            chat_history.clear()
        else:
            answer = "ERROR: GENERAL PROCESSING ERROR"

    response_data = {
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "retriever": retriever_parameters,
        "user_input": user_input,
        "context": context,
        "answer": answer
    }

    return response_data

""" while True:
    user_input = input("You: ")
    if user_input.lower() == "print_chat_history":
        print_chat_history()
        continue

    context = get_relevant_context_from_db(user_input)
    prompt = user_input + "\n" + "CONTEXT: " + "\n".join(context)
    chat_history.append({"role": "user", "content": prompt})

    response = process_query_groq(user_input)
    print("Assistant:", response["answer"])

    chat_history.append({
        "role": "assistant",
        "content": response["answer"]
    }) """