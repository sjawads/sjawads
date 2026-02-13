import { NextResponse } from 'next/server';
export const ok = (data: any) => NextResponse.json(data);
export const bad = (message: string, status = 400) => NextResponse.json({ error: message }, { status });
