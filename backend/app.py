import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Product
from ai_assistant import ProductAssistant

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

assistant = ProductAssistant()


def load_assistant():
    """(Re)builds the assistant's TF-IDF index from current DB products."""
    with app.app_context():
        products = [p.to_dict() for p in Product.query.all()]
        assistant.fit(products)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/products")
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@app.route("/assistant/ask", methods=["POST"])
def ask_assistant():
    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"]
    results = assistant.ask(question, top_k=3)

    return jsonify({
        "question": question,
        "results": results
    }), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    load_assistant()
    app.run(host="0.0.0.0", port=5000, debug=True)
