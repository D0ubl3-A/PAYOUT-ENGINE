export function TablePreview() {
  const rows = [
    { host: "H-102", beans: "12,500", eligible: "Yes", status: "Matched" },
    { host: "H-231", beans: "8,100", eligible: "Yes", status: "Matched" },
    { host: "H-515", beans: "4,200", eligible: "No", status: "Review" },
  ];

  return (
    <section className="panel">
      <h3 className="dropzone__title">Extraction preview</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Host</th>
            <th>Beans</th>
            <th>Eligible</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.host}>
              <td>{row.host}</td>
              <td>{row.beans}</td>
              <td>{row.eligible}</td>
              <td>{row.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
