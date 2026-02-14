import { InvoiceStatus } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { bad, ok } from '@/lib/http';

export async function POST(_: Request, { params }: { params: { id: string } }) {
  const id = Number(params.id);
  const invoice = await prisma.invoice.findUnique({ where: { id }, include: { tankers: true } });
  if (!invoice || invoice.status !== InvoiceStatus.DRAFT) return bad('only draft can finalize');
  const sums = invoice.tankers.reduce((a, t) => ({ afn: a.afn + Number(t.customerDebtAfnCalc), usd: a.usd + Number(t.customerDebtUsdCalc), ik: a.ik + Number(t.customerInKindCalc) }), { afn: 0, usd: 0, ik: 0 });

  await prisma.invoice.update({ where: { id }, data: { status: InvoiceStatus.FINAL, tankerCountFinal: invoice.tankers.length, totalCustomerAfnFinal: sums.afn, totalCustomerUsdFinal: sums.usd, totalInKindFinal: sums.ik } });
  for (const t of invoice.tankers) {
    await prisma.tanker.update({ where: { id: t.id }, data: { customerDebtAfnFinal: t.customerDebtAfnCalc, customerDebtUsdFinal: t.customerDebtUsdCalc, customerInKindFinal: t.customerInKindCalc, supplierRecvAfnFinal: t.supplierRecvAfnCalc, supplierRecvUsdFinal: t.supplierRecvUsdCalc } });
  }
  return ok({ success: true });
}
