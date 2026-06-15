/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        amazon: {
          light: '#232F3E',
          DEFAULT: '#131921',
          orange: '#FF9900',
          yellow: '#FEBD69',
          blue: '#007185',
          background: '#EAEDED',
        }
      },
      fontFamily: {
        sans: ['Amazon Ember', 'Arial', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
