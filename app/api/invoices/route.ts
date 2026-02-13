import { InvoiceStatus } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';

export async function POST(req: Request) {
  const body = await req.json();
  const contract = await prisma.contract.findUniqueOrThrow({ where: { id: body.contractId } });
  const maxSeq = await prisma.invoice.aggregate({ where: { contractId: body.contractId }, _max: { invoiceSeq: true } });
  const seq = (maxSeq._max.invoiceSeq ?? 0) + 1;
  const invoiceNo = `${contract.contractCode}-${String(seq).padStart(4, '0')}`;
  return ok(await prisma.invoice.create({ data: { contractId: body.contractId, invoiceDate: new Date(body.invoiceDate), description: body.description, invoiceSeq: seq, invoiceNo, status: InvoiceStatus.DRAFT } }));
}
