'use client';
import { useState } from 'react';

export default function LeadForm() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const formData = new FormData(e.currentTarget);
    const payload = {
      name: formData.get('name'),
      email: formData.get('email'),
      role: formData.get('role'),
      officeSize: formData.get('officeSize'),
      city: formData.get('city'),
    };
    try {
      const res = await fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        if (typeof window !== 'undefined') {
          // @ts-ignore
          window.gtag && window.gtag('event', 'lead_submit');
        }
        window.location.href = '/thanks';
      } else {
        setError('There was a problem submitting your information.');
      }
    } catch (err) {
      setError('There was a problem submitting your information.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto flex flex-col gap-4 bg-white p-6 rounded">
      {error && <p className="text-red-600">{error}</p>}
      <input required name="name" placeholder="Name" className="border p-2 rounded" />
      <input required type="email" name="email" placeholder="Email" className="border p-2 rounded" />
      <select name="role" className="border p-2 rounded">
        <option value="agent">Agent</option>
        <option value="broker">Broker</option>
        <option value="developer">Developer</option>
      </select>
      <input name="officeSize" placeholder="Office size" className="border p-2 rounded" />
      <input name="city" placeholder="City" className="border p-2 rounded" />
      <button type="submit" className="bg-accent text-white py-2 rounded hover:bg-opacity-90" disabled={loading}>
        {loading ? 'Submitting…' : 'Get 20 free intakes'}
      </button>
    </form>
  );
}
