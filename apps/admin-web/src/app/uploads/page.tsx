import { TablePreview } from "../../components/TablePreview";
import { UploadDropzone } from "../../components/UploadDropzone";
import { getUploads } from "../../lib/api";

export default async function Page() {
  let uploads: Array<Record<string, unknown>> = [];
  try {
    const data = await getUploads();
    uploads = data.uploads;
  } catch {
    uploads = [];
  }

  return (
    <main className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand__name">Uploads</span>
          <span className="brand__tag">Intake</span>
        </div>
        <nav className="nav">
          <a href="/">Overview</a>
          <a href="/months">Months</a>
          <a href="/payouts">Payouts</a>
          <a href="/audits">Audits</a>
          <a href="/invoices">Invoices</a>
        </nav>
      </header>

      <section className="hero">
        <h1>Capture evidence, lock the inputs.</h1>
        <p>
          Every upload is hashed and linked to its extraction so numbers can be
          traced to the original screenshot.
        </p>
      </section>

      <section className="split">
        <UploadDropzone />
        <div className="panel">
          <h3 className="dropzone__title">Recent uploads</h3>
          {uploads.length === 0 ? (
            <p className="dropzone__hint">No uploads found yet.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Upload</th>
                  <th>Type</th>
                  <th>Size</th>
                </tr>
              </thead>
              <tbody>
                {uploads.slice(0, 6).map((upload) => (
                  <tr key={String(upload.upload_id)}>
                    <td>{String(upload.filename)}</td>
                    <td>{String(upload.content_type)}</td>
                    <td>{String(upload.size_bytes)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>

      <TablePreview />
    </main>
  );
}
