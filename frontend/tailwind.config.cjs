/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                redAccent: {
                    100: "#f8dcdb",
                    200: "#f1b9b7",
                    300: "#e99592",
                    400: "#e2726e",
                    500: "#db4f4a",
                    600: "#af3f3b",
                    700: "#832f2c",
                    800: "#58201e",
                    900: "#2c100f",
                },
                blueAccent: {
                    100: "#e1e2fe",
                    200: "#c3c6fd",
                    300: "#a4a9fc",
                    400: "#868dfb",
                    500: "#6870fa",
                    600: "#535ac8",
                    700: "#3e4396",
                    800: "#2a2d64",
                    900: "#151632",
                },
            },
            keyframes: {
                'loading-bar': {
                  '0%': { transform: 'translateX(0px)' },
                  '100%': { transform: 'translateX(calc(100vw))' },
                },
                'gradient': {
                  '0%': { backgroundPosition: '0% 50%' },
                  '50%': { backgroundPosition: '100% 50%' },
                  '100%': { backgroundPosition: '0% 50%' },
                },
                'float': {
                  '0%, 100%': { transform: 'translateY(0px)' },
                  '50%': { transform: 'translateY(-20px)' },
                },
                'glow': {
                  '0%, 100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' },
                  '50%': { boxShadow: '0 0 40px rgba(59, 130, 246, 0.8)' },
                },
            },
            animation: {
                'loading-bar': 'loading-bar 2.5s infinite linear',
                'gradient': 'gradient 3s ease infinite',
                'float': 'float 6s ease-in-out infinite',
                'glow': 'glow 2s ease-in-out infinite',
            }
        },
    },
    plugins: [],
};