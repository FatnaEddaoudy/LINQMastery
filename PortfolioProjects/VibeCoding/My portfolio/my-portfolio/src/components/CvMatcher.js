import React, { useEffect, useState } from 'react';
import './CvMatcher.css';

// Simple client-side CV matcher and download authorization
export default function CvMatcher() {
  const cvFiles = ['cv_fatna.txt', 'cv_john.txt', 'cv_jane.txt'];
  const [cvs, setCvs] = useState([]);
  const [jobDesc, setJobDesc] = useState('');
  const [results, setResults] = useState([]);
  const [downloadAuth, setDownloadAuth] = useState({}); // {filename: bool}
  const PASSWORD = 'letmein'; // simple client-side 'authorization' password

  useEffect(() => {
    // load CV texts from public/cvs
    Promise.all(cvFiles.map(f => fetch(`/cvs/${f}`).then(r => r.text()).then(text => ({ filename: f, text })) ))
      .then(setCvs)
      .catch(err => console.error('Failed to load CVs', err));
  }, []);

  const tokenize = (s) => s
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .filter(w => w.length > 2)
    .filter(w => !['and','the','for','with','that','this','from','have','will','are','but','not','you','your','our'].includes(w));

  const match = () => {
    const jdTokens = new Set(tokenize(jobDesc));
    const scored = cvs.map(cv => {
      const tokens = tokenize(cv.text);
      const tokenSet = new Set(tokens);
      let matches = 0;
      jdTokens.forEach(t => { if (tokenSet.has(t)) matches++; });
      const score = jdTokens.size ? Math.round((matches / jdTokens.size) * 100) : 0;
      return { ...cv, score, matches };
    }).sort((a,b) => b.score - a.score);
    setResults(scored);
  };

  const requestDownload = (filename) => {
    setDownloadAuth({ [filename]: true });
  };

  const confirmDownload = (filename, password) => {
    if (password === PASSWORD) {
      // trigger download
      const a = document.createElement('a');
      a.href = `/cvs/${filename}`;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setDownloadAuth({});
    } else {
      alert('Wrong password');
    }
  };

  return (
    <div className="cv-matcher">
      <h3>CV Matcher</h3>
      <p>Paste a job description and press <b>Match CVs</b>. The app will score each CV by simple keyword overlap. To download a CV you must enter the authorization password.</p>
      <textarea
        placeholder="Paste job description here..."
        value={jobDesc}
        onChange={e => setJobDesc(e.target.value)}
      />
      <div className="cv-actions">
        <button onClick={match}>Match CVs</button>
        <button onClick={() => { setJobDesc(''); setResults([]); }}>Clear</button>
      </div>

      <div className="cv-results">
        {results.length === 0 ? <p>No results yet.</p> : (
          <table>
            <thead>
              <tr><th>CV</th><th>Score</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {results.map(r => (
                <tr key={r.filename}>
                  <td>{r.filename}</td>
                  <td>{r.score}%</td>
                  <td>
                    <button onClick={() => requestDownload(r.filename)}>Download</button>
                    {downloadAuth[r.filename] && (
                      <span className="auth-box">
                        <input type="password" placeholder="password" id={`pw-${r.filename}`} />
                        <button onClick={() => {
                          const pw = document.getElementById(`pw-${r.filename}`).value;
                          confirmDownload(r.filename, pw);
                        }}>Confirm</button>
                        <button onClick={() => setDownloadAuth({})}>Cancel</button>
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
