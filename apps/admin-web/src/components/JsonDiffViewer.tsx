export function JsonDiffViewer() {
  const rows = [
    { label: "host_bonus_pool_usd", left: "600.00", right: "600.00", warn: false },
    { label: "H-515.beans", left: "4,200", right: "4,280", warn: true },
    { label: "recruiter_pool_usd", left: "350.00", right: "350.00", warn: false },
    { label: "H-102.tier", left: "T2", right: "T2", warn: false },
  ];

  return (
    <section className="panel diff">
      <div>
        <div className="diff__label">Maverick</div>
        {rows.map((row) => (
          <div
            className={`diff__line${row.warn ? " warn" : ""}`}
            key={`left-${row.label}`}
          >
            <span>{row.label}</span>
            <span>{row.left}</span>
          </div>
        ))}
      </div>
      <div>
        <div className="diff__label">Scout</div>
        {rows.map((row) => (
          <div
            className={`diff__line${row.warn ? " warn" : ""}`}
            key={`right-${row.label}`}
          >
            <span>{row.label}</span>
            <span>{row.right}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
