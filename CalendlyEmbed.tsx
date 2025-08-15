'use client';
import { useEffect } from 'react';

export default function CalendlyEmbed() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    script.async = true;
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script);
    };
  }, []);
  const url = process.env.NEXT_PUBLIC_CALENDLY_URL || '';
  return (
    <div className="calendly-inline-widget" data-url={url} style={{ minWidth: '320px', height: '630px' }}></div>
  );
}
