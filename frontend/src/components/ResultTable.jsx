function formatValue(value) {
  if (value === null || value === undefined) {
    return "—"
  }

  if (typeof value === "string") {
    return value
  }

  if (typeof value === "object") {
    return JSON.stringify(value)
  }

  return String(value)
}

function ResultTable({ data }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <section className="table-card">
        <div className="card-header">
          <div>
            <span className="card-label">
              QUERY RESULT
            </span>

            <h3>No records found</h3>
          </div>
        </div>

        <div className="empty-state">
          The query returned no data.
        </div>
      </section>
    )
  }

  const columns = Object.keys(data[0])

  return (
    <section className="table-card">

      <div className="card-header">
        <div>
          <span className="card-label">
            QUERY RESULT
          </span>

          <h3>Data returned by the query</h3>
        </div>

        <span className="row-count">
          {data.length} {data.length === 1 ? "row" : "rows"}
        </span>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>
                  {column.replaceAll("_", " ")}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((column) => (
                  <td key={column}>
                    {formatValue(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </section>
  )
}

export default ResultTable