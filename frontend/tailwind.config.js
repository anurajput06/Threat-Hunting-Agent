/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        base: "#0B0E14",
        panel: "#12161F",
        panelAlt: "#171C27",
        border: "#232833",
        cyan: "#4CC9F0",
        amber: "#F2A65A",
        orange: "#FF7A45",
        crimson: "#E5484D",
        emerald: "#3DDC97",
        textPrimary: "#E6E8EB",
        textMuted: "#8B93A1",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(76,201,240,0.15), 0 0 24px rgba(76,201,240,0.08)",
      },
    },
  },
  plugins: [],
}
