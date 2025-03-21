from flask import Blueprint, request, jsonify
from utils.faq_handler import get_best_match

faq_bp = Blueprint('faq', __name__)

@faq_bp.route('/askfaqs', methods=['POST'])
def ask_faqs():
    """
    REST API endpoint to handle user questions and return the best-matched answer.
    """
    data = request.get_json()
    user_question = data.get('question', '').strip().lower()

    if not user_question:
        return jsonify({"error": "Question is required"}), 400

    best_match, answer, score = get_best_match(user_question, threshold=85)

    if best_match and answer:
        return jsonify({"question": best_match, "answer": answer, "score": score})
    else:
        return jsonify({
            "error": "No relevant answer found",
            "original_question": user_question,
            "score": score
        }), 404