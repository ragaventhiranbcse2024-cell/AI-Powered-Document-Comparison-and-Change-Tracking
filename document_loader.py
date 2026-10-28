from pathlib import Path
from uuid import uuid4
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_DIR

class ValidationError(ValueError): pass

def validate_upload(name: str, data: bytes) -> None:
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS: raise ValidationError(f'Unsupported format: {ext or "no extension"}. Use PDF or DOCX.')
    if not data: raise ValidationError('The uploaded file is empty.')
    if len(data) > MAX_FILE_SIZE_MB * 1024 * 1024: raise ValidationError(f'File exceeds {MAX_FILE_SIZE_MB} MB limit.')

def save_upload(name: str, data: bytes) -> Path:
    validate_upload(name, data)
    target = UPLOAD_DIR / f'{uuid4().hex}_{Path(name).name}'
    target.write_bytes(data); return target
