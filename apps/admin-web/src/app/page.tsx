import { AuditExplorer } from "../components/AuditExplorer";
import { JsonDiffViewer } from "../components/JsonDiffViewer";
import { TablePreview } from "../components/TablePreview";
import { UploadDropzone } from "../components/UploadDropzone";
import { getExtractions, getRuns, getUploads } from "../lib/api";

export default async function Page() {
  let uploads: Array<Record<string, unknown>> = [];
  let extractions: Array<Record<string, unknown>> = [];
  let runs: Array<Record<string, unknown>> = [];

  try {
    const data = await getUploads();
    uploads = data.uploads;
  } catch {
    uploads = [];
  }

  try {
    const data = await getExtractions();
    extractions = data.extractions;
  } catch {
    extractions = [];
  }

  try {
    const data = await getRuns();
    runs = data.runs;
  } catch {
    runs = [];
  }

  const needsReview = extractions.filter((item) => item.status === "NEEDS_REVIEW").length;
  const approved = extractions.filter((item) => item.status === "COMPLETED").length;
  const lastRun = runs[0]?.month ? String(runs[0].month) : "n/a";
  const stats = [
    { label: "Pending uploads", value: String(uploads.length) },
    { label: "Needs review", value: String(needsReview) },
    { label: "Approved extractions", value: String(approved) },
    { label: "Last payout run", value: lastRun },
  ];

  return (
    <main className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand__name">Payout Console</span>
          <span className="brand__tag">Audit Mode</span>
        </div>
        <nav className="nav">
          <a href="/uploads">Uploads</a>
          <a href="/months">Months</a>
          <a href="/payouts">Payouts</a>
          <a href="/audits">Audits</a>
          <a href="/invoices">Invoices</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Dispute-proof payouts, with every number traced.</h1>
        <p>
          Extract screenshots into locked JSON, validate every pool, then
          compute deterministic payouts with a full audit trail.
        </p>
        <div className="hero__actions">
          <button className="button">Start new extraction</button>
          <button className="button secondary">Review pending items</button>
        </div>
      </section>

      <section className="grid">
        {stats.map((stat, index) => (
          <div
            className="panel stat reveal"
            style={{ animationDelay: `${index * 0.08 + 0.1}s` }}
            key={stat.label}
          >
            <h3>{stat.label}</h3>
            <p>{stat.value}</p>
          </div>
        ))}
      </section>

      <section className="split">
        <UploadDropzone />
        <TablePreview />
      </section>

      <section className="split">
        <AuditExplorer />
        <JsonDiffViewer />
      </section>
    </main>
  );
}
