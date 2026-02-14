# Tanker Accounting Web App (MVP)

Next.js 14.2 + TypeScript + Prisma + PostgreSQL implementation of tanker accounting with contracts, invoices, tanker rows, payments/exchange, in-kind, reports, and printable invoice views.

## Stack
- Next.js App Router (`next@14.2.5`, stable webpack dev)
- TypeScript
- PostgreSQL
- Prisma ORM
- Docker Compose (db + app)

## 1) Local setup (without Docker)
```bash
cp .env.example .env
npm install
npx prisma migrate dev --name init
npx prisma db seed
npm run dev
```

> Note: `npm run build` now runs `prisma generate` automatically via `prebuild`, preventing missing Prisma enum/client types during Docker and CI builds.


## 2) Docker setup (dev)
```bash
docker compose up -d db
cp .env.example .env
npm install
npx prisma migrate dev --name init
npx prisma db seed
npm run dev
```



Or run full app+db in compose:
```bash
docker compose up --build
```

## 3) Production (Docker)
```bash
docker build -t tanker-accounting .
docker run -p 3000:3000 --env-file .env tanker-accounting
```

## Core routes
- `/accounts`, `/products`, `/ports`, `/contracts`
- `/invoices/:id` (batch tanker paste/upsert + finalize)
- `/transactions`, `/in-kind`
- `/invoices/:id/print`
- `/api/invoices/:id/print.pdf` (HTML placeholder endpoint for puppeteer wiring)

## Seed data
- Roles: Admin, Accountant, DataEntry, Viewer
- Money accounts: Sarafi_AFN, Sarafi_USD
