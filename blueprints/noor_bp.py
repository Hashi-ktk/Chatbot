from flask import Blueprint, request, jsonify
from utils.rag_utils import query_embeddings
import openai
import os

noor_bp = Blueprint('noor', __name__)

@noor_bp.route('/asknoor', methods=['POST'])
def ask_question():
    """Ask a question using the RAG system with accessibility guidelines."""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Get relevant context using RAG retriever
        context = query_embeddings(question)

        # Construct messages for OpenAI API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that provides detailed, accessible, and empathetic answers, "
                    "specifically catering to people with disabilities. Use clear and simple language. "
                    "If a question is outside the scope of the provided context, respond with: "
                    "'I'm sorry, but that question is outside of my current knowledge base.'"
                )
            },
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]

        # Query GPT-4o using streaming API
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True
        )

        final_response = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                final_response += chunk.choices[0].delta.content

        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500