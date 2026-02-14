import { AccountType, Currency } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { bad, ok } from '@/lib/http';

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const type = searchParams.get('type') as AccountType | null;
  const active = searchParams.get('active');
  return ok(await prisma.account.findMany({ where: { accountType: type ?? undefined, isActive: active ? active === 'true' : undefined } }));
}

export async function POST(req: Request) {
  const body = await req.json();
  if (body.accountType === AccountType.MONEY && !body.currency) return bad('currency required for MONEY');
  return ok(await prisma.account.create({ data: { name: body.name, accountType: body.accountType, currency: body.currency as Currency | null, note: body.note } }));
}
