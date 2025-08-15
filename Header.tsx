import Link from 'next/link';

export default function Header() {
  return (
    <header className="flex items-center justify-between px-4 py-3 bg-white shadow sticky top-0 z-50">
      <Link href="/" className="font-display text-2xl">10 Gates</Link>
      <nav className="hidden md:flex gap-6">
        <Link href="/how-it-works">How it Works</Link>
        <Link href="/for-agents">For Agents</Link>
        <Link href="/for-developers">For Developers</Link>
        <Link href="/pricing">Pricing</Link>
        <Link href="/case-studies">Case Studies</Link>
        <Link href="/contact">Contact</Link>
      </nav>
      <Link href="/for-agents" className="bg-accent text-white px-4 py-2 rounded hover:bg-opacity-90">
        Get 20 free intakes
      </Link>
    </header>
  );
}
