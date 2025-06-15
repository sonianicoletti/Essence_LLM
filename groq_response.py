import os
from dotenv import load_dotenv
from groq import Groq # Documentation: https://console.groq.com/docs/models
from ensemble_retriever import get_relevant_context_from_db, get_parameters
from transformers import AutoTokenizer # to count tokens

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = "llama-3.3-70b-versatile" # Limit: 6000 tokens per chat
MAX_TOKENS = 1000 # max number of tokens the response can be
TOKEN_LIMIT = 4000 # max number of tokens the chat can be before being trimmed
TEMPERATURE = 0.7 # range: 0-2
tokenizer = AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer")

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
            # user_input = message["content"].split("\nCONTEXT:")[0] # Remove the context part
            user_input = message["content"]
            print("USER:", user_input)
        elif message["role"] == "system":
            print("SYSTEM PROMPT:", message["content"][:20] + "...")
        elif message["role"] == "assistant":
            print("ASSISTANT:", message["content"])
    print("**********************************\n")


def count_tokens(messages):
    total_tokens = 0
    for m in messages:
        content = m["content"]
        tokens = tokenizer.encode(content, add_special_tokens=False)
        total_tokens += len(tokens)
    return total_tokens

def build_final_messages(history):
    final_msgs = []
    for msg in history:
        final_msgs.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return final_msgs

def trim_and_summarise_history(chat_history, token_limit=TOKEN_LIMIT):
    if count_tokens(chat_history) <= token_limit:
        return chat_history

    # Always preserve system prompt and last message
    system_prompt = chat_history[0]
    last_message = chat_history[-1]
    preserved = [system_prompt]
    summarised = []

    # Summarise all messages except last
    for msg in chat_history[1:-1]:
        try:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                prompt_text = "Summarise the following user message and its appended contexts in less than 100 words. \n"
            else:
                prompt_text = "Summarise the following assistant response in less than 100 words. \n"

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages= [{"role": "user", "content": prompt_text + content}],
                max_tokens=500,
                temperature=0.3
            )
            summary = response.choices[0].message.content.strip()

            summarised.append({"role": role, "content": summary})

        except Exception as e:
            print(f"Summarisation failed: {e}")
            summarised.append(msg)  # Fallback to original

    final_history = preserved + summarised + [last_message]

    # If it's still too long, delete oldest summarised messages one by one
    while count_tokens(final_history) > token_limit and len(summarised) > 0:
        summarised.pop(0)
        final_history = preserved + summarised + [last_message]

    return final_history


def process_query_groq(user_input):
    global chat_history
    try:
        context = get_relevant_context_from_db(user_input)
        context_text = "\n".join(context)
        prompt = user_input + "\n" + "CONTEXT: " + "\n" + context_text

        chat_history.append({"role": "user", "content": prompt})

        # Trim the history if needed
        chat_history = trim_and_summarise_history(chat_history, token_limit=TOKEN_LIMIT)

        # Forming the final list of messages
        final_msgs = build_final_messages(chat_history)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=final_msgs,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})

        print_chat_history()

        # Return structured data for MongoDB insertion
        retriever_parameters = get_parameters()
        return {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "retriever": retriever_parameters,
            "user_input": user_input,
            "context": context,
            "answer": answer
        }

    except Exception as e:
        print("Error in process_query_groq:", e)
        err_str = str(e).lower()
        if "too large" in err_str or "rate_limit_exceeded" in err_str or "request too large" in err_str:
            answer = "ERROR: TOKEN LIMIT EXCEEDED (DELETEING CHAT HISTORY)"
            chat_history.clear()
        else:
            answer = "ERROR: GENERAL PROCESSING ERROR"

        return {
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "retriever": {},
            "user_input": user_input,
            "context": [],
            "answer": answer
        }