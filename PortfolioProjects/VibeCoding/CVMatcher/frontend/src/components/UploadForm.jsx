import React, { useState } from "react";
import axios from "axios";

export default function UploadForm({ setResults }) {
  const [jobDesc, setJobDesc] = useState("");
  const [files, setFiles] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("job_description", jobDesc);
    for (let i = 0; i < files.length; i++) formData.append("cvs", files[i]);

    try {
      const res = await axios.post("http://localhost:5000/match", formData);
      setResults(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Step 1: Enter Job Description</h2>
      <textarea
        placeholder="Enter job description..."
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}  // ✅ added
        required
        rows={6}
        style={{ width: "100%" }}
      />

      <h2>Step 2: Upload CVs</h2>
      <input
        type="file"
        multiple
        onChange={(e) => setFiles(e.target.files)}
      />

      <button type="submit">Match CVs</button>
    </form>
  );
}
