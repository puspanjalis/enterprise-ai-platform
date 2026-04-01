from __future__ import annotations

from pathlib import Path
from typing import Iterable



def load_pdf(path: Path) -> Iterable[tuple[str, int]]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            yield text, index


def load_docx(path: Path) -> Iterable[tuple[str, int | None]]:
    from docx import Document as DocxDocument

    doc = DocxDocument(str(path))
    text = "\n".join(par.text for par in doc.paragraphs if par.text.strip())
    if text.strip():
        yield text, None


def load_markdown(path: Path) -> Iterable[tuple[str, int | None]]:
    text = path.read_text(encoding="utf-8")
    if text.strip():
        yield text, None


def load_text(path: Path) -> Iterable[tuple[str, int | None]]:
    text = path.read_text(encoding="utf-8")
    if text.strip():
        yield text, None


def load_document(path: Path) -> Iterable[tuple[str, int | None]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".docx":
        return load_docx(path)
    if suffix in {".md", ".markdown"}:
        return load_markdown(path)
    if suffix in {".txt", ".rst"}:
        return load_text(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")
