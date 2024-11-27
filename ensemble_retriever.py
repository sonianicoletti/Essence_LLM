import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter

# 1 token = +-4 characters
# 100 token = 70 English words
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
K_1 = 2 # bm25
K_2 = 2 # chroma

markdown_folder_path = "./data/markdown/"
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
md_header_splits = []
for document in markdown_documents:
    splits = markdown_splitter.split_text(document)
    md_header_splits.extend(splits)

page_content_list = [doc.page_content for doc in md_header_splits]

bm25_retriever = BM25Retriever.from_texts(page_content_list)
bm25_retriever.k = K_1

embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': 'cpu'})
chroma_vectorstore = Chroma.from_documents(md_header_splits, embedding_function)
chroma_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": K_2})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5]
)

# print(f"Number of embeddings: {len(md_header_splits)}")

def get_relevant_context_from_db(query):
    context_list = []
    search_results = ensemble_retriever.invoke(query)
    for result in search_results:
        context_list.append(result.page_content)
    return context_list

def get_parameters():
    return "Search: " + "Ensemble retriver" + "\nK1 (bm25): " + str(K_1) + "\nK2 (chroma): " + str(K_2) + "\nChunk splitting: " + str(headers_to_split_on) + "\nNumber of embeddings: " + str(len(md_header_splits))