export default function PricingTable() {
  const tiers = [
    { name: 'Solo', price: 'C$149', features: ['1 seat'], cta: 'Get started' },
    { name: 'Team (5)', price: 'C$499', features: ['5 seats'], cta: 'Start pilot' },
    { name: 'Brokerage', price: 'From C$1,999', features: ['25+ seats'], cta: 'Contact sales' },
  ];
  return (
    <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
      {tiers.map((tier, idx) => (
        <div key={idx} className="border p-6 rounded text-center bg-white">
          <h3 className="font-display text-xl mb-2">{tier.name}</h3>
          <p className="text-3xl font-bold mb-4">{tier.price}/mo</p>
          <ul className="mb-4 space-y-1">
            {tier.features.map((f, i) => (<li key={i}>{f}</li>))}
          </ul>
          <button className="bg-accent text-white px-4 py-2 rounded hover:bg-opacity-90">{tier.cta}</button>
        </div>
      ))}
    </div>
  );
}
