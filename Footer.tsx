import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-sand py-8 px-4">
      <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
        <div>
          <p className="font-display mb-2">10 Gates Studios</p>
          <p>Vancouver, BC</p>
        </div>
        <div>
          <ul className="space-y-2">
            <li><Link href="/privacy">Privacy</Link></li>
            <li><Link href="/pricing">Pricing</Link></li>
            <li><Link href="/contact">Contact</Link></li>
          </ul>
        </div>
        <div>
          <p>© {new Date().getFullYear()} 10 Gates Studios</p>
        </div>
      </div>
    </footer>
  );
}
