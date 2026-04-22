import re
import random
import nltk
from nltk.stem import RSLPStemmer
from backend.models import buscar_ultimo_tema
from backend.intents import INTENTS, get_response_for_tag, get_random_response

for resource in ("rslp", "punkt", "punkt_tab"):
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

try:
    _stemmer = RSLPStemmer()
except Exception:
    _stemmer = None

STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na",
    "por", "para", "com", "que", "e", "eu", "me",
    "meu", "minha", "voce", "te", "se", "seu", "sua",
    "isso", "esse", "essa", "este", "esta", "aqui",
    "mais", "mas", "pra", "pro", "num", "numa", "sobre",
    "qual", "quais", "como", "quando", "onde", "quem",
    "tem", "ha", "ter", "ser", "foi", "sao"
}

AFIRMATIVAS = {
    "sim", "s", "claro", "quero", "pode", "vai", "vamo", "bora",
    "conta", "me conta", "me diz", "quero saber", "com certeza",
    "obvio", "show", "legal", "top", "por favor",
    "conte", "me conte", "fale", "fala", "ouvir", "diz", "mais",
    "continua", "continue", "isso", "exato", "perfeito"
}

NEGATIVAS = {
    "nao", "n", "nope", "deixa", "agora nao",
    "prefiro nao", "outro tema", "outra coisa"
}

_TAGS_SORTEAVEIS = [
    "buraco_negro", "estrelas", "constelacoes", "signos", "supernova", "estrela_neutrons", "galaxias", "big_bang", "destino_universo", "materia_escura", "sol", "mercurio", "venus", "terra", "marte", 
    "jupiter", "saturno", "urano", "netuno", "plutao", "lua", 
    "exoplanetas", "vida_extraterrestre", "cometas_asteroides", 
    "espaco_tempo", "ano_luz", "sistema_solar"
]

_GATILHOS_ALEATORIO = {
    "aleatorio", "aleatoria", "surpresa", "surpreenda", "surpreende",
    "qualquer", "escolha", "escolhe", "tanto faz", "qualquer coisa",
    "qualquer tema", "me surpreenda", "me surpreende", "algo aleatorio",
    "tema aleatorio", "fala qualquer coisa", "fala alguma coisa",
    "me conta algo", "me conte algo", "o que quiser", "livre"
}

_POSICAO_PLANETA = {
    "primeiro": "mercurio", "1": "mercurio",
    "segundo":  "venus",    "2": "venus",
    "terceiro": "terra",    "3": "terra",
    "quarto":   "marte",    "4": "marte",
    "quinto":   "jupiter",  "5": "jupiter",
    "sexto":    "saturno",  "6": "saturno",
    "setimo":   "urano",    "7": "urano",
    "oitavo":   "netuno",   "8": "netuno",
}


def _normalize(text: str) -> str:
    replacements = {
        "\u00e1": "a", "\u00e0": "a", "\u00e3": "a", "\u00e2": "a",
        "\u00e9": "e", "\u00ea": "e", "\u00ed": "i", "\u00f3": "o",
        "\u00f4": "o", "\u00f5": "o", "\u00fa": "u", "\u00fc": "u",
        "\u00e7": "c"
    }
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    return text


def _stem(word: str) -> str:
    if _stemmer is None:
        return word
    try:
        return _stemmer.stem(word)
    except Exception:
        return word


def _tokenize_and_stem(text: str) -> list:
    normalized = _normalize(text.lower())
    tokens = re.findall(r"[a-z]{2,}", normalized)
    return [_stem(t) for t in tokens if t not in STOPWORDS]


def _build_pattern_index() -> dict:
    index = {}
    for intent in INTENTS:
        if intent["tag"] == "default":
            continue
        for pattern in intent["patterns"]:
            for token in _tokenize_and_stem(pattern):
                if token not in index:
                    index[token] = []
                if intent["tag"] not in index[token]:
                    index[token].append(intent["tag"])
    return index


_PATTERN_INDEX = _build_pattern_index()


def _score_intents(tokens: list) -> dict:
    scores = {}
    for token in tokens:
        for tag in _PATTERN_INDEX.get(token, []):
            scores[tag] = scores.get(tag, 0) + 1
    return scores


def _is_afirmativa(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & AFIRMATIVAS)


def _is_negativa(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & NEGATIVAS)


def _is_aleatorio(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", _normalize(text.lower().strip())))
    return bool(tokens & _GATILHOS_ALEATORIO)


def _detect_posicao(text: str):
    normalized = _normalize(text.lower())
    palavras_planeta = {"planeta", "sistema", "solar", "orbita", "sol"}
    if not set(re.findall(r"[a-z]+", normalized)) & palavras_planeta:
        return None
    for palavra, tag in _POSICAO_PLANETA.items():
        if palavra in normalized:
            return tag
    return None


def get_response(user_input: str, sessao_id: str, followup_pendente=None) -> dict:
    if not user_input or not user_input.strip():
        return get_random_response("default")

    texto_norm = _normalize(user_input.lower().strip())

    # Trata followup pendente
    if followup_pendente is not None:
        proxima_tag = followup_pendente.get("proxima_tag")
        if proxima_tag:
            if _is_afirmativa(user_input):
                return get_response_for_tag(
                    proxima_tag,
                    hint=followup_pendente.get("proximo_hint")
                )
            if _is_negativa(user_input):
                return {
                    "text": "Tudo bem! Sobre o que você quer explorar agora?\nPlanetas, estrelas, galáxias, buracos negros... é só perguntar.",
                    "tag": "default",
                    "imagem": None,
                    "followup_pergunta": None,
                    "followup_data": None
                }

    # Pedido de tema aleatório
    if _is_aleatorio(user_input):
        ultimo_tema = buscar_ultimo_tema(sessao_id)
        candidatos = [t for t in _TAGS_SORTEAVEIS if t != ultimo_tema]
        resultado = get_response_for_tag(random.choice(candidatos))
        resultado["text"] = "Vou te surpreender com um tema!\n\n" + resultado["text"]
        return resultado

    # Detecção de posição ordinal (primeiro, segundo... planeta)
    tag_posicao = _detect_posicao(user_input)
    if tag_posicao:
        return get_response_for_tag(tag_posicao, hint=texto_norm)

    # Pipeline normal
    tokens = _tokenize_and_stem(user_input)
    if not tokens:
        return get_random_response("default")

    scores = _score_intents(tokens)
    if scores:
        best_tag = max(scores, key=lambda t: scores[t])
        return get_response_for_tag(best_tag, hint=texto_norm)

    # Fallback: usa último tema se não havia followup pendente
    if followup_pendente is None:
        ultimo_tema = buscar_ultimo_tema(sessao_id)
        if ultimo_tema:
            return get_response_for_tag(ultimo_tema, hint=texto_norm)

    return get_random_response("default")
