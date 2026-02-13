import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';
export async function PATCH(req: Request, { params }: { params: { id: string } }) {
  const body = await req.json();
  return ok(await prisma.account.update({ where: { id: Number(params.id) }, data: body }));
}
