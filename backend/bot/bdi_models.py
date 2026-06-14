from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from backend.db.models import buscar_ultimo_tema
from backend.nlp.text_utils import _normalize, _lemmatize

@dataclass
class Beliefs:
    sessao_id: str
    ultimo_tema: Optional[str]
    followup_data: Optional[dict]
    texto_usuario: str
    texto_norm: str
    lemmas: list[str] = field(default_factory=list)

    @classmethod
    def from_input(cls, user_input: str, sessao_id: str,
                   followup_pendente: Optional[dict]) -> "Beliefs":
        texto_norm = _normalize(user_input.lower().strip())
        lemmas = _lemmatize(user_input)
        ultimo_tema = buscar_ultimo_tema(sessao_id)
        return cls(sessao_id=sessao_id, ultimo_tema=ultimo_tema,
                   followup_data=followup_pendente, texto_usuario=user_input,
                   texto_norm=texto_norm, lemmas=lemmas)

class Desire: pass

@dataclass
class DesireAleatorio(Desire): pass

@dataclass
class DesireConfirmarFollowup(Desire):
    proxima_tag: str
    proximo_hint: Optional[str]

@dataclass
class DesireNegar(Desire): pass

@dataclass
class DesireTema(Desire):
    tag: str
    hint: Optional[str] = None

@dataclass
class DesireDesconhecido(Desire):
    followup_data: Optional[dict] = None
