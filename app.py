from flask import Flask
from blueprints.faq_bp import faq_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(faq_bp)

if __name__ == "__main__":
    app.run(debug=True)