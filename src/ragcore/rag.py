from __future__ import annotations

from .config import Settings
from .generate import generate
from .retrieve import search
from .store import Store


class VaultRag:
    """Fachada que orquestra indexação, busca e geração."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.store = Store(settings)

    def index(self) -> int:
        return self.store.build()

    def buscar(
        self,
        query: str,
        filters: dict | None = None,
        k: int | None = None,
        top: int | None = None,
    ) -> list[dict]:
        return search(self.settings, self.store, query, filters=filters, k=k, top=top)

    def responder(self, query: str, filters: dict | None = None) -> tuple[str, list[str]]:
        trechos = self.buscar(query, filters=filters)
        contexto = "\n\n---\n\n".join(t["texto"] for t in trechos)
        resposta = generate(self.settings, query, contexto)
        fontes = sorted({t["meta"]["arquivo"] for t in trechos})
        return resposta, fontes
