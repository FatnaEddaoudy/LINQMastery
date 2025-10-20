from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

app.config['UPLOAD_FOLDER'] = 'uploads'

# Load model once (all-MiniLM-L6-v2 is small and fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ""

@app.route("/", methods=["GET"])
def home():
    return "CV Matcher backend is running. Use /match endpoint to POST data."

@app.route("/match", methods=["POST"])
def match():
    job_description = request.form.get("job_description", "")
    files = request.files.getlist("cvs")

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400
    if not files:
        return jsonify({"error": "No CVs uploaded"}), 400

    resumes = []
    filenames = []

    # Save files and extract text
    for file in files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        filenames.append(file.filename)
        resumes.append(extract_text(filepath))
        print(f"Uploaded: {file.filename}")  # debug log

    # Compute embeddings
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embeddings = model.encode(resumes, convert_to_tensor=True)
    cos_scores = util.cos_sim(job_embedding, resume_embeddings)[0].cpu().numpy()

    # Prepare results
    results = pd.DataFrame({'Resume': filenames, 'Score': cos_scores})
    results = results.sort_values(by='Score', ascending=False)

    print("Matching done!")  # debug log
    return jsonify(results.to_dict(orient="records"))

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
