"""
=======================================================
Arquitetura BDI (Beliefs · Desires · Intentions)
- Beliefs: estado atual da sessão (último tema, followup pendente, histórico recente)
- Desires: intenção do usuário detectada a partir da mensagem
- Intentions: plano de ação escolhido para satisfazer o desejo

NLP: lematização via spaCy (pt_core_news_sm).
=======================================================
"""

from __future__ import annotations

import re
import random
import logging
from dataclasses import dataclass, field
from typing import Optional

import spacy

from backend.models import buscar_ultimo_tema
from backend.intents import INTENTS, get_response_for_tag, get_random_response

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Carregamento do modelo spaCy (lematização)
# ---------------------------------------------------------------------------
try:
    _nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner"])
except OSError:
    raise RuntimeError(
        "Modelo spaCy 'pt_core_news_sm' não encontrado.\n"
        "Execute: python -m spacy download pt_core_news_sm"
    )

# ---------------------------------------------------------------------------
# Stopwords em português
# ---------------------------------------------------------------------------
STOPWORDS: set[str] = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na",
    "por", "para", "com", "que", "e", "eu", "me",
    "meu", "minha", "voce", "te", "se", "seu", "sua",
    "isso", "esse", "essa", "este", "esta", "aqui",
    "mais", "mas", "pra", "pro", "num", "numa", "sobre",
    "qual", "quais", "como", "quando", "onde", "quem",
    "tem", "ha", "ter", "ser", "foi", "sao",
}

# ---------------------------------------------------------------------------
# Vocabulário de resposta afirmativa
# ---------------------------------------------------------------------------
AFIRMATIVAS: set[str] = {
    "sim", "s", "claro", "quero", "pode", "vai", "vamo", "bora",
    "conta", "me conta", "me diz", "quero saber", "com certeza",
    "obvio", "show", "legal", "top", "por favor", "bora la",
    "conte", "me conte", "fale", "fala", "ouvir", "diz", "mais",
    "continua", "continue", "isso", "exato", "perfeito",
}

# ---------------------------------------------------------------------------
# Vocabulário de resposta negativa
# ---------------------------------------------------------------------------
NEGATIVAS: set[str] = {
    "nao", "n", "nope", "deixa", "agora nao",
    "prefiro nao", "outro tema", "outra coisa",
}

# ---------------------------------------------------------------------------
# Tags sorteáveis para pedido de tema aleatório
# ---------------------------------------------------------------------------
_TAGS_SORTEAVEIS: list[str] = [
    "buraco_negro", "constelacoes", "signos", "estrelas", "supernova",
    "estrela_neutrons", "nebulosa", "galaxias", "big_bang", "destino_universo",
    "materia_escura", "sistema_solar", "sol", "mercurio", "venus", "terra",
    "lua", "marte", "jupiter", "saturno", "urano", "netuno", "plutao",
    "exoplanetas", "vida_extraterrestre", "cometas_asteroides",
    "espaco_tempo", "ano_luz", "spacex",
]

_GATILHOS_ALEATORIO: set[str] = {
    "aleatorio", "aleatoria", "surpresa", "surpreenda", "surpreende",
    "qualquer", "escolha", "escolhe", "tanto faz", "qualquer coisa",
    "qualquer tema", "me surpreenda", "me surpreende", "algo aleatorio",
    "tema aleatorio", "fala qualquer coisa", "fala alguma coisa",
    "me conta algo", "me conte algo", "o que quiser", "livre",
}

# ---------------------------------------------------------------------------
# Mapeamentos de posição ordinal e superlativos de planetas
# ---------------------------------------------------------------------------
_POSICAO_PLANETA: dict[str, str] = {
    "primeiro": "mercurio", "1": "mercurio",
    "segundo":  "venus",    "2": "venus",
    "terceiro": "terra",    "3": "terra",
    "quarto":   "marte",    "4": "marte",
    "quinto":   "jupiter",  "5": "jupiter",
    "sexto":    "saturno",  "6": "saturno",
    "setimo":   "urano",    "7": "urano",
    "oitavo":   "netuno",   "8": "netuno",
}

_SUPERLATIVO_PLANETA: list[tuple[set[str], str, str]] = [
    # Mercúrio
    ({"proximo do sol", "mais proximo do sol", "mais perto do sol", "perto do sol", "planeta proximo ao sol"}, "mercurio", "mais proximo do sol"),
    ({"menor planeta", "menor do sistema", "menor de todos"}, "mercurio", "menor planeta"),
    ({"planeta mais rapido", "planeta mais veloz"}, "mercurio", "mais rapido"),
    # Vênus
    ({"mais quente", "planeta mais quente"}, "venus", "mais quente"),
    ({"planeta mais brilhante", "planeta mais luminoso"}, "venus", "planeta mais brilhante"),
    ({"planeta mais tóxico"}, "venus", "planeta mais tóxico"),
    # Terra
    ({"sobre a terra", "sobre a nossa planeta"}, "terra", "nosso planeta"),
    # Marte
    ({"mais parecido com a terra", "planeta parecido com a terra"}, "marte", "planeta vermelho"),
    # Júpiter
    ({"maior planeta", "maior do sistema", "maior de todos"}, "jupiter", "maior planeta"),
    # Saturno
    ({"mais luas", "planeta com mais luas", "tem mais luas"}, "saturno", "mais luas"),
    # Urano
    ({"mais frio", "planeta mais frio", "mais gelado"}, "urano", "mais frio"),
    # Netuno
    ({"mais distante", "mais distante do sol", "mais longe do sol", "longe do sol", "distante do sol"}, "netuno", "mais distante do sol"),
    ({"mais lento", "planeta mais lento"}, "netuno", "mais lento")
]

# ---------------------------------------------------------------------------
# Utilitários de texto
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Remove acentos e converte para minúsculas."""
    replacements = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e", "í": "i", "ó": "o",
        "ô": "o", "õ": "o", "ú": "u", "ü": "u",
        "ç": "c",
    }
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    return text


def _lemmatize(text: str) -> list[str]:
    """
    Lematiza o texto usando spaCy (pt_core_news_sm).

    Diferença em relação à stemização RSLP anterior:
    - Stemização corta sufixos mecanicamente (ex.: "estrelas" → "estrel")
    - Lematização retorna a forma canônica do dicionário
      (ex.: "estrelas" → "estrela", "correndo" → "correr")
    Isso melhora a precisão do matching, pois a forma lema é mais legível
    e semanticamente correta.
    """
    normalized = _normalize(text.lower())
    doc = _nlp(normalized)
    return [
        token.lemma_
        for token in doc
        if token.is_alpha
        and len(token.lemma_) >= 2
        and token.lemma_ not in STOPWORDS
        and not token.is_stop
    ]


# ---------------------------------------------------------------------------
# Índice invertido de padrões (reconstruído com lemas)
# ---------------------------------------------------------------------------

def _build_pattern_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for intent in INTENTS:
        if intent["tag"] == "default":
            continue
        for pattern in intent["patterns"]:
            for lemma in _lemmatize(pattern):
                if lemma not in index:
                    index[lemma] = []
                if intent["tag"] not in index[lemma]:
                    index[lemma].append(intent["tag"])
    return index


_PATTERN_INDEX: dict[str, list[str]] = _build_pattern_index()


def _score_intents(lemmas: list[str]) -> dict[str, int]:
    scores: dict[str, int] = {}
    for lemma in lemmas:
        for tag in _PATTERN_INDEX.get(lemma, []):
            scores[tag] = scores.get(tag, 0) + 1
    return scores


# ===========================================================================
# ARQUITETURA BDI
# ===========================================================================

# ---------------------------------------------------------------------------
# BELIEFS – estado de crença sobre a sessão atual
# ---------------------------------------------------------------------------

@dataclass
class Beliefs:

    sessao_id: str #identificador único da sessão
    ultimo_tema: Optional[str] # última tag respondida pelo bot (vinda do banco)
    followup_data: Optional[dict] # dict com {pergunta, proxima_tag, proximo_hint} ou None
    texto_usuario: str # mensagem bruta do usuário
    texto_norm: str # mensagem normalizada (sem acentos, minúscula)
    lemmas: list[str] = field(default_factory=list) # lista de lemas extraídos pelo spaCy

    @classmethod
    def from_input(cls, user_input: str, sessao_id: str,
                   followup_pendente: Optional[dict]) -> "Beliefs":
        texto_norm = _normalize(user_input.lower().strip())
        lemmas = _lemmatize(user_input)
        ultimo_tema = buscar_ultimo_tema(sessao_id)
        return cls(
            sessao_id=sessao_id,
            ultimo_tema=ultimo_tema,
            followup_data=followup_pendente,
            texto_usuario=user_input,
            texto_norm=texto_norm,
            lemmas=lemmas,
        )


# ---------------------------------------------------------------------------
# DESIRES – intenção do usuário (o que ele quer)
# ---------------------------------------------------------------------------

class Desire:
    """Classe base para representar um desejo detectado."""
    pass


@dataclass
class DesireAleatorio(Desire):
    """Usuário quer um tema surpresa."""
    pass


@dataclass
class DesireConfirmarFollowup(Desire):
    """Usuário confirmou o followup pendente (afirmativa sem tema novo)."""
    proxima_tag: str
    proximo_hint: Optional[str]


@dataclass
class DesireNegar(Desire):
    """Usuário rejeitou o followup ou não quer continuar no tema."""
    pass


@dataclass
class DesireTema(Desire):
    """Usuário quer saber sobre um tema específico."""
    tag: str
    hint: Optional[str] = None


@dataclass
class DesireDesconhecido(Desire):
    """Não foi possível detectar intenção clara."""
    followup_data: Optional[dict] = None


# ---------------------------------------------------------------------------
# Funções de detecção auxiliares (usadas na fase de Desires)
# ---------------------------------------------------------------------------

def _is_afirmativa(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & AFIRMATIVAS)


def _is_negativa(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & NEGATIVAS)


def _is_aleatorio(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & _GATILHOS_ALEATORIO)


def _detect_posicao(text: str) -> Optional[str]:
    normalized = _normalize(text.lower())
    palavras_planeta = {"planeta", "sistema", "solar", "orbita", "sol"}
    if not set(re.findall(r"[a-z]+", normalized)) & palavras_planeta:
        return None
    for palavra, tag in _POSICAO_PLANETA.items():
        if palavra in normalized:
            return tag
    return None


def _detect_superlativo(text: str) -> Optional[tuple[str, str]]:
    normalized = _normalize(text.lower())
    for gatilhos, tag, hint in _SUPERLATIVO_PLANETA:
        for gatilho in gatilhos:
            if gatilho in normalized:
                return tag, hint
    return None


def _classify(lemmas: list[str]) -> Optional[str]:
    """Classifica a intenção pelo maior score de lemas no índice."""
    scores = _score_intents(lemmas)
    if not scores:
        return None
    melhor_tag = max(scores, key=lambda t: scores[t])
    return melhor_tag if scores[melhor_tag] >= 1 else None


# ---------------------------------------------------------------------------
# Fase 1 – BELIEFS → DESIRES  (percepção e inferência de intenção)
# ---------------------------------------------------------------------------

def _infer_desire(beliefs: Beliefs) -> Desire:
    """Analisa as crenças e infere o desejo do usuário."""
    text = beliefs.texto_usuario

    # 1. Pedido aleatório
    if _is_aleatorio(text):
        return DesireAleatorio()

    # 2. Resposta a followup pendente (afirmativa / negativa / novo tema)
    if beliefs.followup_data:
        proxima_tag = beliefs.followup_data.get("proxima_tag")
        if proxima_tag:
            if _is_negativa(text):
                return DesireNegar()

            tag_detectada = _classify(beliefs.lemmas)

            # Afirmativa pura → confirma followup
            if _is_afirmativa(text) and tag_detectada is None:
                return DesireConfirmarFollowup(
                    proxima_tag=proxima_tag,
                    proximo_hint=beliefs.followup_data.get("proximo_hint"),
                )

            # Usuário mudou de tema no meio do followup
            if tag_detectada:
                return DesireTema(tag=tag_detectada, hint=beliefs.texto_norm)

            # Não entendeu, mas mantém followup
            return DesireDesconhecido(followup_data=beliefs.followup_data)

    # 3. Posição ordinal de planeta
    tag_posicao = _detect_posicao(text)
    if tag_posicao:
        return DesireTema(tag=tag_posicao, hint=beliefs.texto_norm)

    # 4. Superlativo de planeta
    superlativo = _detect_superlativo(text)
    if superlativo:
        tag_sup, hint_sup = superlativo
        return DesireTema(tag=tag_sup, hint=hint_sup)

    # 5. Classificador geral por lemas
    tag = _classify(beliefs.lemmas)
    if tag:
        return DesireTema(tag=tag, hint=beliefs.texto_norm)

    # 6. Desconhecido
    return DesireDesconhecido()


# ---------------------------------------------------------------------------
# Fase 2 – DESIRES → INTENTIONS (seleção e execução do plano)
# ---------------------------------------------------------------------------

def _execute_intention(desire: Desire, beliefs: Beliefs) -> dict:

    # Intenção: responder com tema aleatório
    if isinstance(desire, DesireAleatorio):
        candidatos = [t for t in _TAGS_SORTEAVEIS if t != beliefs.ultimo_tema]
        tag_escolhida = random.choice(candidatos)
        resultado = get_response_for_tag(tag_escolhida)
        aberturas = [
            "Vou te surpreender com um tema!\n\n",
            "Deixa comigo, olha isso:\n\n",
            "Olha que interessante:\n\n",
            "Esse é interessante:\n\n",
            "Se liga nisso:\n\n",
            "Você vai curtir esse:\n\n",
            "Esse aqui é bem interessante:\n\n",
            "Esse aqui é bem maneiro:\n\n",
        ]
        resultado["text"] = random.choice(aberturas) + resultado["text"]
        return resultado

    # Intenção: confirmar followup e responder próxima tag
    if isinstance(desire, DesireConfirmarFollowup):
        return get_response_for_tag(
            desire.proxima_tag,
            hint=desire.proximo_hint,
        )

    # Intenção: rejeitar followup e abrir novo tema
    if isinstance(desire, DesireNegar):
        return {
            "text": (
                "Tudo bem! Sobre o que você quer explorar agora?\n"
                "Planetas, estrelas, galáxias, buracos negros... é só perguntar."
            ),
            "tag": "default",
            "imagem": None,
            "followup_pergunta": None,
            "followup_data": None,
        }

    # Intenção: responder tema específico
    if isinstance(desire, DesireTema):
        return get_response_for_tag(desire.tag, hint=desire.hint)

    # Intenção: não entendeu — retornar mensagem de fallback
    if isinstance(desire, DesireDesconhecido):
        return _nao_entendeu(desire.followup_data)

    # Segurança — não deveria chegar aqui
    return _nao_entendeu()


# ---------------------------------------------------------------------------
# Interface pública
# ---------------------------------------------------------------------------

def get_response(user_input: str, sessao_id: str,
                 followup_pendente: Optional[dict] = None) -> dict:
  
    if not user_input or not user_input.strip():
        return _nao_entendeu(followup_pendente)

    # --- Constrói Beliefs a partir da entrada e do banco de dados. ---
    beliefs = Beliefs.from_input(user_input, sessao_id, followup_pendente)

    # --- Infere o Desire do usuário com _infer_desire(). ---
    desire = _infer_desire(beliefs)

    logger.debug(
        "[BDI] sessao=%s | lemmas=%s | desire=%s",
        sessao_id, beliefs.lemmas, desire,
    )

    # --- Executa a Intention correspondente com _execute_intention(). ---
    return _execute_intention(desire, beliefs)


# ---------------------------------------------------------------------------
# Fallback padrão
# ---------------------------------------------------------------------------

def _nao_entendeu(followup_pendente: Optional[dict] = None) -> dict:
    respostas = [
        "Não entendi o que você perguntou. Tente reformular ou escolha um assunto.",
        "Não entendi o que você quis dizer. Pode tentar explicar de outro jeito?",
        "Hmm, não consegui entender. Quer tentar reformular?",
        "Essa eu não consegui entender. Tenta escrever de um jeito diferente.",
        "Fiquei meio perdido aqui, pode reformular a pergunta?",
    ]
    return {
        "text": random.choice(respostas),
        "tag": "default",
        "imagem": None,
        "followup_pergunta": None,
        "followup_data": followup_pendente if followup_pendente else None,
    }
