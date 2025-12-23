export default function Page() {
  const highlights = [
    { label: "Current month", value: "2026-03" },
    { label: "Projected payout", value: "$1,240.00" },
    { label: "Bonus eligibility", value: "Confirmed" },
  ];

  const timeline = [
    { label: "Screenshot verified", value: "Mar 12" },
    { label: "Pools validated", value: "Mar 13" },
    { label: "Payout run", value: "Mar 14" },
  ];

  return (
    <main className="page">
      <section className="hero">
        <span className="chip">Host portal</span>
        <h1>Your payout trail, explained at a glance.</h1>
        <p>
          Every payout you see here links back to the extraction audit trail.
          No edits, no overrides, just verified inputs.
        </p>
        <div className="cta-row">
          <button className="button">Download statement</button>
          <button className="button secondary">View audit</button>
        </div>
      </section>

      <section className="grid">
        {highlights.map((item, index) => (
          <div
            className="card reveal"
            style={{ animationDelay: `${index * 0.08 + 0.1}s` }}
            key={item.label}
          >
            <h3>{item.label}</h3>
            <div className="amount">{item.value}</div>
          </div>
        ))}
      </section>

      <section className="card timeline">
        <h3>Processing timeline</h3>
        {timeline.map((row) => (
          <div className="timeline__row" key={row.label}>
            <span>{row.label}</span>
            <strong>{row.value}</strong>
          </div>
        ))}
      </section>
    </main>
  );
}
