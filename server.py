
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")

MAX_USERS = 8
leader_id = None
current_target = None


def authorized():
    return (
        bool(TOKEN)
        and request.headers.get("Authorization") == f"Bearer {TOKEN}"
    )


@app.route("/")
def home():
    return "TargetBot server is running!"


@app.route("/leader", methods=["POST"])
def change_leader():
    global leader_id

    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")

    if not isinstance(user_id, int) or not 1 <= user_id <= MAX_USERS:
        return jsonify({"error": "Invalid user ID"}), 400

    leader_id = user_id
    return jsonify({"status": "ok", "leader_id": leader_id})


@app.route("/leader", methods=["GET"])
def get_leader():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"leader_id": leader_id})


@app.route("/target", methods=["POST"])
def publish_target():
    global current_target

    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    target_id = data.get("target_id")

    if user_id != leader_id or leader_id is None:
        return jsonify({"error": "Only the current leader can publish"}), 403

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

    return jsonify({
        "leader_id": leader_id,
        "target_id": current_target
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
