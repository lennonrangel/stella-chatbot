import uuid
from flask import Blueprint, request, jsonify, send_from_directory
import os

from backend.bot.orchestrator import get_response
from backend.db.models import salvar_sessao, salvar_mensagem, buscar_ultimo_tema

bp = Blueprint("routes", __name__)

FRONTEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))


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

    # Memória de tema: se o LLM respondeu, mantém o último tema válido
    tag_para_memoria = result.get("tag")
    if tag_para_memoria == "llm_fallback":
        ultimo = buscar_ultimo_tema(sessao_id)
        if ultimo:
            tag_para_memoria = ultimo

    salvar_mensagem(sessao_id, "user", user_message)
    salvar_mensagem(sessao_id, "bot", result["text"], tag_para_memoria)

    return jsonify({
        "response": result["text"],
        "imagem": result.get("imagem"),
        "followup_pergunta": result.get("followup_pergunta"),
        "followup_data": result.get("followup_data"),
        "source": result.get("source", "knowledge_base"),
    })


@bp.route("/api/status", methods=["GET"])
def status():
    """Health check — verifica se o backend está operacional."""
    import os
    llm_mode = os.getenv("LLM_MODE", "auto")
    local_model = os.getenv("STELLA_LOCAL_MODEL", "Qwen/Qwen2.5-3B-Instruct")
    remote_model = os.getenv("STELLA_REMOTE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    return jsonify({
        "status": "ok",
        "nlp": "spaCy + RSLP Stemmer",
        "knowledge_base": "Hybrid TF-IDF + Alias Boost",
        "llm_mode": llm_mode,
        "llm_local": local_model,
        "llm_remote": remote_model,
    })
