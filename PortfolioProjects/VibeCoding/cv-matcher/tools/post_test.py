# ...existing code...
import argparse
import sys
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent  # project root (cv-matcher)
DEFAULT_SAMPLE = BASE / "samples" / "cv1.txt"
DEFAULT_URL = "http://127.0.0.1:5000/"

def main():
    p = argparse.ArgumentParser(description="Post a job + CV(s) to the local Flask app for testing")
    p.add_argument("--url", "-u", default=DEFAULT_URL, help="Server URL")
    p.add_argument("--cv", "-c", action="append", help="Path to a CV file (can repeat). Default: samples/cv1.txt")
    p.add_argument("--job-file", "-j", help="Path to a job description file")
    p.add_argument("--job-text", help="Job description text (used if --job-file not provided)")
    p.add_argument("--timeout", "-t", type=int, default=120, help="Request timeout in seconds")
    args = p.parse_args()

    url = args.url
    cv_paths = [Path(p) for p in (args.cv or [str(DEFAULT_SAMPLE)])]
    for cv in cv_paths:
        if not cv.exists():
            print("CV file not found:", cv)
            sys.exit(2)

    if args.job_file:
        job_file = Path(args.job_file)
        if not job_file.exists():
            print("Job file not found:", job_file)
            sys.exit(3)
        job_text = job_file.read_text(encoding="utf-8", errors="ignore")
    else:
        job_text = args.job_text or "Test job description"

    open_files = []
    files = []
    try:
        for cv in cv_paths:
            fh = open(cv, "rb")
            open_files.append(fh)
            # requests expects a sequence of (fieldname, (filename, fileobj))
            files.append(("cvs", (cv.name, fh)))

        data = {"job_text": job_text}

        try:
            resp = requests.post(url, data=data, files=files, timeout=args.timeout)
        except requests.exceptions.Timeout:
            print(f"REQUEST TIMED OUT after {args.timeout}s")
            sys.exit(4)
        except requests.exceptions.RequestException as e:
            print("REQUEST ERROR:", e)
            sys.exit(5)

        print("STATUS", resp.status_code)
        print("LENGTH", len(resp.content))
        print("HEADERS:", dict(resp.headers))
        print("\n--- RESPONSE PREVIEW ---\n")
        print(resp.text[:4000])

        if resp.status_code >= 400:
            print("\nServer returned error. Full response below:\n")
            print(resp.text)
            sys.exit(1)

    finally:
        for fh in open_files:
            try:
                fh.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()
# ...existing code...