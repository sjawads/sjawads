import { Direction, InvoiceStatus } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const customerId = Number(searchParams.get('customerId'));
  const invoices = await prisma.invoice.findMany({ where: { status: { in: [InvoiceStatus.DRAFT, InvoiceStatus.FINAL] }, contract: { customerAccountId: customerId } }, include: { tankers: true } });
  const debt = invoices.flatMap(i => i.tankers).reduce((a, t) => ({ afn: a.afn + Number(t.customerDebtAfnCalc), usd: a.usd + Number(t.customerDebtUsdCalc), inKind: a.inKind + Number(t.customerInKindCalc) }), { afn: 0, usd: 0, inKind: 0 });
  const tx = await prisma.transactionHeader.findMany({ where: { partyAccountId: customerId }, include: { lines: true } });
  const paid = tx.flatMap(t => t.lines).reduce((a, l) => ({ afn: a.afn + (l.direction === Direction.IN ? Number(l.amount) : -Number(l.amount)), usd: a.usd }), { afn: 0, usd: 0 });
  const ik = await prisma.inKindTransaction.findMany({ where: { customerAccountId: customerId } });
  const ikNet = ik.reduce((a, t) => a + (t.direction === Direction.IN ? Number(t.qty) : -Number(t.qty)), 0);
  return ok({ afn: debt.afn - paid.afn, usd: debt.usd - paid.usd, inKind: debt.inKind - ikNet });
}
