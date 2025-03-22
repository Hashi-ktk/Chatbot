import os
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env file

import faiss
import openai
import numpy as np
from PyPDF2 import PdfReader
from typing import List
import nltk
from collections import Counter

# Download required NLTK data
nltk.download('punkt', quiet=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDINGS_FILE = "workspace/embeddings.index"
CONTEXT_FILE = "workspace/context.txt"
CHUNK_SEPARATOR = "\n===CHUNK===\n"

# New function to remove duplicate sentences (based on provided code)
def remove_duplicates(text):
    sentences = text.split("\n")
    counter = Counter(sentences)
    unique_sentences = [s.strip() for s in sentences if counter[s] == 1 or len(s) > 20]
    return "\n".join(unique_sentences).strip()

# New function to split text into overlapping chunks (based on provided code)
def split_into_chunks(text, chunk_size=256, overlap=50):
    words = text.split()
    return [" ".join(words[i: i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

# Modified extract function that uses remove_duplicates.
def extract_text_from_pdf(pdf_file_path: str) -> str:
    """
    Extract text from a PDF file and remove duplicate sentences.
    """
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return remove_duplicates(text)

def generate_embeddings(text: str) -> list:
    """
    Generate embeddings for the given text using OpenAI's API.
    """
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def save_embeddings_to_faiss(embeddings: List[list], contexts: List[str]):
    """
    Save the list of embeddings and their associated contexts.
    """
    if not embeddings or not contexts:
        raise ValueError("Empty embeddings or contexts")
    dimension = len(embeddings[0])
    embedding_array = np.array(embeddings, dtype='float32')
    
    if os.path.exists(EMBEDDINGS_FILE):
        index = faiss.read_index(EMBEDDINGS_FILE)
    else:
        index = faiss.IndexFlatL2(dimension)
    
    index.add(embedding_array)
    faiss.write_index(index, EMBEDDINGS_FILE)
    
    # Save contexts with a separator.
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        f.write(CHUNK_SEPARATOR.join(contexts))

def initialize_rag():
    """
    Initialize the RAG system by reading the PDF, splitting its text into chunks,
    generating embeddings for each chunk, and saving both to disk.
    """
    os.makedirs("workspace", exist_ok=True)
    pdf_path = "data/Data.pdf"
    text = extract_text_from_pdf(pdf_path)
    # Use the new chunking function to split the text into overlapping chunks.
    chunks = split_into_chunks(text)
    embeddings = []
    for chunk in chunks:
        emb = generate_embeddings(chunk)
        embeddings.append(emb)
    save_embeddings_to_faiss(embeddings, chunks)

def query_embeddings(question: str, k: int = 5) -> str:
    """
    Query the FAISS index with the question and return the top k relevant contexts.
    
    Args:
        question: The user question.
        k: Number of top chunks to return.
    
    Returns:
        A combined string of the top relevant context chunks.
    """
    query_embedding = generate_embeddings(question)
    query_embedding_array = np.array([query_embedding], dtype='float32')
    
    index = faiss.read_index(EMBEDDINGS_FILE)
    _, indices = index.search(query_embedding_array, k)
    
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        all_contexts = f.read().split(CHUNK_SEPARATOR)
    
    relevant_contexts = [all_contexts[i] for i in indices[0] if i < len(all_contexts)]
    return "\n".join(relevant_contexts)