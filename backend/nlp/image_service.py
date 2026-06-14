from __future__ import annotations

import logging
import requests

logger = logging.getLogger(__name__)

# ─── Mapeamento tag interna → artigo Wikipedia ───
_TAG_PARA_BUSCA: dict[str, str] = {
    "mercurio":          "Mercury (planet)",
    "venus":             "Venus",
    "terra":             "Earth",
    "marte":             "Mars",
    "jupiter":           "Jupiter",
    "saturno":           "Saturn",
    "urano":             "Uranus",
    "netuno":            "Neptune",
    "plutao":            "Pluto",
    "sol":               "Sun",
    "lua":               "Moon",
    "buraco_negro":      "Black hole",
    "galaxia":           "Galaxy",
    "via_lactea":        "Milky Way",
    "andromeda":         "Andromeda Galaxy",
    "nebulosa":          "Nebula",
    "supernova":         "Supernova",
    "estrela":           "Star",
    "sistema_solar":     "Solar System",
    "big_bang":          "Big Bang",
    "cometa":            "Comet",
    "asteroide":         "Asteroid",
    "meteoro":           "Meteoroid",
    "exoplaneta":        "Exoplanet",
    "universo":          "Universe",
    "telescopio":        "Hubble Space Telescope",
    "estacao_espacial":  "International Space Station",
    "apollo":            "Apollo program",
    "nasa":              "NASA",
    "james_webb":        "James Webb Space Telescope",
}

# ─── Extração de tema a partir de texto livre (respostas do LLM) ───

# Ordem importa: termos mais específicos primeiro para evitar falsos positivos.
# Cada entrada: (keyword_em_português, artigo_Wikipedia_em_inglês)
_TERMOS: list[tuple[str, str]] = [

    # Pessoas - astronautas e cosmonautas
    ("yuri gagarin",        "Yuri Gagarin"),
    ("gagarin",             "Yuri Gagarin"),
    ("neil armstrong",      "Neil Armstrong"),
    ("armstrong",           "Neil Armstrong"),
    ("buzz aldrin",         "Buzz Aldrin"),
    ("aldrin",              "Buzz Aldrin"),
    ("valentina tereshkova","Valentina Tereshkova"),
    ("tereshkova",          "Valentina Tereshkova"),
    ("alan shepard",        "Alan Shepard"),
    ("shepard",             "Alan Shepard"),
    ("chris hadfield",      "Chris Hadfield"),
    ("hadfield",            "Chris Hadfield"),
    ("mae jemison",         "Mae Jemison"),
    ("jemison",             "Mae Jemison"),
    ("laika",               "Laika"),
    ("marcos pontes",       "Marcos Pontes"),

    # Pessoas - cientistas e visionários
    ("stephen hawking",     "Stephen Hawking"),
    ("hawking",             "Stephen Hawking"),
    ("carl sagan",          "Carl Sagan"),
    ("sagan",               "Carl Sagan"),
    ("albert einstein",     "Albert Einstein"),
    ("einstein",            "Albert Einstein"),
    ("isaac newton",        "Isaac Newton"),
    ("newton",              "Isaac Newton"),
    ("galileu galilei",     "Galileo Galilei"),
    ("galileu",             "Galileo Galilei"),
    ("galileo",             "Galileo Galilei"),
    ("nicolau copérnico",   "Nicolaus Copernicus"),
    ("copérnico",           "Nicolaus Copernicus"),
    ("copernico",           "Nicolaus Copernicus"),
    ("johannes kepler",     "Johannes Kepler"),
    ("kepler",              "Johannes Kepler"),
    ("tycho brahe",         "Tycho Brahe"),
    ("edwin hubble",        "Edwin Hubble"),
    ("elon musk",           "Elon Musk"),
    ("wernher von braun",   "Wernher von Braun"),
    ("von braun",           "Wernher von Braun"),

    # Missões e programas espaciais
    ("apollo 11",           "Apollo 11"),
    ("apollo 13",           "Apollo 13"),
    ("missão apollo",       "Apollo program"),
    ("programa apollo",     "Apollo program"),
    ("vostok",              "Vostok 1"),
    ("mir",                 "Mir"),
    ("voyager",             "Voyager program"),
    ("voyager 1",           "Voyager 1"),
    ("voyager 2",           "Voyager 2"),
    ("new horizons",        "New Horizons"),
    ("cassini",             "Cassini–Huygens"),
    ("curiosity",           "Curiosity (rover)"),
    ("perseverance",        "Perseverance (rover)"),
    ("artemis",             "Artemis program"),
    ("spacex",              "SpaceX"),
    ("starship",            "SpaceX Starship"),
    ("falcon 9",            "Falcon 9"),
    ("dragon",              "SpaceX Dragon"),
    ("space shuttle",       "Space Shuttle"),
    ("ônibus espacial",     "Space Shuttle"),
    ("onibus espacial",     "Space Shuttle"),
    ("sputnik",             "Sputnik 1"),
    ("challenger",          "Space Shuttle Challenger disaster"),
    ("columbia",            "Space Shuttle Columbia disaster"),

    # Objetos e fenômenos - termos compostos primeiro
    ("james webb",          "James Webb Space Telescope"),
    ("telescópio hubble",   "Hubble Space Telescope"),
    ("hubble",              "Hubble Space Telescope"),
    ("via láctea",          "Milky Way"),
    ("via lactea",          "Milky Way"),
    ("buraco negro",        "Black hole"),
    ("buraco de minhoca",   "Wormhole"),
    ("big bang",            "Big Bang"),
    ("matéria escura",      "Dark matter"),
    ("materia escura",      "Dark matter"),
    ("energia escura",      "Dark energy"),
    ("sistema solar",       "Solar System"),
    ("estação espacial",    "International Space Station"),
    ("iss",                 "International Space Station"),
    ("estrela de nêutrons", "Neutron star"),
    ("estrela de neutrons", "Neutron star"),
    ("anã branca",          "White dwarf"),
    ("ana branca",          "White dwarf"),
    ("anã vermelha",        "Red dwarf"),
    ("ana vermelha",        "Red dwarf"),
    ("gigante vermelha",    "Red giant"),
    ("buraco negro supermassivo", "Supermassive black hole"),
    ("cinto de asteroides", "Asteroid belt"),
    ("nuvem de oort",       "Oort cloud"),
    ("cinturão de kuiper",  "Kuiper belt"),
    ("chuva de meteoros",   "Meteor shower"),

    # Objetos individuais - termos simples por último
    ("mercúrio",            "Mercury (planet)"),
    ("mercurio",            "Mercury (planet)"),
    ("vênus",               "Venus"),
    ("venus",               "Venus"),
    ("marte",               "Mars"),
    ("júpiter",             "Jupiter"),
    ("jupiter",             "Jupiter"),
    ("saturno",             "Saturn"),
    ("urano",               "Uranus"),
    ("netuno",              "Neptune"),
    ("plutão",              "Pluto"),
    ("plutao",              "Pluto"),
    ("andrômeda",           "Andromeda Galaxy"),
    ("andromeda",           "Andromeda Galaxy"),
    ("supernova",           "Supernova"),
    ("nebulosa",            "Nebula"),
    ("exoplaneta",          "Exoplanet"),
    ("cometa",              "Comet"),
    ("asteroide",           "Asteroid"),
    ("lua",                 "Moon"),
    ("sol",                 "Sun"),
    ("estrela",             "Star"),
    ("galáxia",             "Galaxy"),
    ("galaxia",             "Galaxy"),
    ("nasa",                "NASA"),
    ("apollo",              "Apollo program"),
]

_CACHE: dict[str, str | None] = {}


def _buscar_wikipedia(termo: str) -> str | None:
    """
    Busca a imagem principal de um artigo via API REST da Wikipedia.
    Tenta inglês primeiro (mais completo), depois português.
    Gratuito, sem chave de API.
    """
    for lang in ("en", "pt"):
        url = (f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/"
               f"{termo.replace(' ', '_')}")
        try:
            r = requests.get(url, timeout=6,
                             headers={"User-Agent": "StellaBot/1.0"})
            if r.status_code == 200:
                data = r.json()
                img = (data.get("thumbnail") or
                       data.get("originalimage") or {}).get("source")
                if img:
                    logger.info(f"[ImageService] {termo} → {img[:60]}...")
                    return img
        except Exception as e:
            logger.debug(f"[ImageService] {lang}.wikipedia '{termo}': {e}")

    logger.debug(f"[ImageService] Sem imagem para '{termo}'.")
    return None


def buscar_imagem_para_tag(tag: str) -> str | None:
    """Retorna imagem Wikipedia para uma tag interna da Stella."""
    if tag in _CACHE:
        return _CACHE[tag]
    termo = _TAG_PARA_BUSCA.get(tag, tag.replace("_", " "))
    url = _buscar_wikipedia(termo)
    _CACHE[tag] = url
    return url


def buscar_imagem_para_texto(texto: str) -> str | None:
    """
    Extrai o tema mais relevante de um texto livre (resposta do LLM ou
    pergunta do usuário) e retorna a imagem Wikipedia correspondente.
    """
    texto_lower = texto.lower()

    for keyword, termo_wiki in _TERMOS:
        if keyword in texto_lower:
            cache_key = f"_txt_{termo_wiki}"
            if cache_key in _CACHE:
                return _CACHE[cache_key]
            url = _buscar_wikipedia(termo_wiki)
            _CACHE[cache_key] = url
            return url

    return None
