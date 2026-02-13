'use client';
import { useEffect, useState } from 'react';

export default function AccountsPage() {
  const [rows, setRows] = useState<any[]>([]);
  const [form, setForm] = useState<any>({ name: '', accountType: 'CUSTOMER', currency: '' });
  const load = async () => setRows(await (await fetch('/api/accounts')).json());
  useEffect(() => { load(); }, []);
  return <main><h2>Accounts</h2><input placeholder='name' onChange={e => setForm({ ...form, name: e.target.value })} /><select onChange={e => setForm({ ...form, accountType: e.target.value })}><option>CUSTOMER</option><option>SUPPLIER</option><option>MONEY</option><option>OTHER</option></select><select disabled={form.accountType !== 'MONEY'} onChange={e => setForm({ ...form, currency: e.target.value })}><option value=''>-</option><option>AFN</option><option>USD</option></select><button onClick={async () => { await fetch('/api/accounts', { method: 'POST', body: JSON.stringify(form) }); await load(); }}>Create</button><pre>{JSON.stringify(rows, null, 2)}</pre></main>;
}
