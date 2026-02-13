'use client';
import { useEffect, useState } from 'react';

export default function TxPage() {
  const [rows, setRows] = useState<any[]>([]);
  const [f, setF] = useState<any>({ partyAccountId:'', moneyAccountId:'', amount:'', exchangeRate:'', targetMoneyAccountId:'' });
  const load = async () => setRows(await (await fetch('/api/transactions')).json());
  useEffect(()=>{load();},[]);
  return <main><h2>Transactions</h2><input placeholder='partyAccountId' onChange={e=>setF({...f,partyAccountId:Number(e.target.value)})}/><input placeholder='moneyAccountId' onChange={e=>setF({...f,moneyAccountId:Number(e.target.value)})}/><input placeholder='amount' onChange={e=>setF({...f,amount:Number(e.target.value)})}/><input placeholder='exchangeRate(optional)' onChange={e=>setF({...f,exchangeRate:Number(e.target.value)})}/><input placeholder='targetMoneyAccountId(optional)' onChange={e=>setF({...f,targetMoneyAccountId:Number(e.target.value)})}/><button onClick={async()=>{await fetch('/api/transactions/payment',{method:'POST',body:JSON.stringify(f)});load();}}>Record</button><pre>{JSON.stringify(rows,null,2)}</pre></main>;
}
