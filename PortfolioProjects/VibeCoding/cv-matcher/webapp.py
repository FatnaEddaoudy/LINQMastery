# ...existing code...
from pathlib import Path
import logging
import traceback
import io
import csv

from flask import Flask, request, render_template, Response, send_file

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(DEBUG=True, PROPAGATE_EXCEPTIONS=True, TRAP_HTTP_EXCEPTIONS=True)

# logging
LOG_PATH = Path(__file__).resolve().parent / "logs"
LOG_PATH.mkdir(exist_ok=True)
logfile = LOG_PATH / "webapp_error.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(logfile, encoding="utf-8"), logging.StreamHandler()],
)


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


def _decode_file_storage(f):
    raw = f.read()
    try:
        text = raw.decode("utf-8", errors="ignore")
    except Exception:
        text = str(raw)
    try:
        f.close()
    except Exception:
        pass
    return text


def _simple_score(job, cv_text, emb_w, kw_w):
    import re

    job_tokens = set(re.findall(r"\w+", (job or "").lower()))
    cv_tokens = set(re.findall(r"\w+", (cv_text or "").lower()))
    if not job_tokens:
        return {"embedding_score": 0.0, "keyword_overlap": 0.0, "combined_percent": 0.0}
    overlap = len(job_tokens & cv_tokens) / max(1, len(job_tokens))
    emb_score = overlap
    kw_score = overlap
    combined = float(emb_w) * emb_score + float(kw_w) * kw_score
    return {
        "embedding_score": round(emb_score * 100, 2),
        "keyword_overlap": round(kw_score * 100, 2),
        "combined_percent": round(combined * 100, 2),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # read job text
            job_text = (request.form.get("job_text") or "").strip()
            if not job_text and "job_file" in request.files:
                job_file = request.files.get("job_file")
                job_text = _decode_file_storage(job_file)

            # gather CVs
            uploaded = request.files.getlist("cvs") if request.files else []
            if not uploaded:
                single = request.files.get("cv")
                if single:
                    uploaded = [single]

            cvs = []
            for f in uploaded:
                name = f.filename or "uploaded"
                text = _decode_file_storage(f)
                cvs.append((name, text))

            if not cvs:
                plain = request.form.get("cv_text")
                if plain:
                    cvs = [("cv_text", plain)]

            # weights
            try:
                emb_w = float(request.form.get("emb_w", 0.7) or 0.7)
            except Exception:
                emb_w = 0.7
            try:
                kw_w = float(request.form.get("kw_w", 0.3) or 0.3)
            except Exception:
                kw_w = 0.3

            # normalize weights if sum == 0
            s = emb_w + kw_w
            if s == 0:
                emb_w, kw_w = 0.7, 0.3
            else:
                emb_w, kw_w = emb_w / s, kw_w / s

            # try to call real matcher, fall back to simple scorer
            results = []
            try:
                from matcher import batch_score  # may raise ImportError or runtime error

                raw = batch_score(job_text, [t for (_, t) in cvs], weights=(emb_w, kw_w))
                # normalize output into list of dicts with filename
                if isinstance(raw, dict):
                    for i, (name, _) in enumerate(cvs):
                        key = name if name in raw else i
                        val = raw.get(key, {})
                        if not isinstance(val, dict):
                            val = {"score": val}
                        results.append({"filename": name, **val})
                else:
                    for (name, _), r in zip(cvs, raw):
                        if isinstance(r, dict):
                            results.append({"filename": name, **r})
                        else:
                            results.append({"filename": name, "score": r})
            except Exception:
                logging.exception("matcher.batch_score failed; using fallback simple scorer")
                for name, text in cvs:
                    results.append({"filename": name, **_simple_score(job_text, text, emb_w, kw_w)})

            # if client requested CSV download return attachment
            if request.form.get("download") == "1":
                output = io.StringIO()
                writer = csv.writer(output)
                # header
                headers = ["filename", "embedding_score", "keyword_overlap", "combined_percent", "score"]
                writer.writerow(headers)
                for r in results:
                    writer.writerow(
                        [
                            r.get("filename"),
                            r.get("embedding_score", ""),
                            r.get("keyword_overlap", ""),
                            r.get("combined_percent", ""),
                            r.get("score", ""),
                        ]
                    )
                output.seek(0)
                return send_file(
                    io.BytesIO(output.getvalue().encode("utf-8")),
                    as_attachment=True,
                    download_name="results.csv",
                    mimetype="text/csv",
                )

            return render_template("index.html", results=results, cvs=cvs, job_text=job_text, emb_w=emb_w, kw_w=kw_w)

        except Exception:
            tb = traceback.format_exc()
            logging.error("Unhandled exception in POST /:\n%s", tb)
            # write to logfile
            try:
                with open(logfile, "a", encoding="utf-8") as fh:
                    fh.write("\n\n" + tb)
            except Exception:
                pass
            return Response(tb, status=500, mimetype="text/plain")

    # GET - provide safe defaults so template rendering won't fail
    return render_template(
        "index.html",
        results=[],
        cvs=[],
        job_text="",
        emb_w=0.7,
        kw_w=0.3,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
# ...existing code...