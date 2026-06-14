from __future__ import annotations

import logging
import os
import torch
import requests
from transformers import pipeline

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#  MODO DE OPERAÇÃO — defina no .env:
#
#    LLM_MODE=remoto   → usa HF Inference Providers (router.huggingface.co)
#                        requer HF_TOKEN, consome créditos gratuitos mensais
#
#    LLM_MODE=local    → baixa e roda o modelo na sua máquina (GPU/CPU)
#                        sem internet, sem créditos, sem API key
#
#    LLM_MODE=auto     → tenta remoto primeiro; se falhar, usa local
#                        (padrão se não definido)
# ═══════════════════════════════════════════════════════════════════════════════
LLM_MODE = os.getenv("LLM_MODE", "auto").lower()

# ─── Modelo REMOTO (HF Inference Providers) ───────────────────────────────────
HF_TOKEN      = os.getenv("HF_TOKEN")
REMOTE_MODEL  = os.getenv("STELLA_REMOTE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
HF_API_URL    = "https://router.huggingface.co/v1/chat/completions"

# ─── Modelo LOCAL ─────────────────────────────────────────────────────────────
# Baixado automaticamente na 1ª execução e salvo em cache.
# Troque conforme sua RAM/VRAM:
#   "Qwen/Qwen2.5-1.5B-Instruct"  → ~2 GB RAM  (PC fraco)
#   "Qwen/Qwen2.5-3B-Instruct"    → ~5 GB RAM  (recomendado CPU)
#   "Qwen/Qwen2.5-7B-Instruct"    → ~9 GB VRAM (recomendado GPU)
LOCAL_MODEL = os.getenv("STELLA_LOCAL_MODEL", "Qwen/Qwen2.5-3B-Instruct")

_pipe = None

# ─── Prompt de Sistema: Enciclopédia Cósmica ──────────────────────────────────
SYSTEM_PROMPT = (
    "Você é Stella, assistente especializada em astronomia e ciências espaciais. "
    "Sua missão é ser uma ENCICLOPÉDIA CÓSMICA: precisa, didática e fascinante, "
    "mas também pode responder perguntas gerais fora desse tema com a mesma honestidade.\n"
    "REGRAS:\n"
    "- Responda APENAS com fatos científicos verificados e precisos.\n"
    "- Datas, distâncias e medidas devem ser EXATOS. "
    "Ex: A Apollo 11 pousou em 20 de julho de 1969. Júpiter tem 318 massas terrestres.\n"
    "- Linguagem acessível, parágrafos curtos. Português Brasileiro.\n"
    "- JAMAIS invente dados. Se não tiver certeza, diga claramente que não sabe ou peça contexto.\n"
    "- Se a pergunta fugir de astronomia, responda normalmente sem forçar conexão com o cosmos.\n"
    "- NÃO repita a pergunta do usuário.\n"
    "- NÃO use saudações formais nem despedidas longas.\n"
    "- NÃO use títulos com asteriscos (ex: *Título*)."
)

# ═══════════════════════════════════════════════════════════════════════════════
#  UTILITÁRIOS
# ═══════════════════════════════════════════════════════════════════════════════

def _ensure_complete_sentence(text: str) -> str:
    """Garante que o texto termine em pontuação final."""
    if not text:
        return text
    last_punct = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
    if last_punct != -1 and last_punct > len(text) * 0.75:
        return text[: last_punct + 1]
    return text

# ═══════════════════════════════════════════════════════════════════════════════
#  MODO REMOTO — HF Inference Providers
#  Endpoint: router.huggingface.co/v1/chat/completions (API OpenAI-compatible)
#  Créditos gratuitos mensais: ~$0.10 (conta free) | ~$2.00 (conta PRO)
#  Acompanhe o consumo em: https://huggingface.co/settings/billing
# ═══════════════════════════════════════════════════════════════════════════════

def _query_hf_remote(user_message: str, context: str = "") -> str | None:
    if not HF_TOKEN:
        logger.warning("HF_TOKEN ausente — pulando modo remoto.")
        return None

    user_content = (
        f"Contexto da conversa: {context}\nPergunta: {user_message}"
        if context else user_message
    )

    payload = {
        "model": REMOTE_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_content},
        ],
        "max_tokens": 700,
        "temperature": 0.3,
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        logger.info(f"[REMOTO] Resposta via HF Inference Providers ({REMOTE_MODEL}).")
        return _ensure_complete_sentence(text)

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 402:
            logger.warning("[REMOTO] Créditos HF esgotados (402). Usando modelo local.")
        else:
            logger.warning(f"[REMOTO] HTTP {status}: {e.response.text[:200]}")
        return None
    except Exception as e:
        logger.warning(f"[REMOTO] HF Inference Providers falhou: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
#  MODO LOCAL — modelo rodando na sua máquina
#  GPU (CUDA) detectada automaticamente — instale o torch com CUDA para ativar:
#    pip install torch --index-url https://download.pytorch.org/whl/cu124
# ═══════════════════════════════════════════════════════════════════════════════

def _get_pipeline():
    global _pipe
    if _pipe is None:
        use_gpu = torch.cuda.is_available()
        logger.info(f"[LOCAL] Carregando modelo: {LOCAL_MODEL} | GPU: {use_gpu}")
        logger.info("[LOCAL] (O download ocorre apenas na primeira execução)")
        _pipe = pipeline(
            "text-generation",
            model=LOCAL_MODEL,
            dtype=torch.bfloat16 if use_gpu else torch.float32,
            device_map="auto" if use_gpu else None,
        )
        logger.info(f"[LOCAL] Modelo '{LOCAL_MODEL}' pronto.")
    return _pipe


def _query_llm_local(user_message: str, context: str = "") -> str:
    user_content = (
        f"Contexto da conversa: {context}\nPergunta: {user_message}"
        if context else user_message
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_content},
    ]

    try:
        pipe = _get_pipeline()
        outputs = pipe(
            messages,
            max_new_tokens=600,
            temperature=0.3,
            do_sample=True,
            pad_token_id=pipe.tokenizer.eos_token_id,
            generation_config=None,
        )
        text = outputs[0]["generated_text"][-1]["content"].strip()
        logger.info(f"[LOCAL] Resposta via modelo local ({LOCAL_MODEL}).")
        return _ensure_complete_sentence(text)

    except Exception as e:
        logger.error(f"[LOCAL] Erro na inferência local: {e}")
        return "Não consegui processar sua pergunta agora. Tente novamente!"

# ═══════════════════════════════════════════════════════════════════════════════
#  INTERFACE PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════════

def query_llm(user_message: str, context: str = "") -> str:
    """
    Modos de operação (definido por LLM_MODE no .env):

      auto   → tenta remoto (HF); se falhar usa local        [padrão]
      remoto → somente HF Inference Providers
      local  → somente modelo local (sem internet)
    """
    if LLM_MODE == "remoto":
        result = _query_hf_remote(user_message, context)
        return result if result else "Serviço remoto indisponível. Verifique o HF_TOKEN ou os créditos."

    if LLM_MODE == "local":
        return _query_llm_local(user_message, context)

    # auto: remoto com fallback local
    result = _query_hf_remote(user_message, context)
    if result:
        return result

    logger.warning("[AUTO] Remoto indisponível. Usando modelo local.")
    return _query_llm_local(user_message, context)
