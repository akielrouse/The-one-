import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const data = await request.json();
  const endpoint = process.env.FORMSPREE_ENDPOINT || process.env.GENERIC_WEBHOOK_URL;
  if (!endpoint) {
    console.error('No endpoint configured');
    return NextResponse.json({ error: 'No endpoint configured' }, { status: 500 });
  }
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      return NextResponse.json({ success: true });
    }
    return NextResponse.json({ error: 'Error sending form' }, { status: 500 });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
