from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=None)
def get_embedder(model_name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


@lru_cache(maxsize=None)
def get_reranker(model_name: str):
    from sentence_transformers import CrossEncoder

    return CrossEncoder(model_name)
