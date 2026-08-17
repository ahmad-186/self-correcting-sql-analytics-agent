function ExecutiveSummary({ summary }) {
  if (!summary) {
    return null
  }

  const summaryText =
    typeof summary === "string"
      ? summary
      : summary.summary

  const insights =
    typeof summary === "object" &&
    Array.isArray(summary.key_insights)
      ? summary.key_insights
      : []

  return (
    <section className="summary-grid">
      <div className="summary-card">
        <div className="card-header">
          <div>
            <span className="card-label">Executive Summary</span>
            <h3>What the data says</h3>
          </div>

          <div className="card-icon">AI</div>
        </div>

        <div className="summary-badge">AI generated</div>
        <p className="summary-text">{summaryText}</p>
      </div>

      {insights.length > 0 && (
        <div className="summary-card">
          <div className="card-header">
            <div>
              <span className="card-label">Key Insights</span>
              <h3>Important findings</h3>
            </div>

            <div className="card-icon">✓</div>
          </div>

          <ul className="insights">
            {insights.map((insight, index) => (
              <li key={index}>
                <span className="insight-icon">✓</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}

export default ExecutiveSummary