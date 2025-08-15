import Link from 'next/link';

export default function Hero() {
  return (
    <section className="bg-sand py-20 px-4 text-center">
      <h1 className="text-4xl md:text-6xl font-display mb-4">Market like architects. Match like psychologists.</h1>
      <p className="text-xl md:text-2xl mb-6">A 7-minute Design DNA™ + AI-enriched listings that book tours faster.</p>
      <Link href="/for-agents" className="bg-accent text-white py-3 px-6 rounded hover:bg-opacity-90">
        Get 20 free intakes
      </Link>
    </section>
  );
}
