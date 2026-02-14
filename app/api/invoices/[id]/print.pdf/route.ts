import { prisma } from '@/lib/prisma';

export async function GET(_: Request, { params }: { params: { id: string } }) {
  const invoice = await prisma.invoice.findUnique({ where: { id: Number(params.id) }, include: { tankers: true } });
  if (!invoice) return new Response('not found', { status: 404 });
  const html = `<html><body><h1>${invoice.invoiceNo}</h1><p>PDF endpoint placeholder. Use Puppeteer in production deployment.</p></body></html>`;
  return new Response(html, { headers: { 'Content-Type': 'text/html' } });
}
