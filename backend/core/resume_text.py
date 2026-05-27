import io
import zipfile
from xml.etree import ElementTree

import pdfplumber
from fastapi import HTTPException, UploadFile


def extract_text_from_upload(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    data = file.file.read()
    if not data:
        raise HTTPException(
            status_code=400,
            detail={"error": "Empty file", "code": "EMPTY_FILE"},
        )
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail={"error": "File too large (max 5MB)", "code": "FILE_TOO_LARGE"},
        )
    if filename.endswith(".pdf"):
        return _extract_pdf(data)
    if filename.endswith(".docx"):
        return _extract_docx(data)
    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="replace")
    raise HTTPException(
        status_code=400,
        detail={"error": "Unsupported file type. Use PDF, DOCX, or TXT.", "code": "UNSUPPORTED_TYPE"},
    )


def _extract_pdf(data: bytes) -> str:
    parts: list[str] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
    text = "\n".join(parts).strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Could not extract text from PDF. Use a text-based PDF or enter details manually.",
                "code": "NO_TEXT",
            },
        )
    return text


def _extract_docx(data: bytes) -> str:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            xml = zf.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError) as exc:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid DOCX file", "code": "INVALID_DOCX"},
        ) from exc
    root = ElementTree.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    texts = [node.text for node in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
    text = " ".join(texts).strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail={"error": "Could not extract text from DOCX", "code": "NO_TEXT"},
        )
    return text
