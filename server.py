
import os
import hmac
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_USERS = 8
leader_id = None
current_target = None

USER_TOKENS = {}

for item in os.environ.get("USER_TOKENS", "").split(";"):
    if "=" in item:
        user, token = item.split("=", 1)
        if user.isdigit() and 1 <= int(user) <= MAX_USERS and token:
            USER_TOKENS[int(user)] = token


def authorized_user():
    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Bearer "):
        return None

    supplied_token = auth[7:]

    for user_id, token in USER_TOKENS.items():
        if hmac.compare_digest(supplied_token, token):
            return user_id

    return None


@app.route("/")
def home():
    return "TargetBot server is running!"


@app.route("/leader", methods=["POST"])
def change_leader():
    global leader_id

    user_id = authorized_user()

    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    leader_id = user_id

    return jsonify({
        "status": "ok",
        "leader_id": leader_id
    })


@app.route("/leader", methods=["GET"])
def get_leader():
    if authorized_user() is None:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"leader_id": leader_id})


@app.route("/target", methods=["POST"])
def publish_target():
    global current_target

    user_id = authorized_user()

    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    if user_id != leader_id:
        return jsonify({
            "error": "Only the current leader can publish"
        }), 403

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
    if authorized_user() is None:
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
