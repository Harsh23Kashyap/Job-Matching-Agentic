import io

import pytest
from fastapi import HTTPException

from core.resume_text import extract_text_from_upload


class FakeUpload:
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self.file = io.BytesIO(data)


def test_extract_txt():
    text = extract_text_from_upload(FakeUpload("resume.txt", b"Hello resume"))
    assert text == "Hello resume"


def test_extract_unsupported_type():
    with pytest.raises(HTTPException) as exc:
        extract_text_from_upload(FakeUpload("resume.exe", b"data"))
    assert exc.value.status_code == 400


def test_extract_empty_file():
    with pytest.raises(HTTPException) as exc:
        extract_text_from_upload(FakeUpload("resume.txt", b""))
    assert exc.value.status_code == 400
