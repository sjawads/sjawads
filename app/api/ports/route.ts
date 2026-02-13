import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export const GET = async () => ok(await prisma.port.findMany());
export const POST = async (req: Request) => ok(await prisma.port.create({ data: await req.json() }));
