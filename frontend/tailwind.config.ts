import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Georgia", "Cambria", "Times New Roman", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        paper: {
          50: "#faf9f6",
          100: "#f5f3ee",
          200: "#e8e4db",
          300: "#d4cec2",
          400: "#b8b0a0",
          500: "#9c917f",
          600: "#827563",
          700: "#6b5f50",
          800: "#5a5044",
          900: "#4d453b",
        },
        ink: {
          DEFAULT: "#1a1a1a",
          light: "#4a4a4a",
          muted: "#7a7a7a",
        },
        accent: {
          blue: "#2563eb",
          green: "#16a34a",
          yellow: "#ca8a04",
          orange: "#ea580c",
          red: "#dc2626",
        },
      },
    },
  },
  plugins: [],
};

export default config;
