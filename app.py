from flask import Flask
from flask_cors import CORS
from blueprints.faq_bp import faq_bp
from blueprints.noor_bp import noor_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(faq_bp)
app.register_blueprint(noor_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")