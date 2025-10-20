CV Matcher

This is a small Streamlit app that compares multiple CVs against a job description and returns a percentage "match" score using embeddings (sentence-transformers) and keyword overlap.

Quick start (Windows PowerShell):

```powershell
cd "c:\Users\tdi-f\Documents\C#\Projecten\Vibe Coding\Games\cv-matcher"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

How it works
- Embedding similarity (sentence-transformers "all-MiniLM-L6-v2") between the job description and CV text.
- Keyword overlap: top job keywords are extracted and overlap with CV text is computed.
- Final score is a weighted combination (70% embedding similarity, 30% keyword overlap).

Files
- `app.py`: Streamlit UI
- `matcher.py`: Core matching logic and text extraction
- `samples/`: small sample job and CVs
- `tests/`: pytest tests

HTML frontend
- `webapp.py`: A small Flask app that serves a plain HTML form and displays matching results at http://127.0.0.1:5000
- `templates/index.html` and `static/style.css`: simple HTML/CSS for the frontend

Notes
- The app accepts .txt, .pdf, and .docx CVs (basic extraction). PDF/DOCX extraction may occasionally miss formatting or multi-column text.
- Installing the sentence-transformers model requires internet the first time it runs.

Run the Flask HTML frontend (simple HTML interface):

```powershell
cd "c:\Users\tdi-f\Documents\C#\Projecten\Vibe Coding\Games\cv-matcher"
.\.venv\Scripts\Activate.ps1
python webapp.py
# then open http://127.0.0.1:5000 in your browser
```
