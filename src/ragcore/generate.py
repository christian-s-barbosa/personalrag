from __future__ import annotations

import os
from functools import lru_cache

from .config import Settings

SYSTEM_PROMPT = (
    "Você é um assistente especialista. Responda à pergunta usando SOMENTE o "
    "contexto fornecido. Se a resposta não estiver no contexto, diga que não "
    "encontrou na base. Ao final, cite os arquivos usados."
)


@lru_cache(maxsize=None)
def _client(base_url: str, api_key: str):
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url=base_url)


def generate(settings: Settings, question: str, context: str) -> str:
    api_key = os.getenv(settings.llm_api_key_env)
    if not api_key:
        raise RuntimeError(f"Defina a variável de ambiente {settings.llm_api_key_env}")

    client = _client(settings.llm_base_url, api_key)
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPergunta: {question}"},
        ],
    )
    return response.choices[0].message.content
