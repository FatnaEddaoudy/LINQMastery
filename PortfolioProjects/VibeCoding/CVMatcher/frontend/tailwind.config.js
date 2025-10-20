module.exports = {
  darkMode: "class", // important!
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "hsl(220,75%,45%)",
        background: "hsl(0,0%,98%)",
        surface: "hsl(0,0%,100%)",
        textPrimary: "hsl(220,15%,20%)",
        textSecondary: "hsl(220,10%,45%)",
        success: "hsl(145,60%,45%)",
        borderColor: "hsl(220,15%,88%)",
        darkBackground: "hsl(220,15%,12%)",
        darkSurface: "hsl(220,12%,16%)",
        darkTextPrimary: "hsl(220,10%,95%)",
        darkTextSecondary: "hsl(220,10%,65%)",
        darkSuccess: "hsl(145,55%,55%)",
        darkBorder: "hsl(220,12%,22%)",
      },
    },
  },
  plugins: [],
};
