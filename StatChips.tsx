export default function StatChips() {
  const stats = [
    { label: 'Time-to-Tour ↓', value: '30–50%' },
    { label: 'Tours/Offer ↓', value: '25%' },
    { label: 'Felt-Seen ↑', value: '8/10' },
  ];
  return (
    <div className="flex justify-center gap-4">
      {stats.map((s, idx) => (
        <div key={idx} className="border border-accent text-accent px-4 py-2 rounded-full text-sm">
          {s.label} {s.value}
        </div>
      ))}
    </div>
  );
}
