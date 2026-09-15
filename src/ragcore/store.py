from __future__ import annotations

import chromadb

from .chunking import chunk_file, iter_markdown
from .config import Settings
from .models import get_embedder


class Store:
    """Gerencia o índice vetorial (Chroma) de uma base."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = chromadb.PersistentClient(path=str(settings.index_path))

    def build(self) -> int:
        try:
            self.client.delete_collection(self.settings.collection)
        except Exception:
            pass

        collection = self.client.create_collection(
            self.settings.collection, metadata={"hnsw:space": "cosine"}
        )

        docs: list[str] = []
        metas: list[dict] = []
        ids: list[str] = []

        for path in iter_markdown(
            self.settings.vault_path, exclude=set(self.settings.exclude_dirs)
        ):
            chunks = chunk_file(
                path,
                self.settings.vault_path,
                self.settings.chunk_max_chars,
                self.settings.metadata_fields,
            )
            for i, chunk in enumerate(chunks):
                docs.append(chunk["texto"])
                metas.append(chunk["meta"])
                ids.append(f"{chunk['meta']['arquivo']}::{i}")

        if not docs:
            return 0

        embeddings = get_embedder(self.settings.embed_model).encode(
            docs, normalize_embeddings=True, batch_size=32, show_progress_bar=True
        )

        for start in range(0, len(docs), 500):
            end = start + 500
            collection.add(
                ids=ids[start:end],
                documents=docs[start:end],
                metadatas=metas[start:end],
                embeddings=embeddings[start:end].tolist(),
            )

        return len(docs)

    def collection(self):
        return self.client.get_collection(self.settings.collection)
