import json
from fuzzywuzzy import fuzz, process
import os

# Load FAQs from the JSON file
faq_file_path = os.path.join(os.path.dirname(__file__), '../data/FAQs.json')
with open(faq_file_path, 'r', encoding='utf-8') as f:
    faqs = json.load(f)

# Preprocess FAQs for better matching
faq_questions = {question.lower(): question for question in faqs.keys()}

def get_best_match(user_question, threshold=85):
    best_match_lower, score = process.extractOne(
        user_question, faq_questions.keys(), scorer=fuzz.token_set_ratio
    )
    if score >= threshold:
        original_question = faq_questions[best_match_lower]
        answer = faqs.get(original_question, None)
        return original_question, answer, score
    else:
        return None, None, score