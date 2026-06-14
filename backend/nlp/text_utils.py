from __future__ import annotations
import re
import unicodedata
import logging

logger = logging.getLogger(__name__)

# ─── spaCy: modelo treinado ou blank + RSLP ───
_USE_TRAINED_MODEL = False
_nlp = None

try:
    import spacy
    _nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner"])
    _USE_TRAINED_MODEL = True
    logger.info("spaCy: modelo treinado pt_core_news_sm carregado.")
except (OSError, ImportError):
    try:
        import spacy
        _nlp = spacy.blank("pt")
        logger.warning("spaCy: pt_core_news_sm ausente — usando blank + RSLP.")
    except ImportError:
        logger.warning("spaCy não instalado — usando apenas RSLP manual.")

# ---------------------------------------------------------------------------
# Constantes de Linguagem
# ---------------------------------------------------------------------------
_STOPWORDS = {
    "o","a","os","as","um","uma","uns","umas","de","do","da","dos","das",
    "em","no","na","nos","nas","por","para","com","que","e","eu","me","te",
    "meu","minha","voce","se","seu","sua","isso","esse","essa","este","esta",
    "aqui","ali","mais","mas","pra","pro","num","numa","sobre","qual","quais",
    "como","quando","onde","quem","tem","ha","ter","ser","foi","sao","esta",
    "estao","ao","aos","la","lhe","lo","nao","tambem","ja","ate","ai","so",
    "tao","muito","bem","disse","pode","vai","vou","faz","pelo","pela","pelas",
    "pelos","entre","ate","apos","ante","alem","desde","durante","sem","sob",
    "sobre","tras","versus","via","porque","pois","mas","ou","nem","seja",
    "seria","serao","sao","serei","somos","sois","sido","sendo","estar",
    "estou","esta","estamos","estais","estao","estive","esteve","estivemos",
    "estiveram","estivesse","estivessem","estiver","estivermos","estiverem",
    "hei","hao","houve","houvemos","houveram","houvesse","houvessem",
    "houver","houvermos","houverem","haverei","havera","haveremos","haverao",
    "haveria","haveriam","tenho","tem","temos","tendes","tem","tive",
    "teve","tivemos","tiveram","tivesse","tivessem","tiver","tivermos",
    "tiverem","terei","tera","teremos","terao","teria","teriam",
    "e","eh","sou","nao","nao","nada","tudo","algo","alguem","ninguem",
    "cada","todo","toda","todos","todas","outro","outra","outros","outras",
    "mesmo","mesma","mesmos","mesmas","tal","tais","qual","quais","cujo",
    "cuja","cujos","cujas","onde","quando","como","porque","porem","contudo",
    "todavia","entretanto","portanto","logo","assim","tambem","alem",
    "inclusive","exceto","salvo","senao","caso","embora","apesar","ainda",
    "ja","so","apenas","quase","muito","pouco","bastante","mais","menos",
    "bem","mal","melhor","pior","sempre","nunca","jamais","agora","depois",
    "antes","hoje","ontem","amanha","aqui","ali","la","ca","longe","perto",
    "dentro","fora","acima","abaixo","frente","atras","junto","apos",
}

AFIRMATIVAS: set[str] = {
    "sim","s","claro","quero","pode","vai","vamo","bora","conta","me conta",
    "me diz","quero saber","com certeza","obvio","show","legal","top",
    "por favor","bora la","conte","me conte","fale","fala","ouvir","diz",
    "mais","continua","continue","isso","exato","perfeito",
}

NEGATIVAS: set[str] = {
    "nao","n","nope","deixa","agora nao","prefiro nao","outro tema","outra coisa",
}

_GATILHOS_ALEATORIO: set[str] = {
    "aleatorio","aleatoria","surpresa","surpreenda","surpreende","qualquer",
    "escolha","escolhe","tanto faz","qualquer coisa","qualquer tema",
    "me surpreenda","me surpreende","algo aleatorio","tema aleatorio",
    "fala qualquer coisa","fala alguma coisa","me conta algo","me conte algo",
    "o que quiser","livre",
}

# ─── Stemmer RSLP simplificado ───
_RSLP_SUFFIXES = [
    ("amentos",""),("imentos",""),("adores",""),("adoras",""),
    ("amento",""),("imento",""),("adora",""),("ando",""),("endo",""),
    ("indo",""),("coes",""),("cao",""),("mente",""),("dades",""),
    ("dade",""),("ismo",""),("ista",""),("aria",""),("eria",""),
    ("iria",""),("asse",""),("esse",""),("isse",""),("aram",""),
    ("eram",""),("iram",""),("ando",""),("endo",""),("indo",""),
    ("amo",""),("emo",""),("imo",""),("oes",""),("ao",""),
    ("ais",""),("eis",""),("ois",""),("ia",""),("as",""),("os",""),
    ("ou",""),("ar",""),("er",""),("ir",""),("am",""),("s",""),
]

def _stem(word: str) -> str:
    for suf, rep in _RSLP_SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[:len(word)-len(suf)] + rep
    return word

def _normalize(text: str) -> str:
    text = text.lower()
    for a, p in {"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i",
                 "ó":"o","ô":"o","õ":"o","ú":"u","ü":"u","ç":"c"}.items():
        text = text.replace(a, p)
    nfkd = unicodedata.normalize("NFD", text)
    return nfkd.encode("ascii", "ignore").decode("ascii")

def _tokenize(text: str) -> list[str]:
    norm = _normalize(text)
    tokens = re.findall(r"[a-z0-9]+", norm)
    # Aplica stemming em cada token
    return [_stem(t) for t in tokens if len(t) >= 2 and t not in _STOPWORDS]

def _lemmatize(text: str) -> list[str]:
    normalized = _normalize(text.lower())
    tokens = []
    
    if _nlp:
        doc = _nlp(normalized)
        for token in doc:
            if not token.is_alpha or len(token.text) < 2:
                continue
            if token.text in _STOPWORDS:
                continue
            if _USE_TRAINED_MODEL:
                lemma = token.lemma_
                if token.is_stop or lemma in _STOPWORDS:
                    continue
                tokens.append(lemma)
            else:
                stem = _stem(token.text)
                if stem in _STOPWORDS or len(stem) < 2:
                    continue
                tokens.append(stem)
    else:
        # Fallback se spaCy falhar completamente
        raw_tokens = re.findall(r"[a-z0-9]+", normalized)
        for t in raw_tokens:
            if t not in _STOPWORDS and len(t) >= 2:
                tokens.append(_stem(t))
                
    return tokens

# ─── Detecção auxiliar ───

def _is_afirmativa(text):
    return bool(set(re.findall(r"[a-z]+", _normalize(text.lower()))) & AFIRMATIVAS)

def _is_negativa(text):
    return bool(set(re.findall(r"[a-z]+", _normalize(text.lower()))) & NEGATIVAS)

def _is_aleatorio(text):
    return bool(set(re.findall(r"[a-z]+", _normalize(text.lower()))) & _GATILHOS_ALEATORIO)
