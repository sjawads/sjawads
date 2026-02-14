'use client';
import { useEffect, useState } from 'react';
export default function ProductsPage() { const [rows,setRows]=useState<any[]>([]); const [name,setName]=useState(''); const load=async()=>setRows(await (await fetch('/api/products')).json()); useEffect(()=>{load();},[]); return <main><h2>Products</h2><input onChange={e=>setName(e.target.value)} /><button onClick={async()=>{await fetch('/api/products',{method:'POST',body:JSON.stringify({name})});load();}}>Create</button><pre>{JSON.stringify(rows,null,2)}</pre></main>; }
