from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'; UPLOAD_DIR = DATA_DIR / 'uploads'; REPORT_DIR = BASE_DIR / 'reports'
DB_PATH = Path(os.getenv('DOC_COMPARE_DB', DATA_DIR / 'comparison.sqlite3'))
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '25'))
SEMANTIC_THRESHOLD = float(os.getenv('SEMANTIC_THRESHOLD', '0.72'))
REVIEW_HIGH_THRESHOLD = float(os.getenv('REVIEW_HIGH_THRESHOLD', '0.85'))
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}
for d in (DATA_DIR, UPLOAD_DIR, REPORT_DIR): d.mkdir(parents=True, exist_ok=True)
