import uuid
from flask import Blueprint, request, jsonify, send_from_directory
import os

from backend.chatbot import get_response
from backend.models import salvar_sessao, salvar_mensagem

bp = Blueprint("routes", __name__)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


@bp.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@bp.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@bp.route("/api/welcome", methods=["POST"])
def welcome():
    data = request.get_json(silent=True) or {}
    sessao_id = data.get("sessao_id") or str(uuid.uuid4())
    salvar_sessao(sessao_id)
    return jsonify({"sessao_id": sessao_id})


@bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Campo 'message' obrigatório."}), 400

    user_message = str(data["message"]).strip()
    sessao_id = data.get("sessao_id")
    followup_pendente = data.get("followup_pendente")

    if not sessao_id:
        return jsonify({"error": "Campo 'sessao_id' obrigatório."}), 400

    if len(user_message) > 500:
        return jsonify({"error": "Mensagem muito longa."}), 400

    result = get_response(user_message, sessao_id, followup_pendente)

    salvar_mensagem(sessao_id, "user", user_message)
    salvar_mensagem(sessao_id, "bot", result["text"], result["tag"])

    return jsonify({
        "response": result["text"],
        "imagem": result.get("imagem"),
        "followup_pergunta": result.get("followup_pergunta"),
        "followup_data": result.get("followup_data")
    })
