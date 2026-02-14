import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const GET = async () => ok(await prisma.product.findMany());
export const POST = async (req: Request) => ok(await prisma.product.create({ data: await req.json() }));
