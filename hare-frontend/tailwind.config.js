/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#9B1C2C',
        secondary: '#4A2C1F',
        accent: '#D4AF37',
        background: '#F8F1EB',
        'text-primary': '#1F1F1F',
        'text-inverse': '#FFFFFF',
        bordeaux: {
          DEFAULT: '#9B1C2C',
          dark: '#7a1623',
          light: '#b32438',
        },
        cream: {
          DEFAULT: '#F8F1EB',
          light: '#FDF8F5',
        },
        gold: {
          DEFAULT: '#D4AF37',
          light: '#E5C76B',
        },
      },
      fontFamily: {
        serif: ['Cormorant Garamond', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
