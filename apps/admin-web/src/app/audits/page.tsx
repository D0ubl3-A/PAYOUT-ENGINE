import { AuditExplorer } from "../../components/AuditExplorer";
import { JsonDiffViewer } from "../../components/JsonDiffViewer";
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
          <span className="brand__name">Audit Explorer</span>
          <span className="brand__tag">Trace</span>
        </div>
        <nav className="nav">
          <a href="/">Overview</a>
          <a href="/uploads">Uploads</a>
          <a href="/months">Months</a>
          <a href="/payouts">Payouts</a>
          <a href="/invoices">Invoices</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Every number, explainable.</h1>
        <p>
          Compare model reads, inspect formulas, and export the full audit JSON
          for dispute resolution.
        </p>
      </section>

      <section className="split">
        <AuditExplorer />
        <JsonDiffViewer />
      </section>

      <section className="panel">
        <h3 className="dropzone__title">Recent audit runs</h3>
        {runs.length === 0 ? (
          <p className="dropzone__hint">No audit data available yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Run ID</th>
                <th>Month</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => (
                <tr key={String(run.run_id)}>
                  <td>{String(run.run_id).slice(0, 8)}</td>
                  <td>{String(run.month)}</td>
                  <td>{String(run.status)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
