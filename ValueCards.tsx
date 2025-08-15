export default function ValueCards() {
  const items = [
    { title: 'Cut Time-to-Tour.' },
    { title: 'Explainable matches (plain English reasons).' },
    { title: 'Premium listing pages with Potential/Verified badges.' },
  ];
  return (
    <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
      {items.map((item, idx) => (
        <div key={idx} className="bg-white shadow p-6 rounded">
          <h3 className="font-display text-xl mb-2">{item.title}</h3>
        </div>
      ))}
    </div>
  );
}
