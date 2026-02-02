/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 듀오링고 스타일 컬러 팔레트
        primary: {
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981', // 민트 그린 (메인)
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
        },
        secondary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // 게이미피케이션 컬러
        combo: '#f59e0b',      // 콤보 (앰버)
        streak: '#ef4444',     // 연속 정답 (레드)
        levelup: '#8b5cf6',    // 레벨업 (퍼플)
        correct: '#22c55e',    // 정답 (그린)
        incorrect: '#ef4444',  // 오답 (레드)
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
      },
      animation: {
        'bounce-once': 'bounce 0.5s ease-in-out 1',
        'shake': 'shake 0.5s ease-in-out',
        'pulse-fast': 'pulse 0.5s ease-in-out infinite',
        'confetti': 'confetti 1s ease-out forwards',
      },
      keyframes: {
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        },
        confetti: {
          '0%': { transform: 'scale(0) rotate(0deg)', opacity: 1 },
          '100%': { transform: 'scale(1) rotate(360deg)', opacity: 0 },
        },
      },
    },
  },
  plugins: [],
}
