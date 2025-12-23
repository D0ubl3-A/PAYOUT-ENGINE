import { getRuns } from "../../lib/api";

export default async function Page() {
  let runs: Array<Record<string, unknown>> = [];
  try {
    const data = await getRuns();
    runs = data.runs;
  } catch {
    runs = [];
  }

  return (
    <main className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand__name">Monthly Runs</span>
          <span className="brand__tag">History</span>
        </div>
        <nav className="nav">
          <a href="/">Overview</a>
          <a href="/uploads">Uploads</a>
          <a href="/payouts">Payouts</a>
          <a href="/audits">Audits</a>
          <a href="/invoices">Invoices</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Track every month with immutable inputs.</h1>
        <p>
          Each run links the screenshot hash, validation result, and payout
          totals for dispute-proof reporting.
        </p>
      </section>

      <section className="panel">
        {runs.length === 0 ? (
          <p className="dropzone__hint">No payout runs yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Month</th>
                <th>Status</th>
                <th>Run ID</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((row) => (
                <tr key={String(row.run_id)}>
                  <td>{String(row.month)}</td>
                  <td>{String(row.status)}</td>
                  <td>{String(row.run_id).slice(0, 8)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
