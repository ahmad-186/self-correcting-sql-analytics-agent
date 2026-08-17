import { useMemo, useState } from "react"
import { downloadCsv, formatColumnName } from "../utils/formatters"

function formatValue(value) {
  if (value === null || value === undefined) {
    return "—"
  }

  if (typeof value === "number") {
    return new Intl.NumberFormat("en-US", {
      maximumFractionDigits: 2,
    }).format(value)
  }

  if (typeof value === "string") {
    return value
  }

  if (typeof value === "object") {
    return JSON.stringify(value)
  }

  return String(value)
}

function ResultTable({ data, compact = false }) {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" })

  if (!Array.isArray(data) || data.length === 0) {
    return (
      <section className="table-card">
        <div className="empty-state">The query returned no data.</div>
      </section>
    )
  }

  const columns = Object.keys(data[0] || {})

  const sortedRows = useMemo(() => {
    if (!sortConfig.key) return data

    return [...data].sort((a, b) => {
      const aValue = a?.[sortConfig.key]
      const bValue = b?.[sortConfig.key]

      if (aValue == null && bValue == null) return 0
      if (aValue == null) return 1
      if (bValue == null) return -1

      if (typeof aValue === "number" && typeof bValue === "number") {
        return sortConfig.direction === "asc" ? aValue - bValue : bValue - aValue
      }

      const stringA = String(aValue).toLowerCase()
      const stringB = String(bValue).toLowerCase()
      return sortConfig.direction === "asc"
        ? stringA.localeCompare(stringB)
        : stringB.localeCompare(stringA)
    })
  }, [data, sortConfig])

  const handleSort = (column) => {
    setSortConfig((current) => {
      if (current.key === column) {
        return {
          key: column,
          direction: current.direction === "asc" ? "desc" : "asc",
        }
      }

      return { key: column, direction: "asc" }
    })
  }

  const displayRows = compact ? sortedRows.slice(0, 8) : sortedRows

  return (
    <section className="table-card">
      <div className="table-actions-row">
        <span className="row-count">{data.length} {data.length === 1 ? "row" : "rows"}</span>
        <button className="secondary-button" type="button" onClick={() => downloadCsv(data)}>
          Download CSV
        </button>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column} onClick={() => handleSort(column)}>
                  <span>{formatColumnName(column)}</span>
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {displayRows.map((row, rowIndex) => (
              <tr key={`${rowIndex}-${JSON.stringify(row)}`}>
                {columns.map((column) => (
                  <td key={`${column}-${rowIndex}`}>{formatValue(row[column])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {compact && data.length > 8 && (
        <p className="table-preview-note">Showing the first 8 rows. Use the raw data toggle to inspect the full dataset.</p>
      )}
    </section>
  )
}

export default ResultTable
