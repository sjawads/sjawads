'use client';
import { useEffect, useState } from 'react';

export default function InvoicePage({ params }: { params: { id: string } }) {
  const [invoice, setInvoice] = useState<any>(null);
  const [paste, setPaste] = useState('');
  const load = async () => setInvoice(await (await fetch(`/api/invoices/${params.id}`)).json());
  useEffect(() => { load(); }, [params.id]);
  const batch = async () => {
    const rows = paste.trim().split('\n').filter(Boolean).map(r => { const [portId, productWeight, billWeight, exchangeRate] = r.split('\t'); return { portId: Number(portId), productWeight: Number(productWeight), billWeight: Number(billWeight), exchangeRate: Number(exchangeRate), tonBasis: 'PRODUCT' }; });
    await fetch(`/api/invoices/${params.id}/tankers/batchUpsert`, { method: 'POST', body: JSON.stringify({ rows }) });
    await load();
  };
  return <main><h2>Invoice {invoice?.invoiceNo}</h2><p>Status: {invoice?.status}</p><textarea rows={8} cols={80} value={paste} onChange={e => setPaste(e.target.value)} placeholder='Paste tab-separated rows: portId productWeight billWeight exchangeRate' /><br /><button onClick={batch} disabled={invoice?.status !== 'DRAFT'}>Batch Upsert</button><button onClick={async()=>{await fetch(`/api/invoices/${params.id}/finalize`,{method:'POST'});load();}} disabled={invoice?.status!=='DRAFT'}>Finalize</button><a href={`/invoices/${params.id}/print`}>Print</a><pre>{JSON.stringify(invoice, null, 2)}</pre></main>;
}
