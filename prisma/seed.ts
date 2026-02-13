import { PrismaClient, AccountType, Currency } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const roles = ['Admin', 'Accountant', 'DataEntry', 'Viewer'];
  for (const name of roles) {
    await prisma.role.upsert({ where: { name }, update: {}, create: { name } });
  }

  await prisma.account.upsert({
    where: { id: 1 },
    update: {},
    create: { name: 'Sarafi_AFN', accountType: AccountType.MONEY, currency: Currency.AFN }
  });
  await prisma.account.upsert({
    where: { id: 2 },
    update: {},
    create: { name: 'Sarafi_USD', accountType: AccountType.MONEY, currency: Currency.USD }
  });
}

main().finally(() => prisma.$disconnect());
