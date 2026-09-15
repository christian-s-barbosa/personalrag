from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    """Configuração de uma base de conhecimento para o RAG."""

    vault_dir: str
    collection: str

    index_dir: str | None = None
    chunk_max_chars: int = 1200
    metadata_fields: list[str] = field(
        default_factory=lambda: ["titulo", "nivel", "categoria", "tipo", "tags"]
    )
    exclude_dirs: list[str] = field(
        default_factory=lambda: ["rag", ".venv", "chroma", "__pycache__"]
    )

    embed_model: str = "BAAI/bge-m3"
    rerank_model: str = "BAAI/bge-reranker-v2-m3"
    use_rerank: bool = False

    llm_model: str = "deepseek-chat"
    llm_base_url: str = "https://api.deepseek.com"
    llm_api_key_env: str = "DEEPSEEK_API_KEY"

    top_k: int = 8
    top_n: int = 4

    @property
    def vault_path(self) -> Path:
        return Path(self.vault_dir).expanduser().resolve()

    @property
    def index_path(self) -> Path:
        base = self.index_dir or str(Path.cwd() / "chroma")
        return Path(base).expanduser().resolve()
