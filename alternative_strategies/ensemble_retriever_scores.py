import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.runnables import chain
from typing import List, Tuple

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

markdown_folder_path = "../data/markdown/"
markdown_documents = []

def load_markdown_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                markdown_documents.append(content)
load_markdown_files(markdown_folder_path)

headers_to_split_on = [("#", "Header 1")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
md_header_splits = [] # list of Documents
for document in markdown_documents:
    splits = markdown_splitter.split_text(document)
    md_header_splits.extend(splits)

page_content_list = [doc.page_content for doc in md_header_splits] # list of Strings

@chain
def create_hybrid_retriever(query: str) -> List[Document]:
    # Retrieve documents and scores from retriever1
    docs1, scores1 = zip(*retriever1.similarity_search_with_score(query))
    for doc, score in zip(docs1, scores1):
        doc.metadata["score"] = score

    # Retrieve documents and scores from bm25_retriever
    docs2, scores2 = zip(*bm25_retriever.similarity_search_with_score(query))
    for doc, score in zip(docs2, scores2):
        doc.metadata["score"] = score

    # Combine results from both retrievers
    combined_docs = list(docs1) + list(docs2)
    
    # Filter results by score threshold
    score_threshold = 0.5  # Set your desired threshold here
    filtered_docs = [doc for doc in combined_docs if doc.metadata["score"] >= score_threshold]
    
    return filtered_docs

def get_relevant_context_from_db(query):
    context = ""
    search_results = create_hybrid_retriever(query)
    for i, result in enumerate(search_results, 1): 
        print(f"\n********************* CONTEXT #{i}: *********************\n{result.page_content}")
        context += result.page_content + "\n"
    
    return context

get_relevant_context_from_db(query)


""" bm25_retriever = BM25Retriever.from_texts(page_content_list)
bm25_retriever.k = 2

embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': 'cpu'})
chroma_vectorstore = Chroma.from_documents(md_header_splits, embedding_function)
chroma_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 2})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5]
) """