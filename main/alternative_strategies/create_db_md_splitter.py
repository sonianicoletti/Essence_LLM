import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import MarkdownHeaderTextSplitter

# 1 token = +-4 characters
# 100 token = 70 English words
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 100

# Define the embedding function (using a pre-trained model)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

# Path to the folder containing the markdown files
markdown_folder_path = "../data/markdown/"

# List to store all loaded markdown documents
markdown_documents = []

# Function to load Markdown files
def load_markdown_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            # Read the Markdown file content directly
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                markdown_documents.append(content)

# Load Markdown files
load_markdown_files(markdown_folder_path)

# Define headers to split on
headers_to_split_on = [("#", "Header 1")]

# MD splits
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)

# Create a list to hold all header splits
md_header_splits = []
for document in markdown_documents:
    splits = markdown_splitter.split_text(document)
    md_header_splits.extend(splits)

# Create a Chroma DB instance from the split documents
db = Chroma.from_documents(md_header_splits, embedding_function, persist_directory="./chroma_db")

print(f"Number of processed documents into ChromaDB: {len(markdown_documents)}")
print(f"Number of embeddings: {db._collection.count()}")

""" split_sizes = [len(split.page_content) for split in md_header_splits]

if split_sizes:
    smallest_size = min(split_sizes)
    largest_size = max(split_sizes)
    average_size = sum(split_sizes) / len(split_sizes)
    print(f"Smallest split size: {smallest_size} characters")
    print(f"Largest split size: {largest_size} characters")
    print(f"Average split size: {average_size} characters")

    # Find and print the number of splits larger than 8000 characters
    large_splits_count = sum(1 for size in split_sizes if size > 8000)
    print(f"Number of splits larger than 8000 characters: {large_splits_count}")

    # Print the content of the splits that are larger than 8000 characters
    print("\nContent of splits larger than 8000 characters:\n")
    for idx, (split, size) in enumerate(zip(md_header_splits, split_sizes)):
        if size > 8000:
            print(f"Split Document {idx + 1} (Size: {size} characters):\n{split.page_content}\n")
else:
    print("No splits were created.") """
