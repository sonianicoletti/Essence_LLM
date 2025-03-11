import os
import tiktoken
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

# Initialize tiktoken for accurate token counting
encoder = tiktoken.get_encoding("cl100k_base")

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


def count_tokens(messages):
    overhead_per_message = 4
    total = 0
    for m in messages:
        total += len(encoder.encode(m["content"])) + overhead_per_message
    return total


def summarize_history():
    global chat_history
    if len(chat_history) < 2:
        return

    system_msg = chat_history[0]
    old_msgs = chat_history[1:]
    text_to_summarize = "\n".join(m["content"] for m in old_msgs)
    safe_word_limit = 1000
    words = text_to_summarize.split()
    if len(words) > safe_word_limit:
        text_to_summarize = " ".join(words[:safe_word_limit])

    summary_prompt = "Summarize the following text, keeping only the key details:\n\n" + text_to_summarize
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=300,
            temperature=0.5
        )
        summary = resp.choices[0].message.content.strip()
        summary_msg = {"role": "assistant", "content": "Summary: " + summary}
        chat_history = [system_msg, summary_msg]
    except Exception as e:
        pass  # In production, you might handle errors or fallback here


def trim_history_if_needed():
    while count_tokens(chat_history) > TOKEN_LIMIT and len(chat_history) > 1:
        chat_history.pop(1)


def trim_history():
    current_tokens = count_tokens(chat_history)
    if current_tokens >= SUMMARIZATION_THRESHOLD:
        summarize_history()
        current_tokens = count_tokens(chat_history)
        if current_tokens > TOKEN_LIMIT:
            trim_history_if_needed()


def process_query_groq(user_input):
    try:
        context = get_relevant_context_from_db(user_input)
        context_text = "\n".join(context)
        full_user_prompt = user_input + "\n" + "CONTEXT: " + context_text
        chat_history.append({"role": "user", "content": full_user_prompt})

        trim_history()

        retriever_params = get_parameters()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=chat_history,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        answer = response.choices[0].message.content.strip()

        chat_history.append({"role": "assistant", "content": answer})
        trim_history()

        print_chat_history()

        return {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "retriever": retriever_params,
            "user_input": full_user_prompt,
            "context": context,
            "answer": answer
        }
    except Exception as e:
        if "rate_limit_exceeded" in str(e):
            chat_history.clear()
            answer = "ERROR: TOKEN LIMIT EXCEEDED"
        else:
            answer = "ERROR: GENERAL PROCESSING ERROR"
        return {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "retriever": get_parameters(),
            "user_input": user_input,
            "context": [],
            "answer": answer
        }

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