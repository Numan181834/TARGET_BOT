
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
current_target = None


def authorized():
    return (
        TOKEN != ""
        and request.headers.get("Authorization") == f"Bearer {TOKEN}"
    )


@app.route("/")
def home():
    return "TargetBot server is running!"


@app.route("/target", methods=["POST"])
def publish_target():
    global current_target

    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    target_id = data.get("target_id")

    if not target_id:
        return jsonify({"error": "Target ID missing"}), 400

    current_target = str(target_id)

    return jsonify({
        "status": "ok",
        "target_id": current_target
    })


@app.route("/target", methods=["GET"])
def get_target():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"target_id": current_target})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
