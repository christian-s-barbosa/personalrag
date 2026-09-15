from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .config import Settings
from .rag import VaultRag


def load_settings(path: str) -> Settings:
    config_path = Path(path).expanduser().resolve()
    spec = importlib.util.spec_from_file_location("ragcore_project_config", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "settings"):
        raise SystemExit(f"O arquivo {config_path} não define 'settings'.")
    return module.settings


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="ragcore", description="RAG sobre uma base Markdown")
    parser.add_argument("--config", required=True, help="Caminho para o config.py do projeto")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("index", help="Constrói o índice vetorial")

    query = sub.add_parser("query", help="Faz uma pergunta")
    query.add_argument("question", nargs="+")

    args = parser.parse_args(argv)
    settings = load_settings(args.config)
    rag = VaultRag(settings)

    if args.cmd == "index":
        total = rag.index()
        print(f"OK: {total} chunks na coleção '{settings.collection}'.")
    elif args.cmd == "query":
        pergunta = " ".join(args.question)
        resposta, fontes = rag.responder(pergunta)
        print(resposta)
        print("\nFontes:")
        for fonte in fontes:
            print(f"- {fonte}")


if __name__ == "__main__":
    main()
