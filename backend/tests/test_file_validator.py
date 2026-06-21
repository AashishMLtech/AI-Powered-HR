import pytest
from fastapi import UploadFile

from app.utils.file_validator import validate_resume_file


class FakeFile:
    filename = "resume.pdf"

    def __init__(self, content: bytes):
        self.content = content

    async def read(self) -> bytes:
        return self.content

    async def seek(self, position: int) -> None:
        self.position = position


@pytest.mark.asyncio
async def test_accepts_pdf_magic_bytes():
    file = FakeFile(b"%PDF resume text")
    content = await validate_resume_file(file, max_size_mb=1)  # type: ignore[arg-type]
    assert content.startswith(b"%PDF")


@pytest.mark.asyncio
async def test_rejects_invalid_magic_bytes():
    file = FakeFile(b"MZ executable")
    with pytest.raises(Exception):
        await validate_resume_file(file, max_size_mb=1)  # type: ignore[arg-type]
