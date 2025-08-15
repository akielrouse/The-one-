import CalendlyEmbed from '../components/CalendlyEmbed';

export default function ThanksPage() {
  return (
    <div className="py-12 px-4">
      <h1 className="font-display text-4xl mb-6">Thank you!</h1>
      <p className="mb-4">Your request has been received. Please schedule your onboarding below.</p>
      <CalendlyEmbed />
    </div>
  );
}
