import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export async function GET(_: Request, { params }: { params: { id: string } }) {
  const invoice = await prisma.invoice.findUnique({ where: { id: Number(params.id) }, include: { contract: true, tankers: true } });
  if (!invoice) return ok(null);
  const totalCustomerAfn = invoice.tankers.reduce((a, t) => a + Number(t.customerDebtAfnCalc), 0);
  const totalCustomerUsd = invoice.tankers.reduce((a, t) => a + Number(t.customerDebtUsdCalc), 0);
  const totalInKind = invoice.tankers.reduce((a, t) => a + Number(t.customerInKindCalc), 0);
  return ok({ ...invoice, totals: { totalCustomerAfn, totalCustomerUsd, totalInKind } });
}
