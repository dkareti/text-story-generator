from flask import Flask, render_template, request, jsonify
import random
import logging

app = Flask(__name__)

# Simple story generator function (no LLM)
def generate_story(genre):
    elements = {
        "adventure": {
            "characters": ["a brave knight", "an explorer", "a treasure hunter"],
            "settings": ["in a dark cave", "on a distant island", "deep in the jungle"],
            "goals": ["sought a lost relic", "fought off wild beasts", "escaped a booby-trapped ruin"]
        },
        "sci-fi": {
            "characters": ["a curious robot", "a space pilot", "an alien child"],
            "settings": ["on Mars", "aboard a starship", "in a futuristic city"],
            "goals": ["discovered a wormhole", "repaired a broken AI", "saved their planet"]
        },
        "fantasy": {
            "characters": ["a young wizard", "a talking dragon", "a forest elf"],
            "settings": ["in a mystical forest", "at the royal castle", "within an ancient dungeon"],
            "goals": ["cast a forbidden spell", "protected the kingdom", "found a magical artifact"]
        }
    }

    #this line seeks to find the specified genre from the dictionary elements
    #   if the genre is not found it defaults to the adventure one
    starters = {
        "adventure" : "In a far-off land",
        "sci-fi" : "In a dystopian land",

        "fantasy" : "Once upon a time"
    }

    selection = starters.get(genre, starters["adventure"])

    genre_data = elements.get(genre, elements["adventure"])
    character = random.choice(genre_data["characters"])
    setting = random.choice(genre_data["settings"])
    goal = random.choice(genre_data["goals"])

    return f"Genre: {genre.strip().capitalize()}; {selection} there was {character} {setting} who {goal}."

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    genre = request.form.get("genre")
    logger.info(f"Received prompt: {genre}")

    if not genre:
        return jsonify({"error": "You must select a genre."}), 400

    story = generate_story(genre)
    return jsonify({"response": story})

if __name__ == "__main__":
    app.run(debug=True, port=3001)