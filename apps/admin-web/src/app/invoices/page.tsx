import { API_BASE, getInvoices } from "../../lib/api";

export default async function Page() {
  let invoices: Array<Record<string, unknown>> = [];
  try {
    const data = await getInvoices();
    invoices = data.invoices;
  } catch {
    invoices = [];
  }

  return (
    <main className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand__name">Invoices</span>
          <span className="brand__tag">Exports</span>
        </div>
        <nav className="nav">
          <a href="/">Overview</a>
          <a href="/uploads">Uploads</a>
          <a href="/months">Months</a>
          <a href="/payouts">Payouts</a>
          <a href="/audits">Audits</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Generated automatically for each payout run.</h1>
        <p>
          Invoices are created when a run completes. Download the HTML and print
          to PDF if needed.
        </p>
      </section>

      <section className="panel">
        {invoices.length === 0 ? (
          <p className="dropzone__hint">No invoices have been generated yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Month</th>
                <th>Recipient</th>
                <th>Total (USD)</th>
                <th>Download</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((invoice) => {
                const invoiceId = String(invoice.invoice_id || "");
                const downloadPath =
                  typeof invoice.download_url === "string"
                    ? `${API_BASE}${invoice.download_url}`
                    : `${API_BASE}/invoices/${invoiceId}/download`;
                const recipientType = String(invoice.recipient_type || "");
                const recipientId = String(invoice.recipient_id || "");
                return (
                  <tr key={invoiceId}>
                    <td>{String(invoice.invoice_number || invoiceId)}</td>
                    <td>{String(invoice.month || "")}</td>
                    <td>
                      {recipientType} {recipientId}
                    </td>
                    <td>{String(invoice.total_usd || "0.00")}</td>
                    <td>
                      <a href={downloadPath}>Download</a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
