/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {
    colors: { ink:"#182230", primary:"#4f46e5", lilac:"#7c3aed", mint:"#dff8ed", sky:"#eaf4ff" },
    boxShadow: { soft:"0 14px 40px rgba(37, 50, 85, .08)" }
  }},
  plugins: []
};
