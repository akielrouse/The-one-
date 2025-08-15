interface Props {
  study: {
    id: string;
    title: string;
    problem: string;
    intervention: string;
    kpi_delta: string;
    quote: string;
    media: string;
  };
}

export default function CaseCard({ study }: Props) {
  return (
    <article className="border p-6 rounded bg-white">
      <h3 className="font-display text-2xl mb-2">{study.title}</h3>
      <p className="mb-2"><strong>Problem:</strong> {study.problem}</p>
      <p className="mb-2"><strong>Intervention:</strong> {study.intervention}</p>
      <p className="mb-2"><strong>KPI delta:</strong> {study.kpi_delta}</p>
      <blockquote className="italic mb-4">“{study.quote}”</blockquote>
      <a href="#" className="text-accent underline">View details</a>
    </article>
  );
}
