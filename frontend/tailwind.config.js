/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bli-low': '#22c55e',
        'bli-medium': '#eab308',
        'bli-high': '#f97316',
        'bli-critical': '#ef4444',
        'uidai-blue': '#1e40af',
        'uidai-orange': '#ea580c'
      }
    },
  },
  plugins: [],
}
