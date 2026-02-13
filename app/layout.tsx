export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body style={{ fontFamily: 'sans-serif', padding: 20 }}><nav style={{ display: 'flex', gap: 12 }}><a href="/accounts">Accounts</a><a href="/products">Products</a><a href="/ports">Ports</a><a href="/contracts">Contracts</a><a href="/transactions">Transactions</a><a href="/in-kind">In-Kind</a></nav><hr />{children}</body></html>;
}
