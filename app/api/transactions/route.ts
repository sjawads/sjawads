import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const partyAccountId = searchParams.get('partyAccountId');
  return ok(await prisma.transactionHeader.findMany({ where: { partyAccountId: partyAccountId ? Number(partyAccountId) : undefined }, include: { lines: true }, orderBy: { id: 'desc' } }));
}
