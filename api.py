from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from create_tweet import create_tweet

flask_app = Flask(__name__)
CORS(flask_app)

# Root route → serve frontend
@flask_app.route("/")
def index():
    return render_template("index.html")

# Simple add numbers route
@flask_app.route("/add/<num1>/<num2>")
def add_numbers(num1, num2):
    sumNum = int(num1) + int(num2)
    return f"this method will add numbers {num1} and {num2} ==> {sumNum}"

# Tweet generation route (POST instead of GET)
@flask_app.route("/generate", methods=["POST"])
@cross_origin()
def generate_tweet():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        tweet_data = create_tweet(prompt)
        return jsonify(tweet_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    flask_app.run(debug=True)
