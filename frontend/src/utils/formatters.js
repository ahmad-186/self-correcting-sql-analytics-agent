export function formatColumnName(column) {
  return String(column)
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function formatValue(value, columnName = "") {
  if (value === null || value === undefined) return "—"
  if (typeof value === "object") return JSON.stringify(value)
  if (typeof value === "number") {
    const currency = /amount|price|sales|revenue|cost|profit|total/.test(String(columnName).toLowerCase())
    return new Intl.NumberFormat("en-US", currency
      ? { style: "currency", currency: "USD", maximumFractionDigits: 2 }
      : { maximumFractionDigits: 2 }).format(value)
  }
  return String(value)
}

const escapeCsvCell = (value) => {
  const cell = value == null ? "" : typeof value === "object" ? JSON.stringify(value) : String(value)
  return /[",\n\r]/.test(cell) ? `"${cell.replaceAll('"', '""')}"` : cell
}

export function downloadCsv(rows, filename = "analysis-result.csv") {
  if (!Array.isArray(rows) || rows.length === 0) return
  const columns = Array.from(new Set(rows.flatMap((row) => Object.keys(row || {}))))
  const csv = [columns.map(escapeCsvCell).join(","), ...rows.map((row) => columns.map((key) => escapeCsvCell(row?.[key])).join(","))].join("\r\n")
  const url = URL.createObjectURL(new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8" }))
  const link = document.createElement("a")
  link.href = url
  link.download = filename
  document.body.append(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
