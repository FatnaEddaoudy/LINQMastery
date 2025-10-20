import React from "react";

export default function Results({ results, darkMode }) {
  const getScoreColor = (score) => {
    if (score >= 0.8) return "bg-green-500";
    if (score >= 0.6) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="overflow-x-auto">
      <table className={`w-full border-collapse shadow-md
        ${darkMode ? "text-darkTextPrimary" : "text-textPrimary"}`}>
        <thead className={`${darkMode ? "bg-darkSurface" : "bg-surface"} text-left`}>
          <tr>
            <th className="p-4 border-b">Resume</th>
            <th className="p-4 border-b">Score</th>
            <th className="p-4 border-b">Skills</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, idx) => (
            <tr key={idx} className={`${darkMode ? "bg-darkBackground" : "bg-background"} hover:bg-gray-100 dark:hover:bg-gray-700`}>
              <td className="p-4 border-b">{r.Resume}</td>
              
              {/* Score with colored circle */}
              <td className="p-4 border-b flex items-center">
                <span className={`w-4 h-4 rounded-full mr-2 ${getScoreColor(r.Score)}`}></span>
                {Math.round(r.Score * 100)}%
              </td>

              {/* Skills with matched/unmatched color */}
              <td className="p-4 border-b">
                <div className="flex flex-wrap gap-2">
                  {r.skills?.map((skill, i) => (
                    <span
                      key={i}
                      className={`px-2 py-1 rounded-full text-xs font-semibold
                        ${skill.present ? "bg-green-500 text-white" : "bg-red-200 text-red-800"}`}
                    >
                      {skill.name}
                    </span>
                  ))}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
