import { InvoiceStatus } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const POST = async (_: Request, { params }: { params: { id: string } }) => ok(await prisma.invoice.update({ where: { id: Number(params.id) }, data: { status: InvoiceStatus.CANCELED } }));
