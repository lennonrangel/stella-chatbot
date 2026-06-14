from __future__ import annotations
import re
from backend.bot.bdi_models import (
    Beliefs, Desire, DesireAleatorio, DesireConfirmarFollowup,
    DesireNegar, DesireTema, DesireDesconhecido
)
from backend.nlp.text_utils import (
    _normalize, _lemmatize, _is_afirmativa, _is_negativa, _is_aleatorio
)
from backend.nlp.search_service import INTENTS

# ---------------------------------------------------------------------------
# Regras Heurísticas e Constantes de Classificação
# ---------------------------------------------------------------------------

_TAGS_SORTEAVEIS: list[str] = [i["tag"] for i in INTENTS if i["tag"] not in {"saudacao", "despedida", "default"}]

_POSICAO_PLANETA: dict[str,str] = {
    "primeiro":"mercurio","1":"mercurio","segundo":"venus","2":"venus",
    "terceiro":"terra","3":"terra","quarto":"marte","4":"marte",
    "quinto":"jupiter","5":"jupiter","sexto":"saturno","6":"saturno",
    "setimo":"urano","7":"urano","oitavo":"netuno","8":"netuno",
}

_MAPA_FATOS_DIRETOS = [
    #sistema solar
    ({"o que e o sol","definicao do sol"},"sol","O Sol é uma estrela anã amarela"),
    ({"qual a cor do sol","cor do sol"},"sol","A verdadeira cor do Sol é branco"),
    ({"manchas solares", "mancha solar"},"sol","Manchas solares são regiões mais frias causadas por campos magnéticos intensos"),
    ({"erupcoes solares", "erupcao solar"},"sol","Erupções solares são explosões que acontecem na superfície do Sol"),
    ({"vento solar"},"sol","O vento solar é um fluxo contínuo de partículas carregadas que o Sol emite o tempo todo"),
    ({"tempestade solar"},"sol","Uma tempestade solar ocorre quando o Sol lança uma nuvem de plasma magnetizado para o espaço."),
    ({"proximo do sol","mais proximo do sol","mais perto do sol","perto do sol","planeta proximo ao sol"},"mercurio","mais proximo do sol"),
    ({"menor planeta","menor do sistema","menor de todos"},"mercurio","menor planeta"),
    ({"planeta mais rapido","planeta mais veloz"},"mercurio","mais rapido"),
    ({"mais quente","planeta mais quente"},"venus","mais quente"),
    ({"planeta mais brilhante","planeta mais luminoso"},"venus","planeta mais brilhante"),
    ({"sobre a terra","sobre a nossa planeta"},"terra","A Terra é o terceiro planeta do sistema solar"),
    ({"mais parecido com a terra","planeta parecido com a terra"},"marte","planeta vermelho"),
    ({"maior planeta","maior do sistema","maior de todos","planeta gigante","planeta massivo","rei dos planetas"},"jupiter","maior planeta"),
    ({"segundo maior planeta","segundo maior do sistema"},"saturno","segundo maior planeta"),
    ({"mais luas","planeta com mais luas","qual planeta tem mais luas"},"saturno","Saturno é o planeta com o maior número de luas confirmadas no Sistema Solar"),
    ({"luas de jupiter", "quantas luas tem jupiter", "jupiter tem quantas luas", "luas em jupiter"},"jupiter","Júpiter tem 95 luas confirmadas"),
    ({"mais frio","planeta mais frio","mais gelado"},"urano","mais frio"),
    ({"mais distante","mais distante do sol","mais longe do sol","longe do sol","distante do sol","mais longe","planeta mais longe"},"netuno","mais distante do sol"),
    ({"mais lento","planeta mais lento"},"netuno","mais lento"),    
    ({"lua e um planeta", "lua e planeta"},"lua","A lua é um satélite natural"),
    ({"face da lua","lado da lua", "lado oculto da lua"},"lua","sempre vemos a mesma face dela"),   
    ({"a lua e redonda", "porque a lua e redonda", "lua redonda"}, "lua", "A Lua é redonda"),
    ({"planetas sao redondos", "por que os planetas sao redondos", "planeta redondo"}, "sistema_solar", "Planetas são redondos"),

    # Palavras técnicas
    ({"buraco negro no centro", "o que tem no centro da galaxia"}, "buraco_negro", "O buraco negro no centro da Via Láctea"),
    ({"O que e um buraco de minhoca", "buraco de minhoca"}, "espaco_tempo", "Um buraco de minhoca é uma estrutura teórica que conecta dois pontos distantes do espaço-tempo"),  
    ({"o que e uma contelacao", "o que sao as constelacoes"},"constelacoes","Constelações são grupos de estrelas"),
    ({"o que e uma estrela de neutrons", "definicao de estrela de neutrons"},"estrela_neutrons","Uma estrela de nêutrons é uma estrela extremamente densa, resultado do colapso de uma estrela massiva"),
    ({"o que e uma estrela","o que sao estrelas","definicao de estrela"},"estrelas","Estrelas são esferas de gás"),    
    ({"quantas estrelas existem","numero de estrelas","quantas estrelas tem no universo"},"estrelas","100 bilhões de estrelas só na Via Láctea"),
    ({"quantos planetas","numero de planetas","quais planetas","lista de planetas"},"sistema_solar","8 planetas"),
    ({"o que e uma nebulosa?", "definicao de nebulosa"},"nebulosa","Uma nebulosa é uma grande nuvem de gás e poeira no espaço"),
    ({"O que e uma galaxia", "definicao de galaxia"},"galaxias","Galáxias são enormes sistemas de estrelas, gás e poeira"),
    ({"qual a galaxia mais proxima da via lactea", "galaxia mais proxima da via lactea"},"galaxias","A Galáxia de Andrômeda é a mais próxima da Via Láctea"),
    ({"quantas galaxias existem", "numero de galaxias"},"galaxias","Cerca de 2 trilhões de galáxias no universo observável"),
    ({"o que e energia escura", "definicao de energia escura"},"materia_escura","Energia escura representa cerca de 68% do universo e está acelerando sua expansão."),
    ({"cinturao de asteroides", "o que e o cinturão de asteroides"},"cometas_asteroides","O Cinturão de Asteroides é uma região entre as órbitas de Marte e Júpiter"),
    ({"SpaceX", "o que e a spacex"},"spacex","A SpaceX é uma empresa aeroespacial fundada em 2002 por Elon Musk"),
    ({"foguete falcon 9", "falcon 9"},"spacex","Os foguetes da SpaceX, como o Falcon 9, conseguem voltar e pousar na Terra após o lançamento"),
    ({"starship", "nave starship"},"spacex","AO Starship é o foguete mais ambicioso da SpaceX"),
    ({"Falcon Heavy", "foguete falcon heavy"},"spacex","O Falcon Heavy é um dos foguetes mais poderosos já construídos"),
    ({"primeiro animal", "cachorra no espaco", "cachorro no espaco", "laika", "primeiro ser vivo", "cachorra enviada"}, "laika", "A primeira cachorra enviada ao espaço foi a Laika")
]

# Palavras técnicas de sub-tópico (formas stemizadas).
_SPECIFIC_STEMS: set[str] = {
    "altitude", "atmosfera", "camada", "campo", "carga", "cassini",
    "combustivel", "composi", "compr", "corrente", "crosta", "densi",
    "diametro", "discovery", "distancia", "eletron", "espectro", "foguete",
    "gravi", "horizon", "infravermelho", "ion", "jwst", "magnetico", "manto",
    "massa", "miss", "nucleo", "onda", "orbita", "particula", "peso",
    "pioneer", "press", "profundi", "propuls", "proton", "radia", "radio",
    "rota", "sonda", "superficie", "tamanho", "telescopio", "temperatura",
    "veloci", "volume", "voyager",
}

# Palavras que sugerem continuidade de assunto
_GATILHOS_CONTINUIDADE = {
    "ele", "ela", "dele", "dela", "nesse", "naquele", "neste", "isso", "disso",
    "mancha", "anel", "luas", "tamanho", "distancia", "clima", "temperatura",
    "cor", "brilho", "massa", "gravidade", "missao", "sonda", "telescopio"
}

def _is_continuidade(text: str) -> bool:
    """Detecta se a frase parece ser uma continuação (ex: 'e o tamanho dele?')."""
    tokens = set(re.findall(r"\w+", text.lower()))
    return bool(tokens & _GATILHOS_CONTINUIDADE)

def _build_pattern_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for intent in INTENTS:
        if intent["tag"] == "default":
            continue
        for pattern in intent["patterns"]:
            for lemma in _lemmatize(pattern):
                index.setdefault(lemma, [])
                if intent["tag"] not in index[lemma]:
                    index[lemma].append(intent["tag"])
    return index

_PATTERN_INDEX = _build_pattern_index()

def _score_intents(lemmas: list[str]) -> dict[str, int]:
    scores: dict[str, int] = {}
    for lemma in lemmas:
        for tag in _PATTERN_INDEX.get(lemma, []):
            scores[tag] = scores.get(tag, 0) + 1
    return scores

_GATILHOS_SAUDACAO: set[str] = {
    "oi", "ola", "hey", "hei", "e ai", "eae", "bom dia", "boa tarde", "boa noite", "ola stella", "oi stella", "stella", "hello", "hi"
}

_GATILHOS_DESPEDIDA: set[str] = {
    "tchau", "adeus", "ate logo", "ate mais", "fui", "bye", "tchau stella", "encerrar", "parar", "chega"
}

def _is_saudacao(text: str) -> bool:
    """Detecta se a mensagem é uma saudação simples."""
    normalized = _normalize(text.lower()).strip()
    # Verifica match exato ou se começa com saudação e é curta
    if normalized in _GATILHOS_SAUDACAO:
        return True
    
    palavras = set(re.findall(r"[a-z]+", normalized))
    if palavras & _GATILHOS_SAUDACAO and len(palavras) <= 3:
        return True
    return False

def _is_despedida(text: str) -> bool:
    """Detecta se a mensagem é uma despedida."""
    normalized = _normalize(text.lower()).strip()
    if normalized in _GATILHOS_DESPEDIDA:
        return True
    
    palavras = set(re.findall(r"[a-z]+", normalized))
    if palavras & _GATILHOS_DESPEDIDA and len(palavras) <= 3:
        return True
    return False

def _detect_posicao(text):
    normalized = _normalize(text.lower())
    palavras_planeta = {"planeta","sistema","solar","orbita","sol"}
    if not set(re.findall(r"[a-z]+", normalized)) & palavras_planeta:
        return None
    for palavra, tag in _POSICAO_PLANETA.items():
        if palavra in normalized:
            return tag
    return None

def _detect_fato_direto(text):
    """Detecta se a frase contém algum gatilho de fato direto mapeado."""
    normalized = _normalize(text.lower())
    tokens = set(re.findall(r"\w+", normalized))
    
    for gatilhos, tag, hint in _MAPA_FATOS_DIRETOS:
        for gatilho in gatilhos:
            # 1. Match exato de substring (Prioridade 1)
            norm_gatilho = _normalize(gatilho)
            if norm_gatilho in normalized:
                return tag, hint
            
            # 2. Match de palavras-chave (Prioridade 2)
            # Se todas as palavras do gatilho estiverem na frase (em qualquer ordem)
            gatilho_tokens = set(re.findall(r"\w+", norm_gatilho))
            if gatilho_tokens and gatilho_tokens.issubset(tokens):
                return tag, hint
                
    return None

def _classify(lemmas):
    """
    Classifica a intenção pelo maior score de lemas no índice.
    """
    scores = _score_intents(lemmas)
    if not scores:
        return None

    tag = max(scores, key=lambda t: scores[t])
    score = scores[tag]
    has_specific = any(l in _SPECIFIC_STEMS for l in lemmas)

    if score >= 2:
        matching = [l for l in lemmas if tag in _PATTERN_INDEX.get(l, [])]
        if all(l in _SPECIFIC_STEMS for l in matching):
            return None  # só palavras técnicas bateram → LLM
        return tag

    # score == 1
    if has_specific:
        return None  # pergunta técnica de sub-tópico → LLM
    return tag

def _infer_desire(beliefs: Beliefs) -> Desire:
    text = beliefs.texto_usuario
    text_lower = text.lower().strip()

    # 1. Prioridade Máxima: Saudações e Despedidas
    if _is_saudacao(text):
        return DesireTema(tag="saudacao")
    
    if _is_despedida(text):
        return DesireTema(tag="despedida")

    # 2. Mapeamento de Fatos Diretos
    fato_direto = _detect_fato_direto(text)
    if fato_direto:
        return DesireTema(tag=fato_direto[0], hint=fato_direto[1])

    if _is_aleatorio(text):
        return DesireAleatorio()

    if beliefs.followup_data:
        proxima_tag = beliefs.followup_data.get("proxima_tag")
        if proxima_tag:
            if _is_negativa(text):
                return DesireNegar()
            tag_detectada = _classify(beliefs.lemmas)
            if _is_afirmativa(text) and tag_detectada is None:
                return DesireConfirmarFollowup(
                    proxima_tag=proxima_tag,
                    proximo_hint=beliefs.followup_data.get("proximo_hint"),
                )
            if tag_detectada:
                return DesireTema(tag=tag_detectada, hint=beliefs.texto_norm)
            return DesireDesconhecido(followup_data=beliefs.followup_data)

    tag_posicao = _detect_posicao(text)
    if tag_posicao:
        return DesireTema(tag=tag_posicao, hint=beliefs.texto_norm)

    tag = _classify(beliefs.lemmas)
    if tag:
        return DesireTema(tag=tag, hint=beliefs.texto_norm)

    # 3. Continuidade de Tópico (Memória de Assunto)
    # Se não detectamos um novo tema forte, mas a frase parece uma continuação 
    # e já estávamos falando de algo, mantemos o tema atual.
    if beliefs.ultimo_tema and _is_continuidade(text):
        return DesireTema(tag=beliefs.ultimo_tema, hint=beliefs.texto_norm)

    return DesireDesconhecido()
