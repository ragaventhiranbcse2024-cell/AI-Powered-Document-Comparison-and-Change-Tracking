from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class Passage:
    id: int; page: int; text: str; kind: str = 'paragraph'

class ExtractionError(Exception): pass

def extract_pages(path: str | Path) -> tuple[list[Passage], list[str]]:
    path=Path(path); ext=path.suffix.lower(); warnings=[]; pages=[]
    try:
        if ext == '.pdf':
            import fitz
            doc=fitz.open(path)
            for n,p in enumerate(doc,1):
                text=p.get_text('text') or ''
                if not text.strip(): warnings.append(f'Page {n} has no extractable text; it may be scanned.')
                for chunk in _paragraphs(text): pages.append(Passage(len(pages)+1,n,chunk))
        elif ext == '.docx':
            from docx import Document
            doc=Document(path)
            for para in doc.paragraphs:
                if para.text.strip(): pages.append(Passage(len(pages)+1,1,para.text.strip()))
            if not pages: warnings.append('DOCX contained no extractable paragraphs.')
        else: raise ExtractionError(f'Unsupported format: {ext}')
    except (ImportError, ModuleNotFoundError) as e: raise ExtractionError(f'Missing dependency for {ext}: {e}')
    except Exception as e:
        if isinstance(e, ExtractionError): raise
        raise ExtractionError(f'Could not extract {path.name}: {e}')
    return pages,warnings

def _paragraphs(text: str):
    return [re.sub(r'\s+',' ',x).strip() for x in re.split(r'\n\s*\n|\n(?=[A-Z0-9])', text) if x.strip()]
