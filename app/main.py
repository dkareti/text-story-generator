from flask import Flask, render_template, request, jsonify
import random
import logging

app = Flask(__name__)

# Simple story generator function (no LLM)
def generate_story(prompt):
    characters = ["a frog", "a robot", "a cat", "an alien", "a young wizard"]
    settings = ["in a forest", "on Mars", "in New York", "at school", "inside a video game"]
    goals = ["wanted to fly", "was searching for treasure", "learned to code", "had to save the world", "became a hero"]

    character = random.choice(characters)
    setting = random.choice(settings)
    goal = random.choice(goals)

    return f"{prompt.strip().capitalize()}... There was {character} {setting} who {goal}."

# Logging setup
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

    story = generate_story(user_input)
    return jsonify({"response": story})

if __name__ == "__main__":
    app.run(debug=True, port=3001)