import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const GET = async () => ok(await prisma.inKindTransaction.findMany({ orderBy: { id: 'desc' } }));
export const POST = async (req: Request) => ok(await prisma.inKindTransaction.create({ data: await req.json() }));
