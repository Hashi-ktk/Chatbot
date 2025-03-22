import os
from utils.rag_utils import initialize_rag

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in .env file")
        return
    if not os.path.exists("data/Data.pdf"):
        print("Error: data/Data.pdf not found.")
        return

    print("Initializing RAG system...")
    try:
        initialize_rag()
        print("RAG system initialized successfully!")
        print("Embeddings saved to: workspace/embeddings.index")
        print("Contexts saved to: workspace/context.txt")
    except Exception as e:
        print(f"Initialization failed: {e}")

if __name__ == "__main__":
    main()