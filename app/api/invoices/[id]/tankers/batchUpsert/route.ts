import { InvoiceStatus, TonBasis } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { bad, ok } from '@/lib/http';
import { calculateTanker } from '@/lib/calc';

export async function POST(req: Request, { params }: { params: { id: string } }) {
  const invoiceId = Number(params.id);
  const body = await req.json();
  const rows = body.rows || [];
  const invoice = await prisma.invoice.findUnique({ where: { id: invoiceId }, include: { contract: true } });
  if (!invoice) return bad('invoice not found', 404);
  if (invoice.status !== InvoiceStatus.DRAFT) return bad('invoice locked');

  const results = [];
  const errors: any[] = [];
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    try {
      const port = await prisma.port.findUniqueOrThrow({ where: { id: Number(row.portId) } });
      const calc = calculateTanker({ ...row, tonBasis: row.tonBasis ?? TonBasis.PRODUCT, calcType: invoice.contract.calcType });
      const data: any = { ...row, invoiceId, contractId: invoice.contractId, supplierAccountId: port.supplierAccountId, ...calc };
      const saved = row.id
        ? await prisma.tanker.update({ where: { id: Number(row.id) }, data })
        : await prisma.tanker.create({ data });
      results.push(saved);
    } catch (e: any) {
      errors.push({ index: i, message: e.message });
    }
  }
  return ok({ rows: results, errors });
}
