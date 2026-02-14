import { Direction } from '@prisma/client';
import { prisma } from '@/lib/prisma';
import { ok } from '@/lib/http';

export async function POST(req: Request) {
  const b = await req.json();
  const payment = await prisma.transactionHeader.create({
    data: {
      date: new Date(b.date || new Date()),
      partyAccountId: b.partyAccountId,
      contractId: b.contractId,
      invoiceId: b.invoiceId,
      note: b.note,
      lines: { create: [{ moneyAccountId: b.moneyAccountId, direction: b.direction || Direction.IN, amount: b.amount }] }
    }, include: { lines: true }
  });

  let exchange = null;
  if (b.exchangeRate && b.targetMoneyAccountId) {
    const targetAmount = Number(b.amount) / Number(b.exchangeRate);
    exchange = await prisma.transactionHeader.create({
      data: {
        date: new Date(b.date || new Date()),
        note: 'exchange transfer',
        exchangeRate: b.exchangeRate,
        lines: {
          create: [
            { moneyAccountId: b.moneyAccountId, direction: Direction.OUT, amount: b.amount },
            { moneyAccountId: b.targetMoneyAccountId, direction: Direction.IN, amount: targetAmount }
          ]
        }
      }, include: { lines: true }
    });
  }
  return ok({ payment, exchange });
}
