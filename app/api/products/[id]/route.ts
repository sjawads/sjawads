import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const PATCH = async (req: Request, { params }: { params: { id: string } }) => ok(await prisma.product.update({ where: { id: Number(params.id) }, data: await req.json() }));
