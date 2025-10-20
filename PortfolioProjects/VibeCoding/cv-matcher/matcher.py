import re
import io
from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# lazy import heavy libs

MODEL = None

STOPWORDS = set("""
A ABOUT ABOVE AFTER AGAIN AGAINST ALL AM AMONG AN AND ANY ARE AS AT BE BECAUSE BEEN BEFORE
BEHIND BELOW BESIDE BETWEEN BOTH BUT BY CAN CANNOT COULD DID DO DOES DONE DURING
EACH FEW FOR FROM FURTHER HAD HAS HAVE HAVING HE HER HERE HERS HIM HIS HOW I IF IN
INTO IS IT ITS JUST MORE MOST MY NO NOR NOT OF OFF ON ONCE ONLY OR OTHER OUR OUT
OVER OWN SAME SHE SHOULD SO SOME SUCH THAN THAT THE THEIR THEM THEN THERE THESE THEY
THIS THOSE THROUGH TO TOO UNDER UNTIL UP VERY WAS WE WERE WHAT WHEN WHERE WHICH WHILE
WHO WHOM WHY WILL WITH YOU YOUR
""".split())

def _load_model():
    global MODEL
    if MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError("sentence-transformers is required. Install it first.") from e
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return MODEL


def normalize_text(text: str) -> str:
    text = text or ""
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r"[^\w\s]", ' ', text)
    text = re.sub(r"\s+", ' ', text)
    return text.strip().lower()


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    name = (filename or '').lower()
    if name.endswith('.pdf'):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            pages = [p.extract_text() or '' for p in reader.pages]
            return '\n'.join(pages)
        except Exception:
            return ''
    if name.endswith('.docx'):
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs]
            return '\n'.join(paragraphs)
        except Exception:
            return ''
    # fallback: assume text or utf-8
    try:
        return file_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return ''


def _extract_keywords(text: str, top_k: int = 10) -> list:
    text = normalize_text(text)
    tokens = [t for t in text.split() if t and t not in STOPWORDS and not t.isdigit()]
    counts = Counter(tokens)
    most = [w for w, c in counts.most_common(top_k)]
    return most


def _embedding_similarity(a: str, b: str) -> float:
    model = _load_model()
    emb = model.encode([a, b], convert_to_numpy=True)
    sim = cosine_similarity(emb[0].reshape(1, -1), emb[1].reshape(1, -1))[0][0]
    # clip and normalize to 0..1
    if np.isnan(sim):
        return 0.0
    return float(max(0.0, min(1.0, sim)))


def score_cv(cv_text: str, job_text: str, weights=(0.7, 0.3)) -> dict:
    """
    Return a dict with embedding_score (0..1), keyword_overlap (0..1) and combined_percent (0..100)
    weights: (embedding_weight, keyword_weight)
    """
    if not job_text:
        return {'embedding_score': 0.0, 'keyword_overlap': 0.0, 'combined_percent': 0.0}
    cv_n = normalize_text(cv_text)
    job_n = normalize_text(job_text)

    embedding_score = _embedding_similarity(cv_n, job_n)

    keywords = _extract_keywords(job_text, top_k=12)
    if keywords:
        cv_tokens = set(cv_n.split())
        matched = sum(1 for k in keywords if k in cv_tokens)
        keyword_overlap = matched / len(keywords)
    else:
        keyword_overlap = 0.0

    emb_w, kw_w = weights
    combined = embedding_score * emb_w + keyword_overlap * kw_w
    return {
        'embedding_score': embedding_score,
        'keyword_overlap': keyword_overlap,
        'combined_percent': round(float(combined) * 100, 2)
    }


def batch_score(job_text: str, cvs: list, weights=(0.7, 0.3)) -> list:
    """
    cvs: list of tuples (name, text)
    returns list of dicts with name, embedding_score, keyword_overlap, combined_percent
    """
    results = []
    for name, text in cvs:
        sc = score_cv(text, job_text, weights=weights)
        results.append({
            'name': name,
            'embedding_score': round(sc['embedding_score'] * 100, 2),
            'keyword_overlap': round(sc['keyword_overlap'] * 100, 2),
            'combined_percent': sc['combined_percent']
        })
    results.sort(key=lambda r: r['combined_percent'], reverse=True)
    return results
