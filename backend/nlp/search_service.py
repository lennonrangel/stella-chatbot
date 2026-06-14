from __future__ import annotations
import math
from typing import Optional
from backend.nlp.text_utils import _tokenize, _normalize
from backend.nlp.indexer import _CORPUS, _DOC_VECTORS, _compute_tf, _tfidf_vector, _TAG_ALIASES, INTENTS

def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    comum = set(a) & set(b)
    if not comum:
        return 0.0
    dot = sum(a[t] * b[t] for t in comum)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def search(query: str, threshold: float = 0.12) -> Optional[dict]:
    """
    Busca HÍBRIDA:
    1. Tenta encontrar match exato ou forte via aliases/tags (Prioridade Máxima).
    2. Usa TF-IDF + Cosseno para similaridade semântica (Prioridade Média).
    3. Retorna None para acionar LLM se a confiança for baixa.
    """
    tokens = _tokenize(query)
    if not tokens:
        return None

    query_tf = _compute_tf(tokens)
    query_vec = _tfidf_vector(query_tf)
    query_norm = _normalize(query)

    best_score = 0.0
    best_doc = None

    for doc, doc_vec in zip(_CORPUS, _DOC_VECTORS):
        score = _cosine(query_vec, doc_vec)

        # BOOST MASSIVO: Se o nome da tag ou um alias exato aparecer (Modelo Híbrido)
        tag_norm = _normalize(doc.tag.replace("_", " "))
        if tag_norm in query_norm:
            score += 1.0  # Garante que essa tag vença o TF-IDF comum

        for alias in _TAG_ALIASES.get(doc.tag, []):
            if _normalize(alias) in query_norm:
                score += 0.8
                break

        if score > best_score:
            best_score = score
            best_doc = doc

    # Se o score for muito baixo, admitimos que não sabemos e deixamos para o LLM
    if best_doc is None or best_score < threshold:
        return None

    return {
        "tag": best_doc.tag,
        "texto": best_doc.texto,
        "imagem": best_doc.imagem,
        "followup": best_doc.followup,
        "score": best_score,
    }

def search_by_tag(tag: str, hint: Optional[str] = None) -> Optional[dict]:
    """
    Retorna um bloco de conteúdo de uma tag específica.
    """
    docs = [doc for doc in _CORPUS if doc.tag == tag]
    if not docs:
        return None

    if hint:
        hint_norm = _normalize(hint)
        
        # 1. Match direto por palavra-chave (Prioridade 1)
        for doc in docs:
            if hint_norm in _normalize(doc.texto):
                return {
                    "tag": doc.tag,
                    "texto": doc.texto,
                    "imagem": doc.imagem,
                    "followup": doc.followup,
                    "score": 2.0,
                }

        # 2. Similaridade TF-IDF (Prioridade 2)
        tokens = _tokenize(hint)
        if tokens:
            query_tf = _compute_tf(tokens)
            query_vec = _tfidf_vector(query_tf)
            best_score = -1.0
            best_doc = None
            for doc in docs:
                doc_vec = _tfidf_vector(doc.tf)
                score = _cosine(query_vec, doc_vec)
                if score > best_score:
                    best_score = score
                    best_doc = doc
            
            # Limiar para evitar respostas que apenas "parecem" mas não são o que foi pedido
            if best_doc and best_score > 0.18:
                return {
                    "tag": best_doc.tag,
                    "texto": best_doc.texto,
                    "imagem": best_doc.imagem,
                    "followup": best_doc.followup,
                    "score": best_score,
                }

    # Se houve um hint mas nada foi bom o suficiente, retorna None -> LLM Fallback
    if hint:
        return None

    # Fallback para o primeiro bloco sem hint (ex: ao clicar num menu)
    doc = docs[0]
    return {
        "tag": doc.tag,
        "texto": doc.texto,
        "imagem": doc.imagem,
        "followup": doc.followup,
        "score": 1.0,
    }

def get_response_for_tag(tag: str, hint: str | None = None) -> dict:
    """
    Busca a resposta para uma tag específica usando a busca aprimorada.
    """
    result = search_by_tag(tag, hint)
    if result:
        return {
            "text": result["texto"],
            "tag": result["tag"],
            "imagem": result.get("imagem"),
            "source": "knowledge_base"
        }

    # Se a busca refinada falhou (especialmente com hint), sinaliza fallback imediato
    if hint:
        return {
            "fallback_needed": True,
            "text": None,
            "tag": tag,
            "source": "llm"
        }

    # Fallback manual apenas para navegação sem pergunta específica (ex: menus)
    for intent in INTENTS:
        if intent["tag"] == tag:
            chosen = intent["responses"][0] if intent["responses"] else {}
            return {
                "text": chosen.get("texto", ""),
                "tag": intent["tag"],
                "imagem": chosen.get("imagem"),
                "source": "knowledge_base"
            }

    return {
        "fallback_needed": True,
        "text": None,
        "tag": "default"
    }
