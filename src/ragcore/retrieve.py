from __future__ import annotations

from .config import Settings
from .models import get_embedder, get_reranker
from .store import Store


def search(
    settings: Settings,
    store: Store,
    query: str,
    filters: dict | None = None,
    k: int | None = None,
    top: int | None = None,
) -> list[dict]:
    k = k or settings.top_k
    top = top or settings.top_n

    query_embedding = get_embedder(settings.embed_model).encode(
        [query], normalize_embeddings=True
    ).tolist()

    kwargs = {"where": filters} if filters else {}
    result = store.collection().query(
        query_embeddings=query_embedding, n_results=k, **kwargs
    )

    docs = result["documents"][0]
    metas = result["metadatas"][0]

    if settings.use_rerank and len(docs) > 1:
        try:
            scores = get_reranker(settings.rerank_model).predict(
                [(query, doc) for doc in docs]
            )
            order = sorted(range(len(docs)), key=lambda i: -float(scores[i]))
            docs = [docs[i] for i in order]
            metas = [metas[i] for i in order]
        except Exception:
            pass

    return [
        {"texto": doc, "meta": meta}
        for doc, meta in zip(docs[:top], metas[:top])
    ]
