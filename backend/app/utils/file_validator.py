from fastapi import HTTPException, UploadFile


PDF_BYTES = b"%PDF"
DOCX_BYTES = b"PK\x03\x04"


async def validate_resume_file(file: UploadFile, max_size_mb: int) -> bytes:
    content = await file.read()
    max_bytes = max_size_mb * 1024 * 1024

    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail="FILE_TOO_LARGE")

    if not (content.startswith(PDF_BYTES) or content.startswith(DOCX_BYTES)):
        raise HTTPException(status_code=400, detail="INVALID_FILE_TYPE")

    await file.seek(0)
    return content
