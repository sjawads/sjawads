'use client';
import { useEffect, useState } from 'react';

export default function ContractsPage() {
  const [rows, setRows] = useState<any[]>([]);
  const [f, setF] = useState<any>({ customerAccountId: '', productId: '', contractCode: '', calcType: 'COST' });
  const load = async () => setRows(await (await fetch('/api/contracts')).json());
  useEffect(() => { load(); }, []);
  return <main><h2>Contracts</h2><input placeholder='customerAccountId' onChange={e => setF({ ...f, customerAccountId: Number(e.target.value) })} /><input placeholder='productId' onChange={e => setF({ ...f, productId: Number(e.target.value) })} /><input placeholder='contractCode' onChange={e => setF({ ...f, contractCode: e.target.value })} /><select onChange={e => setF({ ...f, calcType: e.target.value })}><option>COST</option><option>COST_USD</option><option>PER_TON</option></select><input placeholder='perTonAfnDefault' onChange={e => setF({ ...f, perTonAfnDefault: Number(e.target.value) })} /><input placeholder='perTonUsdDefault' onChange={e => setF({ ...f, perTonUsdDefault: Number(e.target.value) })} /><button onClick={async () => { await fetch('/api/contracts', { method: 'POST', body: JSON.stringify(f) }); load(); }}>Create</button><h3>Create Draft Invoice</h3><input id='cid' placeholder='contractId' /><button onClick={async () => { const id = (document.getElementById('cid') as HTMLInputElement).value; const r = await (await fetch('/api/invoices', { method: 'POST', body: JSON.stringify({ contractId: Number(id), invoiceDate: new Date() }) })).json(); alert(`Invoice ${r.invoiceNo} created with id ${r.id}`); }}>New Invoice</button><pre>{JSON.stringify(rows, null, 2)}</pre></main>;
}
