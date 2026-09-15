from __future__ import annotations

import re
from pathlib import Path

import frontmatter


def iter_markdown(vault_dir: Path, exclude: set[str] | None = None):
    exclude = exclude or set()
    for path in sorted(vault_dir.rglob("*.md")):
        rel = path.relative_to(vault_dir)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if any(part in exclude for part in rel.parts):
            continue
        yield path


def _split_section(section: str, max_chars: int) -> list[str]:
    if len(section) <= max_chars:
        return [section]
    parts, buf = [], ""
    for paragraph in re.split(r"\n\s*\n", section):
        if len(buf) + len(paragraph) > max_chars and buf:
            parts.append(buf.strip())
            buf = paragraph
        else:
            buf = (buf + "\n\n" + paragraph).strip()
    if buf:
        parts.append(buf)
    return parts


def chunk_file(
    path: Path,
    vault_dir: Path,
    max_chars: int,
    metadata_fields: list[str],
) -> list[dict]:
    post = frontmatter.load(path)
    meta = post.metadata
    rel = path.relative_to(vault_dir).as_posix()

    chunks: list[dict] = []
    for section in re.split(r"(?m)^(?=## )", post.content):
        section = section.strip()
        if not section:
            continue
        for piece in _split_section(section, max_chars):
            heading = (
                piece.splitlines()[0].lstrip("#").strip()
                if piece.startswith("#")
                else ""
            )
            breadcrumb = f"[{meta.get('categoria', '')} > {meta.get('titulo', '')} > {heading}]"

            chunk_meta: dict[str, str] = {"arquivo": rel}
            for field in metadata_fields:
                value = meta.get(field, "")
                if isinstance(value, (list, tuple)):
                    value = ",".join(str(v) for v in value)
                chunk_meta[field] = str(value)

            chunks.append({"texto": f"{breadcrumb}\n{piece}", "meta": chunk_meta})
    return chunks
