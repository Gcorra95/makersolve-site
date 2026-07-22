/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './*/index.html',
    './servizi/*/index.html',
    './assets/*.js',
  ],
  // classi attivate da JS: vanno protette dal purge
  safelist: [
    'bg-ink/80', 'backdrop-blur-xl', 'border-white/10', 'border-transparent',
    'border-copper/50', 'bg-ink-700', 'in',
  ],
  theme: {
    extend: {
      colors: {
        // grafite caldo — fondo e superfici
        ink: {
          DEFAULT: '#12100E',
          800: '#1C1917',
          700: '#292524',
          600: '#3A3532',
        },
        // rame / ambra — accento
        copper: {
          DEFAULT: '#C87137',
          light: '#E8A33D',
          dim: 'rgba(200,113,55,.28)',
        },
        bone: {
          DEFAULT: '#FAFAF9',
          dim: '#A8A29E',
          dimmer: '#78716C',
        },
        // superfici chiare
        paper: {
          DEFAULT: '#FAF9F7',
          200: '#F1EEEA',
          line: '#E2DDD6',
          ink: '#1C1917',
          dim: '#6B635C',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      letterSpacing: {
        tightest: '-.045em',
      },
      maxWidth: {
        wrap: '1200px',
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(.22,.61,.36,1)',
        out: 'cubic-bezier(.16,1,.3,1)',
      },
      keyframes: {
        drift: { to: { backgroundPosition: '72px 72px, 72px 72px' } },
        breathe: {
          '0%,100%': { opacity: '.55', transform: 'translate(-50%,-50%) scale(1)' },
          '50%': { opacity: '.9', transform: 'translate(-50%,-50%) scale(1.14)' },
        },
        ring: {
          '70%': { boxShadow: '0 0 0 11px rgba(232,163,61,0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(232,163,61,0)' },
        },
        marquee: { to: { transform: 'translateX(-50%)' } },
        kenburns: {
          from: { transform: 'scale(1.03) translate3d(0,0,0)' },
          to: { transform: 'scale(1.16) translate3d(-1.5%,0,0)' },
        },
      },
      animation: {
        drift: 'drift 44s linear infinite',
        breathe: 'breathe 11s ease-in-out infinite',
        ring: 'ring 2.4s infinite',
        marquee: 'marquee 38s linear infinite',
        kenburns: 'kenburns 28s ease-in-out infinite alternate',
      },
    },
  },
  plugins: [],
}
