import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1 token = +-4 characters
# 100 token = 70 English words
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 100

# Define the embedding function (using a pre-trained model)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

# Path to the folder containing the markdown files
markdown_folder_path = "../data/markdown/"

# List to store all loaded documents
all_documents = []

# Function to load Markdown files
def load_markdown_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            
            # Use UnstructuredMarkdownLoader to load the Markdown file
            markdown_loader = UnstructuredMarkdownLoader(file_path=file_path)
            documents = markdown_loader.load()
            all_documents.extend(documents)

# Load Markdown files
load_markdown_files(markdown_folder_path)

# Split documents after loading them
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
split_docs = text_splitter.split_documents(all_documents)

# Create a Chroma DB instance from the split documents
db = Chroma.from_documents(split_docs, embedding_function, persist_directory="./chroma_db")

print(f"Number of processed documents into ChromaDB: {len(all_documents)}")
print(f"Number of embeddings: {db._collection.count()}")
