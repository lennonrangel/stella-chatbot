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
    "obvio", "show", "legal", "top", "por favor", "bora la",
    "conte", "me conte", "fale", "fala", "ouvir", "diz", "mais",
    "continua", "continue", "isso", "exato", "perfeito"
}

NEGATIVAS = {
    "nao", "n", "nope", "deixa", "agora nao",
    "prefiro nao", "outro tema", "outra coisa"
}

_TAGS_SORTEAVEIS = [
    "buraco_negro", "constelacoes", "signos", "estrelas", "supernova", "estrela_neutrons", "nebulosa", "galaxias", "big_bang", "destino_universo", "materia_escura", "sistema_solar", "sol", "mercurio", "venus", "terra", "lua", "marte", "jupiter", "saturno", "urano", "netuno", "plutao", 
    "exoplanetas", "vida_extraterrestre", "cometas_asteroides", 
    "espaco_tempo", "ano_luz", "spacex"
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

_SUPERLATIVO_PLANETA = [
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
    ({"mais anéis", "planeta com mais aneis", "planeta com mais anéis"}, "saturno", "mais aneis"),
    # Urano
    ({"mais frio", "planeta mais frio", "mais gelado"}, "urano", "mais frio"),
    # Netuno
    ({"mais distante", "mais distante do sol", "mais longe do sol", "longe do sol", "distante do sol"}, "netuno", "mais distante do sol"),
    ({"mais lento", "planeta mais lento"}, "netuno", "mais lento")
]


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
 
 
def _classify(text: str):
    tokens = _tokenize_and_stem(text)
    scores = _score_intents(tokens)
    if not scores:
        return None
    melhor_tag = max(scores, key=lambda t: scores[t])
    return melhor_tag if scores[melhor_tag] >= 1 else None


def _detect_superlativo(text: str):
    normalized = _normalize(text.lower())
    for gatilhos, tag, hint in _SUPERLATIVO_PLANETA:
        for gatilho in gatilhos:
            if gatilho in normalized:
                return tag, hint
    return None


def get_response(user_input: str, sessao_id: str, followup_pendente=None) -> dict:
    if not user_input or not user_input.strip():
        return _nao_entendeu(followup_pendente)
 
    texto_norm = _normalize(user_input.lower().strip())
 
    # 1. Pedido de tema aleatório
    if _is_aleatorio(user_input):
        ultimo_tema = buscar_ultimo_tema(sessao_id)
        candidatos = [t for t in _TAGS_SORTEAVEIS if t != ultimo_tema]
        resultado = get_response_for_tag(random.choice(candidatos))
        resultado["text"] = "Vou te surpreender com um tema!\n\n" + resultado["text"]
        return resultado
 
    # 2. Followup pendente
    if followup_pendente is not None:
        proxima_tag = followup_pendente.get("proxima_tag")
        if proxima_tag:
            tag_detectada = _classify(user_input)
 
            if _is_negativa(user_input):
                return {
                    "text": "Tudo bem! Sobre o que você quer explorar agora?\nPlanetas, estrelas, galáxias, buracos negros... é só perguntar.",
                    "tag": "default",
                    "imagem": None,
                    "followup_pergunta": None,
                    "followup_data": None
                }
 
            # Afirmativa sem tema → confirma followup
            if _is_afirmativa(user_input) and tag_detectada is None:
                return get_response_for_tag(
                    proxima_tag,
                    hint=followup_pendente.get("proximo_hint")
                )
 
            # Tem tema próprio → ignora followup e responde o tema
            if tag_detectada:
                return get_response_for_tag(tag_detectada, hint=texto_norm)
 
            # Não entendeu mas havia followup → devolve followup intacto
            return _nao_entendeu(followup_pendente)
 
    # 3. Detecção de posição ordinal (primeiro, segundo... planeta)
    tag_posicao = _detect_posicao(user_input)
    if tag_posicao:
        return get_response_for_tag(tag_posicao, hint=texto_norm)

    # 4. Detecção de superlativo (mais próximo, mais distante, maior, menor...)
    superlativo = _detect_superlativo(user_input)
    if superlativo:
        tag_sup, hint_sup = superlativo
        return get_response_for_tag(tag_sup, hint=hint_sup)

    # 5. Classificador principal por soma de scores de frases
    tag = _classify(user_input)
    if tag:
        return get_response_for_tag(tag, hint=texto_norm)

    # 6. Não entendeu nada
    return _nao_entendeu()
 

def _nao_entendeu(followup_pendente=None) -> dict:
    respostas = [
        "Não entendi o que você perguntou. Tente reformular ou escolha um assunto.",
        "Não entendi o que você quis dizer. Pode tentar explicar de outro jeito?",
        "Hmm, não consegui entender. Quer tentar reformular?",
        "Essa eu não consegui entender. Tenta escrever de um jeito diferente",
        "Fiquei meio perdido aqui, pode reformular a pergunta?",
    ]

    return {
        "text": random.choice(respostas),
        "tag": "default",
        "imagem": None,
        "followup_pergunta": None,
        "followup_data": followup_pendente if followup_pendente else None
    }