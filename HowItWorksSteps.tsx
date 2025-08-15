export default function HowItWorksSteps() {
  const steps = [
    { title: 'Profile', description: 'A visual, 7-minute intake that captures how you live.' },
    { title: 'Enrich', description: 'Address + photos → light, quiet, flow, walkability. Badges: Potential / Verified.' },
    { title: 'Match & Tour', description: 'Six explained matches. Pick three; tour within 48–96 hours.' },
  ];
  return (
    <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
      {steps.map((s, idx) => (
        <div key={idx} className="bg-white shadow p-6 rounded">
          <h3 className="font-display text-2xl mb-2">{s.title}</h3>
          <p>{s.description}</p>
        </div>
      ))}
    </div>
  );
}
