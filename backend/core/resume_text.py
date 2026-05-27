import io
import zipfile
from xml.etree import ElementTree

import pdfplumber
from fastapi import UploadFile

from gateway.errors import (
    corrupt_pdf,
    empty_file,
    file_too_large,
    invalid_docx,
    no_extractable_text,
    unsupported_file_type,
)


def extract_text_from_upload(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    data = file.file.read()
    if not data:
        raise empty_file()
    if len(data) > 5 * 1024 * 1024:
        raise file_too_large()
    if filename.endswith(".pdf"):
        return _extract_pdf(data)
    if filename.endswith(".docx"):
        return _extract_docx(data)
    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="replace")
    raise unsupported_file_type()


def _extract_pdf(data: bytes) -> str:
    parts: list[str] = []
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    parts.append(text)
    except Exception as exc:
        raise corrupt_pdf() from exc
    text = "\n".join(parts).strip()
    if not text:
        raise no_extractable_text("pdf")
    return text


def _extract_docx(data: bytes) -> str:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            xml = zf.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError) as exc:
        raise invalid_docx() from exc
    root = ElementTree.fromstring(xml)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs: list[str] = []
    for para in root.iter(f"{ns}p"):
        parts = [node.text for node in para.iter(f"{ns}t") if node.text]
        if parts:
            paragraphs.append("".join(parts).strip())
    text = "\n".join(paragraphs).strip()
    if not text:
        raise no_extractable_text("docx")
    return text
