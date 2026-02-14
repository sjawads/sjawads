import { prisma } from '@/lib/prisma';

export default async function PrintPage({ params }: { params: { id: string } }) {
  const invoice = await prisma.invoice.findUnique({ where: { id: Number(params.id) }, include: { contract: true, tankers: true } });
  if (!invoice) return <div>Not found</div>;
  const showCol = (key: keyof (typeof invoice.tankers)[number]) => invoice.tankers.some((t: any) => Number(t[key]) !== 0);

  return <main><h1>Invoice {invoice.invoiceNo}</h1><p>Status: {invoice.status}</p><table border={1}><thead><tr><th>#</th><th>Weight</th>{showCol('mahsuli') && <th>mahsuli</th>}{showCol('fawaed') && <th>fawaed</th>}<th>Cust AFN</th><th>Cust USD</th></tr></thead><tbody>{invoice.tankers.map((t, i) => <tr key={t.id}><td>{i + 1}</td><td>{String(t.tonBasis) === 'PRODUCT' ? Number(t.productWeight) : Number(t.billWeight)}</td>{showCol('mahsuli') && <td>{Number(t.mahsuli)}</td>}{showCol('fawaed') && <td>{Number(t.fawaed)}</td>}<td>{Number(t.customerDebtAfnCalc)}</td><td>{Number(t.customerDebtUsdCalc)}</td></tr>)}</tbody></table></main>;
}
