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


def count_tokens_approx(messages):
    return sum(len(m["content"].split()) for m in messages)


def summarize_message(message):
    role = message["role"]
    original_text = message["content"]

    if role == "user":
        prompt_text = "Summarise the following user message and its appended context in less than 80 words."
    else:
        prompt_text = "Summarise the following assistant response in less than 80 words."

    summary_prompt = [
        {"role": "system", "content": prompt_text},
        {"role": role, "content": original_text}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=summary_prompt,
            max_tokens=150,
            temperature=0.3
        )
        summarized_content = response.choices[0].message.content.strip()

        # Recursive shortening if summary too long
        if len(summarized_content.split()) > 80:
            forced_prompt = [
                {"role": "system", "content": "Please rewrite the following summary in less than 60 words:"},
                {"role": "assistant", "content": summarized_content}
            ]
            response2 = client.chat.completions.create(
                model=MODEL_NAME,
                messages=forced_prompt,
                max_tokens=80,
                temperature=0.3
            )
            summarized_content = response2.choices[0].message.content.strip()

        return "Summary: " + summarized_content
    except Exception as e:
        print(f"ERROR during summarization: {e}")
        return message["content"]


def do_summarize_pass(history, skip_last_n=2):
    if len(history) <= skip_last_n + 1:
        return history

    preserved = history[-skip_last_n:]
    middle = history[1:-skip_last_n]

    new_hist = [history[0]]
    for msg in middle:
        short_text = summarize_message(msg)
        new_hist.append({"role": msg["role"], "content": short_text})
    new_hist.extend(preserved)

    return new_hist


def reduce_history_if_needed(history, skip_last_n=2, max_passes=5):
    for _ in range(max_passes):
        if count_tokens_approx(history) <= TOKEN_LIMIT:
            break
        history = do_summarize_pass(history, skip_last_n=skip_last_n)

    # If after max_passes it's still too much - delete the oldest ones
    while count_tokens_approx(history) > TOKEN_LIMIT:
        if len(history) <= skip_last_n + 1:
            break
        del history[1]

    return history


def build_final_messages(history):
    final_msgs = []
    for msg in history:
        final_msgs.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return final_msgs


def process_query_groq(user_input):
    global chat_history
    try:
        context = get_relevant_context_from_db(user_input)
        context_text = "\n".join(context)
        prompt = user_input + "\n" + "CONTEXT: " + context_text

        chat_history.append({"role": "user", "content": prompt})

        # Trim the history
        chat_history = reduce_history_if_needed(chat_history, skip_last_n=2, max_passes=5)

        # Forming the final list of messages
        final_msgs = build_final_messages(chat_history)

        retriever_parameters = get_parameters()

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
            answer = "ERROR: TOKEN LIMIT EXCEEDED (AGGRESSIVE CLEANUP)"
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