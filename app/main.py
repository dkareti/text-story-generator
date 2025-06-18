from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import logging

app = Flask(__name__)

# Set up a simple and lightweight LLM pipeline using Hugging Face (DistilGPT2)
llm = pipeline("text-generation", model="distilgpt2")

# Logging setup (for observability on Render)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.form.get("prompt")
    logger.info(f"Received prompt: {user_input}")
    
    if not user_input:
        return jsonify({"error": "Prompt required."}), 400

    try:
        output = llm(user_input, max_length=300, do_sample=True, top_k=50, temperature=0.9)[0]["generated_text"]
        return jsonify({"response": output})
    except Exception as e:
        logger.error(f"LLM generation error: {str(e)}")
        return jsonify({"error": "Generation failed."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3001)  