import csv
import os
import requests
from dotenv import load_dotenv
from ensemble_retriever import get_relevant_context_from_db
from groq import Groq

load_dotenv()

# Constants
INPUT_FILE = "questions.csv"
OUTPUT_FILE = "dataset_llama.csv"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """ You are Essence Coach, a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices. 
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
    Be sure to break down complicated concepts and strike a friendly and conversational tone. """

def call_groq_api(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return chat_completion.choices[0].message.content

def call_groq_api_context(prompt_context):
    chat_completion = client.chat.completions.create(
        messages=prompt_context,
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return chat_completion.choices[0].message.content

# Step 1: Read questions from CSV
questions = []
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        questions.append(row["question"])

# Step 2 & 3: Get answers from LLM and save to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["question", "answer_llama", "context_1", "context_2", "context_3", "context_4", "answer_llama_rag"])

    for question in questions:
        # First API call (without context)
        answer_no_context = call_groq_api(question)

        # Get context from RAG system
        context = get_relevant_context_from_db(question)
        context_text = "\n".join(context)

        # Second API call (with context)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{question}\nCONTEXT: {context_text}"}
        ]
        answer_with_context = call_groq_api_context(messages)

        # Ensure exactly 4 context columns
        context_padded = context[:4] + [""] * (4 - len(context))

        # Write to CSV
        writer.writerow([question, answer_no_context] + context_padded + [answer_with_context])

print(f"Answers saved to '{OUTPUT_FILE}'.")
