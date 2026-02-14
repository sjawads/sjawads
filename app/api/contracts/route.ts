import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const GET = async () => ok(await prisma.contract.findMany({ include: { customerAccount: true, product: true } }));
export const POST = async (req: Request) => ok(await prisma.contract.create({ data: await req.json() }));
