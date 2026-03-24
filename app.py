from flask import Flask, render_template, request, jsonify
from brain import get_ai_response
from memory import load_name

app = Flask(__name__)

chat_history = []

@app.route("/")
def home():
    name = load_name()

    if name:
        greeting = f"Welcome back, {name} 👋"
    else:
        greeting = "Hello! Tell me your name 😊"

    return render_template("index.html", greeting=greeting)


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    if not user_message.strip():
        return jsonify({"reply": "Please type something."})

    chat_history.append({
        "role": "user",
        "content": user_message
    })

    reply = get_ai_response(chat_history)

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)