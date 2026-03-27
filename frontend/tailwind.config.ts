import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Playfair Display", "Georgia", "Cambria", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
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
          DEFAULT: "#0f172a",
          light: "#334155",
          muted: "#64748b",
        },
        accent: {
          blue: "#2563eb",
          green: "#16a34a",
          yellow: "#ca8a04",
          orange: "#ea580c",
          red: "#dc2626",
        },
        navy: {
          50: "#f0f4ff",
          100: "#e0e8ff",
          700: "#1e3a5f",
          800: "#172e4a",
          900: "#0f172a",
        },
      },
    },
  },
  plugins: [],
};

export default config;
