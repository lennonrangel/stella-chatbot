from __future__ import annotations
import random
import logging
from typing import Optional

from backend.bot.bdi_models import (
    Beliefs, Desire, DesireAleatorio, DesireConfirmarFollowup,
    DesireNegar, DesireTema, DesireDesconhecido
)
from backend.bot.intent_classifier import _infer_desire, _TAGS_SORTEAVEIS
from backend.nlp.search_service import INTENTS, get_response_for_tag
from backend.nlp.image_service import buscar_imagem_para_tag, buscar_imagem_para_texto
from backend.llm.fallback_service import query_llm
from backend.db.models import buscar_historico_recente, buscar_ultimo_tema

logger = logging.getLogger(__name__)


def _build_context_summary(beliefs: Beliefs) -> str:
    """Monta resumo do contexto atual para o LLM, incluindo histórico recente."""
    parts = []

    historico = buscar_historico_recente(beliefs.sessao_id, limite=6)
    if historico:
        conversa_str = " | ".join([f"{m['role']}: {m['content']}" for m in historico])
        parts.append(f"Histórico recente: {conversa_str}")

    if beliefs.ultimo_tema:
        parts.append(f"Último tema discutido: {beliefs.ultimo_tema.replace('_', ' ')}")

    return " | ".join(parts) if parts else "Início de conversa."


def _enriquecer_com_imagem_llm(result: dict, beliefs: Beliefs) -> dict:
    """
    Busca imagem Wikipedia para respostas do LLM.
    A imagem deve vir da pergunta atual, não do tema anterior da sessão.
    """
    # Só enriquece respostas do LLM sem imagem
    if result.get("source") != "llm" or result.get("imagem"):
        return result

    imagem_url = None

    # Usa apenas a pergunta atual para evitar reaproveitar imagens do histórico.
    imagem_url = buscar_imagem_para_texto(beliefs.texto_usuario)

    if imagem_url:
        result["imagem"] = [imagem_url]
        logger.info(f"[LLM Image] Imagem associada: {imagem_url}")
    else:
        logger.debug("[LLM Image] Nenhuma imagem encontrada para esta resposta.")

    return result


def _build_llm_response(user_input: str, context: str = "") -> dict:
    """Fallback para o LLM quando a base de conhecimento não tem resposta."""
    llm_text = query_llm(user_input, context=context)

    if not llm_text or "__" in llm_text:
        return _nao_entendeu()

    return {
        "text": llm_text,
        "tag": "llm_fallback",
        "imagem": [],
        "followup_pergunta": None,
        "followup_data": None,
        "source": "llm"
    }


def _execute_intention(desire: Desire, beliefs: Beliefs) -> dict:
    if isinstance(desire, DesireAleatorio):
        candidatos = [t for t in _TAGS_SORTEAVEIS if t != beliefs.ultimo_tema]
        tag = random.choice(candidatos)
        result = get_response_for_tag(tag)
        aberturas = [
            "Vou te surpreender com um tema!\n\n",
            "Deixa comigo, olha isso:\n\n",
            "Olha que interessante:\n\n",
            "Se liga nisso:\n\n",
            "Você vai curtir esse:\n\n",
        ]
        result["text"] = random.choice(aberturas) + result["text"]
        return result

    if isinstance(desire, DesireConfirmarFollowup):
        return get_response_for_tag(desire.proxima_tag, hint=desire.proximo_hint)

    if isinstance(desire, DesireNegar):
        return {
            "text": ("Tudo bem! Sobre o que você quer explorar agora?\n"
                     "Planetas, estrelas, galáxias, buracos negros... é só perguntar."),
            "tag": "default", "imagem": None,
            "followup_pergunta": None, "followup_data": None,
        }

    if isinstance(desire, DesireTema):
        res = get_response_for_tag(desire.tag, hint=desire.hint)

        # Anti-alucinação: superlativos vêm sempre da base de conhecimento
        superlativos = ["maior planeta", "menor planeta", "mais distante",
                        "mais frio", "mais quente", "mais rapido"]
        if desire.hint and any(s in desire.hint for s in superlativos):
            res["source"] = "knowledge_base"

        if not res or res.get("fallback_needed") or not res.get("text"):
            summary = _build_context_summary(beliefs)
            return _build_llm_response(beliefs.texto_usuario, context=summary)
        return res

    if isinstance(desire, DesireDesconhecido):
        if desire.followup_data:
            return _nao_entendeu(desire.followup_data)
        summary = _build_context_summary(beliefs)
        return _build_llm_response(beliefs.texto_usuario, context=summary)

    return _nao_entendeu()


def get_response(user_input: str, sessao_id: str, followup_pendente: Optional[dict] = None) -> dict:
    """Ponto de entrada principal — Arquitetura BDI."""
    if not user_input or not user_input.strip():
        return _nao_entendeu()

    # 1. Beliefs
    beliefs = Beliefs.from_input(user_input, sessao_id, followup_pendente)

    # 2. Desires
    desire = _infer_desire(beliefs)

    logger.debug("[BDI] sessao=%s | lemmas=%s | desire=%s",
                 sessao_id, beliefs.lemmas, desire)

    result = _execute_intention(desire, beliefs)

    # Anti-loop: se resposta idêntica à anterior da base, força LLM
    historico = buscar_historico_recente(sessao_id, limite=1)
    if historico and result.get("text"):
        ultimo_texto = historico[0].get("content", "")
        if (result["text"].strip() == ultimo_texto.strip()
                and result.get("source") == "knowledge_base"):
            logger.info("Resposta repetida detectada. Forçando fallback LLM.")
            summary = _build_context_summary(beliefs)
            result = _build_llm_response(user_input, context=summary)

    # Enriquece respostas do LLM com imagem da Wikipedia
    if result.get("source") == "llm":
        result = _enriquecer_com_imagem_llm(result, beliefs)

    if "source" not in result:
        result["source"] = "knowledge_base"

    # Oculta badge de fonte para saudações e despedidas
    if result.get("tag") in ["saudacao", "despedida"]:
        result["source"] = "system"

    return result


def _nao_entendeu(followup_pendente: Optional[dict] = None) -> dict:
    msgs = [
        "Não entendi o que você perguntou. Tente reformular ou escolha um assunto.",
        "Não entendi o que você quis dizer. Pode tentar explicar de outro jeito?",
        "Hmm, não consegui entender. Quer tentar reformular?",
        "Essa eu não consegui entender. Tenta escrever de um jeito diferente.",
        "Fiquei meio perdido aqui, pode reformular a pergunta?",
    ]
    return {
        "text": random.choice(msgs),
        "tag": "default",
        "imagem": None,
        "followup_pergunta": None,
        "followup_data": followup_pendente if followup_pendente else None,
    }