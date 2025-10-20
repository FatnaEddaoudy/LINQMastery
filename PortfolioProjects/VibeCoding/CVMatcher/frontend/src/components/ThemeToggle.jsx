import React from "react";

export default function ThemeToggle({ darkMode, setDarkMode }) {
  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="px-4 py-2 rounded-md bg-primary text-white hover:bg-blue-600 transition"
    >
      {darkMode ? "Light Mode" : "Dark Mode"}
    </button>
  );
}
