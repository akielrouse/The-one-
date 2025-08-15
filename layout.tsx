import './globals.css';
import { Fraunces, Inter } from 'next/font/google';
import type { Metadata } from 'next';
import { ReactNode } from 'react';
import Script from 'next/script';
import Header from './components/Header';
import Footer from './components/Footer';

const fraunces = Fraunces({ subsets: ['latin'], variable: '--font-fraunces' });
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: '10 Gates Studios | Architect-grade marketing + buyer-fit AI (Vancouver)',
  description:
    'Market like architects and match like psychologists. 7-minute Design DNA™ + AI-enriched listings that book tours faster.',
  openGraph: {
    title: '10 Gates Studios | Architect-grade marketing + buyer-fit AI (Vancouver)',
    description: 'Market like architects and match like psychologists.',
    url: 'https://example.com',
    siteName: '10 Gates Studios',
    locale: 'en_CA',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${fraunces.variable} ${inter.variable}`}>
      <head>
        {process.env.NEXT_PUBLIC_GA_ID && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
              strategy="afterInteractive"
            />
            <Script id="gtag-init" strategy="afterInteractive">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}', {
                  page_path: window.location.pathname,
                });
              `}
            </Script>
          </>
        )}
      </head>
      <body className="bg-stone text-ink font-sans">
        <Header />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
