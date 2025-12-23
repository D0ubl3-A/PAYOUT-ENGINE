export function AuditExplorer() {
  const rows = [
    { label: "host_bonus_pool_usd", value: "600.00", note: "60% of commission" },
    {
      label: "eligible_total_beans",
      value: "20,600",
      note: "sum of eligible host beans",
    },
    {
      label: "recruiter_pool_usd",
      value: "350.00",
      note: "7% of gross agency revenue",
    },
    { label: "sunset_pool_usd", value: "150.00", note: "legacy share" },
  ];

  return (
    <section className="panel audit">
      <h3 className="dropzone__title">Audit trail highlights</h3>
      {rows.map((row) => (
        <div className="audit__row" key={row.label}>
          <strong>{row.label}</strong>
          <span>{row.value}</span>
          <span>{row.note}</span>
        </div>
      ))}
    </section>
  );
}
