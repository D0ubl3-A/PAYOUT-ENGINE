import { GenerateInvoicesButton } from "../../components/GenerateInvoicesButton";
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
          <span className="brand__name">Payout Results</span>
          <span className="brand__tag">Preview</span>
        </div>
        <nav className="nav">
          <a href="/">Overview</a>
          <a href="/uploads">Uploads</a>
          <a href="/months">Months</a>
          <a href="/audits">Audits</a>
          <a href="/invoices">Invoices</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Deterministic outputs with zero guessing.</h1>
        <p>
          Every payout row is computed from validated inputs and reconciled to
          its pool totals before export.
        </p>
      </section>

      <section className="panel">
        {runs.length === 0 ? (
          <p className="dropzone__hint">No payout runs have been completed.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Run</th>
                <th>Status</th>
                <th>Host rows</th>
                <th>Recruiter rows</th>
                <th>Invoices</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => {
                const outputs = (run.outputs_json as Record<string, unknown>) || {};
                const hosts = Array.isArray(outputs.host_payouts)
                  ? outputs.host_payouts.length
                  : 0;
                const recruiters = Array.isArray(outputs.recruiter_payouts)
                  ? outputs.recruiter_payouts.length
                  : 0;
                const runId = String(run.run_id || "");
                return (
                  <tr key={runId}>
                    <td>{String(run.month)}</td>
                    <td>{String(run.status)}</td>
                    <td>{hosts}</td>
                    <td>{recruiters}</td>
                    <td>
                      <GenerateInvoicesButton runId={runId} />
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
