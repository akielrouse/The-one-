import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx,jsx,js}','./app/components/**/*.{ts,tsx,jsx,js}','./components/**/*.{ts,tsx,jsx,js}'],
  theme: {
    extend: {
      colors: { ink:'#0B0F14', stone:'#F3F4F6', sand:'#E8E3DA', accent:'#4169E1' },
      fontFamily: { display:['var(--font-fraunces)','serif'], sans:['var(--font-inter)','sans-serif'] },
    },
  },
  plugins: [],
};
export default config;
