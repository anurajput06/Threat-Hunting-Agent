/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        base: "#F4F5F7",
        panel: "#FFFFFF",
        panelAlt: "#F0F2F5",
        border: "#E1E4E9",
        cyan: "#0284C7",
        amber: "#D97706",
        orange: "#EA580C",
        crimson: "#DC2626",
        emerald: "#059669",
        textPrimary: "#1A1D23",
        textMuted: "#6B7280",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(2,132,199,0.12), 0 4px 16px rgba(2,132,199,0.06)",
      },
    },
  },
  plugins: [],
}
