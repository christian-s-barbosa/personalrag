# ragcorelib

Núcleo reutilizável de **RAG** (Retrieval-Augmented Generation) sobre bases de conhecimento em **Markdown**.

Separa o **motor** (esta biblioteca) do **conteúdo/config** de cada projeto. Cada base define um `Settings` e usa a API:

```python
from ragcorelib import VaultRag, Settings

settings = Settings(vault_dir="..", collection="git")
rag = VaultRag(settings)

rag.index()
print(rag.buscar("como desfazer o último commit"))
print(rag.responder("como desfazer o último commit"))
```

E o servidor MCP:

```python
from ragcorelib.mcp import run_mcp
from config import settings

run_mcp(settings)
```

## Instalação

```bash
pip install ragcorelib          # núcleo
pip install "ragcorelib[mcp]"   # com o servidor MCP
```

## Módulos

| Módulo | Responsabilidade |
| --- | --- |
| `config.py` | `Settings` (dataclass) |
| `chunking.py` | Dividir markdown por seção + breadcrumb |
| `store.py` | Embeddings + Chroma |
| `retrieve.py` | Busca (+ rerank opcional) |
| `generate.py` | LLM compatível com OpenAI |
| `rag.py` | Classe `VaultRag` |
| `cli.py` | `python -m ragcorelib index/query` |
| `mcp.py` | `run_mcp(settings)` |
