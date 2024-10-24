import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

markdown_folder_path = "../data/markdown/"
markdown_documents = []

def load_markdown_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            # Read the Markdown file content directly
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                markdown_documents.append(content)
load_markdown_files(markdown_folder_path)

headers_to_split_on = [("#", "Header 1")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
md_header_splits = []
for document in markdown_documents:
    splits = markdown_splitter.split_text(document)
    md_header_splits.extend(splits)

page_content_list = [doc.page_content for doc in md_header_splits]

bm25_retriever = BM25Retriever.from_texts(page_content_list)
bm25_retriever.k = 2

embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': 'cpu'})
chroma_vectorstore = Chroma.from_documents(md_header_splits, embedding_function)
chroma_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 2})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5]
)

def get_relevant_context_from_db(query):
    context = ""
    search_results = ensemble_retriever.invoke(query)
    for i, result in enumerate(search_results, 1): 
        print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
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
