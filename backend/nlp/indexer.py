from __future__ import annotations
import json
import math
import os
from typing import Optional
from backend.nlp.text_utils import _tokenize

_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "intents.json")

with open(_JSON_PATH, encoding="utf-8") as f:
    _INTENTS: list[dict] = json.load(f)

# Tags que não participam da busca por conteúdo
_SKIP_TAGS = {"saudacao", "despedida", "default"}

# Aliases de entidades (Modelo Híbrido) - Centralizado aqui
_TAG_ALIASES: dict[str, list[str]] = {
    "mercurio":           ["primeiro planeta", "menor planeta", "mais rapido", "perto do sol", "proximo ao sol", "messenger"],
    "venus":              ["segundo planeta", "mais quente", "planeta quente", "mais brilhante", "venera 13"],
    "terra":              ["terceiro planeta", "planeta azul", "nosso planeta", "escudo magnetico"],
    "lua":                ["satelite natural", "satelite da terra", "formacao da lua", "grande impacto", "apollo", "artemis", "fases da lua", "crateras"],
    "marte":              ["quarto planeta", "planeta vermelho", "planeta marciano", "olympus mons", "valles marineris", "perseverance", "curiosity"],
    "jupiter":            ["quinto planeta", "maior planeta do sistema solar", "gigante gasoso", "grande mancha vermelha", "juno", "io", "europa", "ganimedes", "calisto"],
    "saturno":            ["sexto planeta", "aneis", "planeta dos aneis", "cassini", "titan"],
    "urano":              ["setimo planeta", "gigante de gelo", "mais frio","eixo inclinado", "titania", "oberon", "miranda"],
    "netuno":             ["oitavo planeta", "mais distante", "mais lento", "voyager 2", "tritao"],
    "plutao":             ["planeta anao", "cinturao de kuiper", "new horizons", "nuvem de oort", "eris"],
    "sistema_solar":      ["sistema solar", "nossa vizinhanca", "planetas", "orbita do sol", "quantos planetas"],
    "buraco_negro":       ["horizonte de eventos", "singularidade", "espaguetificacao", "sagitario a", "evento horizon telescope"],
    "constelacoes":       ["constelacao", "cruzeiro do sul", "cinturao de orion", "tres marias", "betelgeuse", "rigel"],
    "signos":             ["signo", "zodiaco", "astrologia", "precessao", "ofiuco"],
    "estrelas":           ["estrela", "sol", "fusao nuclear", "proxima centauri", "stephenson 2-18", "ciclo de vida", "poeira de estrelas"],
    "supernova":          ["supernova", "explosao estelar", "morte de estrela", "nebulosa do caranguejo"],
    "estrela_neutrons":   ["pulsar", "magnetar", "estrela compacta", "kilonova"],
    "nebulosa":           ["nebulosa", "nuvem de gas", "bercario estelar", "nebulosa de orion", "helix", "olho de deus"],
    "galaxias":           ["galaxia", "via lactea", "andromeda", "hubble", "james webb"],
    "big_bang":           ["origem do universo", "inicio do universo", "criacao do universo", "radiacao cosmica de fundo"],
    "destino_universo":   ["fim do universo", "destino do universo", "big freeze", "big rip", "big crunch", "energia escura"],
    "materia_escura":     ["dark matter", "massa invisivel", "lente gravitacional", "energia escura"],
    "espaco_tempo":       ["relatividade", "einstein", "curvatura", "dilatacao temporal", "buraco de minhoca"],
    "vida_extraterrestre":["alien", "extraterrestre", "fermi", "drake", "seti", "trappist"],
    "cometas_asteroides": ["cometa", "asteroide", "meteorito", "chicxulub", "dart"],
    "ano_luz":            ["distancia espacial", "parsec", "distancia no espaco", "velocidade da luz"],
    "spacex":             ["spacex", "elon musk", "falcon 9", "starship", "falcon heavy"],
    "laika":              ["cachorra no espaco", "cachorro no espaco", "primeiro animal no espaco", "primeiro ser vivo no espaco", "laika"],
}

def load_processed_intents():
    processed = []
    for item in _INTENTS:
        tag = item["tag"]
        patterns = _TAG_ALIASES.get(tag, [tag.replace("_", " ")])
        if tag.replace("_", " ") not in patterns:
            patterns.append(tag.replace("_", " "))
        processed.append({
            "tag": tag,
            "patterns": patterns,
            "responses": item["conteudo"]
        })
    return processed

INTENTS = load_processed_intents()

# ---------------------------------------------------------------------------
# Construção do corpus TF-IDF
# ---------------------------------------------------------------------------

def _compute_tf(tokens: list[str]) -> dict[str, float]:
    if not tokens:
        return {}
    freq: dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    n = len(tokens)
    return {t: c / n for t, c in freq.items()}

class _Document:
    __slots__ = ("tag", "idx", "texto", "imagem", "followup", "tokens", "tf")

    def __init__(self, tag: str, idx: int, texto: str, imagem: list, followup: Optional[dict], searchable_text: str = None):
        self.tag = tag
        self.idx = idx
        self.texto = texto
        self.imagem = imagem
        self.followup = followup
        
        # Usa searchable_text se fornecido (herança de hints), senão usa o texto original
        final_text = searchable_text if searchable_text else texto
        self.tokens = _tokenize(final_text)
        self.tf: dict[str, float] = _compute_tf(self.tokens)

# Monta corpus
_CORPUS: list[_Document] = []

for intent in _INTENTS:
    tag = intent["tag"]
    if tag in _SKIP_TAGS:
        continue
    
    blocos = intent.get("conteudo", [])
    for idx, bloco in enumerate(blocos):
        # Texto base para busca
        searchable_text = bloco.get("texto", "")

        # Tenta encontrar quem aponta para este bloco para herdar as palavras-chave
        if idx > 0:
            prev_bloco = blocos[idx-1]
            prev_followup = prev_bloco.get("followup")
            if prev_followup and prev_followup.get("proxima_tag") == tag:
                # Adiciona a pergunta e o hint do bloco anterior ao índice deste bloco
                if prev_followup.get("pergunta"):
                    searchable_text += " " + prev_followup["pergunta"]
                if prev_followup.get("proximo_hint"):
                    searchable_text += " " + prev_followup["proximo_hint"]
        
        doc = _Document(
            tag=tag,
            idx=idx,
            texto=bloco.get("texto", ""),
            imagem=bloco.get("imagem", []),
            followup=bloco.get("followup"),
            searchable_text=searchable_text
        )
        
        if doc.tokens:
            _CORPUS.append(doc)

# IDF sobre o corpus
_N = len(_CORPUS)

def _compute_idf() -> dict[str, float]:
    df: dict[str, int] = {}
    for doc in _CORPUS:
        for t in set(doc.tokens):
            df[t] = df.get(t, 0) + 1
    if _N == 0:
        return {}
    return {t: math.log((_N + 1) / (n + 1)) + 1 for t, n in df.items()}

_IDF: dict[str, float] = _compute_idf()

def _tfidf_vector(tf: dict[str, float]) -> dict[str, float]:
    return {t: w * _IDF.get(t, 1.0) for t, w in tf.items()}

# Pré-computa vetores TF-IDF de todos os documentos
_DOC_VECTORS: list[dict[str, float]] = [_tfidf_vector(doc.tf) for doc in _CORPUS]
