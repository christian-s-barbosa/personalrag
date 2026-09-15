from __future__ import annotations

from .config import Settings
from .rag import VaultRag


def run_mcp(settings: Settings, name: str | None = None) -> None:
    from mcp.server.mcpserver import MCPServer

    rag = VaultRag(settings)
    server = MCPServer(name or f"rag-{settings.collection}")
    suffix = settings.collection

    @server.tool(name=f"buscar_{suffix}")
    def buscar(query: str, nivel: str = "", categoria: str = "") -> str:
        """Busca trechos relevantes na base de conhecimento.

        Args:
            query: a busca em linguagem natural.
            nivel: filtra por nível (basico, intermediario, avancado) - opcional.
            categoria: filtra por categoria - opcional.
        """
        filtros = {k: v for k, v in {"nivel": nivel, "categoria": categoria}.items() if v}
        trechos = rag.buscar(query, filters=filtros or None)
        if not trechos:
            return "Nenhum trecho encontrado."
        return "\n\n".join(f"### {t['meta']['arquivo']}\n{t['texto']}" for t in trechos)

    @server.tool(name=f"responder_{suffix}")
    def responder(query: str, nivel: str = "", categoria: str = "") -> str:
        """Responde uma pergunta usando a base (RAG) e o LLM.

        Args:
            query: a pergunta.
            nivel: filtra por nível (basico, intermediario, avancado) - opcional.
            categoria: filtra por categoria - opcional.
        """
        filtros = {k: v for k, v in {"nivel": nivel, "categoria": categoria}.items() if v}
        resposta, fontes = rag.responder(query, filters=filtros or None)
        return f"{resposta}\n\nFontes:\n" + "\n".join(f"- {f}" for f in fontes)

    server.run()
