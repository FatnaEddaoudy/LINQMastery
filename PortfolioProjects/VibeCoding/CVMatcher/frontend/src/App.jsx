import React, { useState } from "react";
import ThemeToggle from "./components/ThemeToggle";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [results, setResults] = useState([]);

  return (
    <div className={`${darkMode ? "dark" : ""} min-h-screen`}>
      <div className={`min-h-screen p-8 transition-colors duration-300
        ${darkMode ? "bg-darkBackground text-darkTextPrimary" : "bg-background text-textPrimary"}`}>

        {/* ===== Top Navbar / Header ===== */}
        <div className="flex justify-between items-center mb-8">
          <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
          <h1 className="text-3xl font-bold ml-4">HR CV Matching</h1>
        </div>

        {/* ===== Step 1/2 Form ===== */}
        <UploadForm setResults={setResults} darkMode={darkMode} />

        {/* ===== Step 3 Results ===== */}
        <Results results={results} darkMode={darkMode} />
        
      </div>
    </div>
  );
}

export default App;
