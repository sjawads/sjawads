import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const GET = async (_: Request, { params }: { params: { id: string } }) => ok(await prisma.contract.findUnique({ where: { id: Number(params.id) }, include: { invoices: true, customerAccount: true, product: true } }));
