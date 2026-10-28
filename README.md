# AI-Powered Document Comparison and Change Tracking

A local Streamlit application for comparing PDF/DOCX versions while preserving source files, page references, exact changes, semantic review suggestions, human decisions, audit events, and CSV/PDF exports.

## Run

```bash
cd document-comparison-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Run tests with `pytest -q`. The application initializes `data/comparison.sqlite3` automatically. Configure limits and thresholds in `.env`; API credentials are optional and are never stored in source code.

## Architecture

Upload files are validated and copied under UUID names. `text_extractor` returns page-linked passages. `text_alignment` and `exact_diff` detect added/removed/modified blocks. `semantic_analysis` uses Sentence Transformers when available in a future adapter path and otherwise uses a transparent lexical similarity fallback. `change_classifier` provides rule-based suggestions. `database` stores versions, comparisons, changes, reviews, and audit events. `report_generator` creates evidence-linked CSV/PDF files. `app.py` provides the Streamlit workflow.

## Responsible-AI limitations

Similarity is not proof of equivalent meaning or factual correctness. The fallback is lexical, not a trained embedding model. The current version flags candidates for review and does not fabricate LLM evidence; a production LLM adapter should be configured only with an approved API and must preserve citations from stored passages. Scanned PDFs produce warnings and require OCR before reliable extraction. Authentication, multi-user authorization, and encrypted at-rest storage are deployment responsibilities.

## Recovery and privacy

Original uploads are copied and never edited. If processing is interrupted, rerun the comparison; completed review decisions already committed to SQLite remain available. Remove `data/uploads` and the SQLite file only when a deliberate cleanup is intended.
