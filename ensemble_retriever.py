import os
import logging
import argparse
from dotenv import load_dotenv
from ast import literal_eval
from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ensemble_retriever")

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    logger.warning("GROQ_API_KEY not found in the environment")
groq_client = Groq(api_key=groq_api_key)

parser = argparse.ArgumentParser()
parser.add_argument("--cosine_threshold", type=float, default=float(os.getenv("COSINE_THRESHOLD", 0.75)))
parser.add_argument("--bm25_weight", type=float, default=float(os.getenv("BM25_WEIGHT", 0.5)))
parser.add_argument("--chroma_weight", type=float, default=float(os.getenv("CHROMA_WEIGHT", 0.5)))
args, _ = parser.parse_known_args()

# 1 token = +-4 characters
# 100 token = 70 English words
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
K_1 = 2  # bm25
K_2 = 2  # chroma
IGNORE_QUERIES = {"ciao", "hi", "hello", "ok", "thanks"}

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
    retrievers=[bm25_retriever, chroma_retriever],
    weights=[args.bm25_weight, args.chroma_weight]
)


# print(f"Number of embeddings: {len(md_header_splits)}")


def cosine_filtering(query, docs, threshold):
    query_vec = embedding_function.embed_query(query)
    filtered = []
    for doc in docs:
        doc_vec = embedding_function.embed_query(doc.page_content)
        sim = cosine_similarity([query_vec], [doc_vec])[0][0]
        logger.debug(f"Sim = {sim:.3f} > {threshold}")
        if sim >= threshold:
            filtered.append(doc)
    if not filtered:
        logger.warning("[cosine] No context passed filtering - fallback to first")
        return [docs[0]]
    return filtered


def call_llm_filter(query, context_texts):
    prompt = (
        "You are a helpful assistant.\n\n"
        f"Given the following user query:\n\"{query}\"\n\n"
        "And the following context snippets:\n\n"
        f"{chr(10).join([f'[{i + 1}] {ctx}' for i, ctx in enumerate(context_texts)])}\n\n"
        "Return a list of snippet numbers (1-based index, e.g., [1, 3]) that are relevant to answer the query. "
        "Just reply with a Python list using 1-based indexing."
    )
    logger.debug(f"LLM prompt: {prompt[:300]}...")
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.0
        )
        reply = response.choices[0].message.content.strip()
        indices = literal_eval(reply)
        if not isinstance(indices, list) or not all(isinstance(i, int) for i in indices):
            raise ValueError("LLM reply is not list[int]")
        return indices
    except Exception as e:
        logger.error(f"LLM filtering failed: {e}")
        return []


def llm_filtering(query, docs):
    if not docs:
        return []
    indices = call_llm_filter(query, [doc.page_content for doc in docs])
    if not indices:
        logger.warning("[llm] No context passed filtering - fallback to first")
        return [docs[0]]
    return [docs[i - 1] for i in indices if 0 < i <= len(docs)]


def get_relevant_context_from_db(query, filter_strategy="cosine", threshold=args.cosine_threshold):
    if not query or query.lower().strip() in IGNORE_QUERIES:
        return []

    search_results = ensemble_retriever.invoke(query)
    logger.info(f"[{filter_strategy}] Retrieved: {len(search_results)}")

    if filter_strategy == "cosine":
        filtered = cosine_filtering(query, search_results, threshold)
    elif filter_strategy == "llm":
        filtered = llm_filtering(query, search_results)
    else:
        filtered = search_results

    logger.info(f"[{filter_strategy}] Filtered: {len(filtered)}")
    return [doc.page_content for doc in filtered]


def get_parameters():
    return (
            "Search: Ensemble retriever" +
            f"\nK1 (bm25): {K_1}" +
            f"\nK2 (chroma): {K_2}" +
            f"\nChunk splitting: {headers_to_split_on}" +
            f"\nNumber of embeddings: {len(md_header_splits)}" +
            f"\nDefault cosine threshold: {args.cosine_threshold}" +
            f"\nWeights: BM25={args.bm25_weight}, Chroma={args.chroma_weight}"
    )
