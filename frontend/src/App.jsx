import { useMemo, useState, useEffect } from "react"
import QueryInput from "./components/QueryInput"
import ExecutiveSummary from "./components/ExecutiveSummary"
import AnalyticsChart from "./components/AnalyticsChart"
import ResultTable from "./components/ResultTable"
import "./App.css"

const API_URL = "/analytics/query"
const HEALTH_URL = "/health"

const suggestedQuestions = [
  "Show total sales by product",
  "Which products generate the most revenue?",
  "Show monthly sales trends",
  "Which customers have placed the most orders?",
  "Compare sales across cities",
]

const navItems = [
  { label: "Overview", icon: "◌" },
  { label: "Analytics", icon: "◍" },
  { label: "Query History", icon: "◔" },
  { label: "Saved Insights", icon: "◕" },
  { label: "Settings", icon: "⚙" },
]

function formatCompactNumber(value) {
  if (!Number.isFinite(value)) return "—"

  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 2,
  }).format(value)
}

function getMetricCards(result) {
  if (!result || !Array.isArray(result.result) || result.result.length === 0) {
    return []
  }

  const rows = result.result
  const chart = result.chart || {}
  const chartY = chart.y_axis
  const numericKeys = Object.keys(rows[0] || {}).filter((key) =>
    rows.some((row) => typeof row?.[key] === "number")
  )

  const metricKey =
    chartY && numericKeys.includes(chartY)
      ? chartY
      : numericKeys.find((key) => key.toLowerCase().includes("sales") || key.toLowerCase().includes("revenue") || key.toLowerCase().includes("total") || key.toLowerCase().includes("amount")) || numericKeys[0]

  if (!metricKey) {
    return []
  }

  const values = rows
    .map((row) => Number(row?.[metricKey]))
    .filter((value) => Number.isFinite(value))

  if (!values.length) {
    return []
  }

  const total = values.reduce((sum, value) => sum + value, 0)
  const average = total / values.length
  const highest = Math.max(...values)

  const cards = [
    { label: "Total", value: formatCompactNumber(total), meta: "All records" },
    { label: "Average", value: formatCompactNumber(average), meta: "Per item" },
    { label: "Items", value: String(rows.length), meta: "Rows returned" },
    { label: "Highest", value: formatCompactNumber(highest), meta: "Peak value" },
  ]

  return cards.slice(0, 4)
}

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showRawData, setShowRawData] = useState(false)
  const [activeSection, setActiveSection] = useState("Analytics")
  const [queryHistory, setQueryHistory] = useState([])

  const metricCards = useMemo(() => getMetricCards(result), [result])

  // Check backend health on mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await fetch(HEALTH_URL, { method: "GET" })
        setBackendOnline(response.ok)
      } catch (err) {
        setBackendOnline(false)
      }
    }
    checkBackendHealth()
  }, [])

  const sectionMeta = {
    Overview: {
      eyebrow: "Overview",
      title: "Overview",
      subtitle: "A quick summary of your analytics workspace and recent business health.",
    },
    Analytics: {
      eyebrow: "Analytics",
      title: "Analytics",
      subtitle: "Ask questions about your business data in natural language.",
    },
    "Query History": {
      eyebrow: "Query History",
      title: "Query History",
      subtitle: "Review recent questions and the analysis results you have already explored.",
    },
    "Saved Insights": {
      eyebrow: "Saved Insights",
      title: "Saved Insights",
      subtitle: "Keep your most valuable findings close at hand and revisit them quickly.",
    },
    Settings: {
      eyebrow: "Settings",
      title: "Settings",
      subtitle: "Tune the analytics workspace, model behavior, and dashboard preferences.",
    },
  }

  const [backendOnline, setBackendOnline] = useState(true)

  const queryList = queryHistory

  const savedInsightCards = result?.summary?.key_insights?.length
    ? result.summary.key_insights.map((insight, index) => ({
        title: `Insight ${index + 1}`,
        body: insight,
        category: index % 2 === 0 ? "Revenue" : "Behavior",
      }))
    : []

  const settingsCards = [
    { title: "Analytics Engine", detail: "Natural Language SQL Agent", status: "Active" },
    { title: "Database Connection", detail: "Configured via environment variables", status: "Connected" },
  ]

  const analyzeQuestion = async (question) => {
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setShowRawData(false)
    setActiveSection("Analytics")

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data?.message || data?.detail || "Something went wrong while processing your request."
        )
      }

      setResult(data)
      setQueryHistory((current) => {
        const nextEntry = question.trim()

        if (current[0] === nextEntry) {
          return current
        }

        return [nextEntry, ...current].slice(0, 6)
      })
    } catch (err) {
      setResult(null)
      setError(err.message || "Unable to connect to the analytics API.")
    } finally {
      setLoading(false)
    }
  }

  const renderContent = () => {
    if (activeSection === "Overview") {
      return (
        <section className="results-panel">
          <div className="results-header">
            <div>
              <span className="panel-label">Overview</span>
              <h2>Dashboard Overview</h2>
            </div>
          </div>

          <div className="empty-state-panel">
            <div className="empty-illustration">📊</div>
            <h3>No data available yet</h3>
            <p>Run an analysis in the Analytics section to see your data here.</p>
          </div>
        </section>
      )
    }

    if (activeSection === "Query History") {
      return (
        <section className="results-panel">
          <div className="results-header">
            <div>
              <span className="panel-label">Query History</span>
              <h2>Recent queries</h2>
            </div>
            {queryList.length > 0 && (
              <div className="result-meta">
                <span>{queryList.length} saved queries</span>
              </div>
            )}
          </div>

          {queryList.length > 0 ? (
            <div className="history-list">
              {queryList.map((entry, index) => (
                <button
                  key={`${entry}-${index}`}
                  type="button"
                  className="history-item"
                  onClick={() => analyzeQuestion(entry)}
                >
                  <span className="history-order">#{index + 1}</span>
                  <div className="history-text">
                    <strong>{entry}</strong>
                  </div>
                  <span className="history-status success">Done</span>
                </button>
              ))}
            </div>
          ) : (
            <div className="empty-state-panel">
              <div className="empty-illustration">📝</div>
              <h3>No analyses yet</h3>
              <p>Your completed analyses will appear here.</p>
            </div>
          )}
        </section>
      )
    }

    if (activeSection === "Saved Insights") {
      return (
        <section className="results-panel">
          <div className="results-header">
            <div>
              <span className="panel-label">Saved Insights</span>
              <h2>Key findings</h2>
            </div>
            {savedInsightCards.length > 0 && (
              <div className="result-meta">
                <span>{savedInsightCards.length} insights</span>
              </div>
            )}
          </div>

          {savedInsightCards.length > 0 ? (
            <div className="insight-grid">
              {savedInsightCards.map((insight) => (
                <article key={insight.title} className="info-card insight-card">
                  <div className="card-header">
                    <h3>{insight.title}</h3>
                    <span className="insight-tag">{insight.category}</span>
                  </div>
                  <p>{insight.body}</p>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state-panel">
              <div className="empty-illustration">💡</div>
              <h3>No saved insights yet</h3>
              <p>Save important findings from your analyses to access them here.</p>
            </div>
          )}
        </section>
      )
    }

    if (activeSection === "Settings") {
      return (
        <section className="results-panel">
          <div className="results-header">
            <div>
              <span className="panel-label">Settings</span>
              <h2>Workspace preferences</h2>
            </div>
          </div>

          <div className="settings-grid">
            {settingsCards.map((setting) => (
              <div key={setting.title} className="info-card settings-card">
                <div className="card-header">
                  <h3>{setting.title}</h3>
                  <span className="status-pill small-status">{setting.status}</span>
                </div>
                <p>{setting.detail}</p>
              </div>
            ))}
          </div>

          <div className="info-card toggle-card">
            <div className="card-header">
              <h3>About this Application</h3>
            </div>
            <p><strong>InsightAI</strong> is a natural language analytics agent that transforms business questions into SQL queries, executes them against your database, and generates insights with visualizations.</p>
            <p style={{ marginTop: "12px", fontSize: "0.85rem", color: "var(--text-soft)" }}>For configuration details or support, please check the application documentation.</p>
          </div>
        </section>
      )
    }

    return (
      <>
        <section className="query-panel">
          <div className="panel-header">
            <div>
              <span className="panel-label">Ask your data</span>
              <h2>Ask your data</h2>
            </div>
            <span className="mini-badge">AI-powered</span>
          </div>

          <p className="panel-description">
            Ask a business question and let the AI analyst find the answer.
          </p>

          <QueryInput onSubmit={analyzeQuestion} loading={loading} suggestions={suggestedQuestions} />
        </section>

        {!result && !loading && !error && (
          <section className="empty-state-panel">
            <div className="empty-illustration">✦</div>
            <h3>Ask your data anything.</h3>
            <p>Get business insights using natural language instead of writing SQL.</p>
            <div className="empty-suggestions">
              {suggestedQuestions.map((suggestion) => (
                <button key={suggestion} type="button" className="suggestion-pill" onClick={() => analyzeQuestion(suggestion)}>
                  {suggestion}
                </button>
              ))}
            </div>
          </section>
        )}

        {error && (
          <section className="error-card">
            <div className="error-icon">!</div>
            <div className="error-copy">
              <h3>Unable to analyze this question</h3>
              <p>Please check your question and try again.</p>
              <button type="button" className="primary-button" onClick={() => result && analyzeQuestion(result.question)}>
                Try again
              </button>
            </div>
          </section>
        )}

        {loading && (
          <section className="loading-card">
            <div className="loading-spinner" />
            <div className="loading-copy">
              <h3>Analyzing your data...</h3>
              <p>Understanding question • Analyzing database • Generating insights • Preparing visualization</p>
              <div className="loading-steps" aria-label="Analysis steps">
                <span className="loading-step active">Understanding question</span>
                <span className="loading-step">Analyzing database</span>
                <span className="loading-step">Generating insights</span>
                <span className="loading-step">Preparing visualization</span>
              </div>
            </div>
          </section>
        )}

        {result && !loading && (
          <section className="results-panel">
            <div className="results-header">
              <div>
                <span className="panel-label">Analysis Results</span>
                <h2>{result.question}</h2>
              </div>
              <div className="result-meta">
                <span>Generated just now</span>
                {Array.isArray(result.result) && (
                  <span>{result.result.length} rows analyzed</span>
                )}
              </div>
            </div>

            {metricCards.length > 0 && (
              <div className="metrics-grid">
                {metricCards.map((card) => (
                  <div key={card.label} className="metric-card">
                    <div className="metric-label">{card.label}</div>
                    <div className="metric-value">{card.value}</div>
                    <div className="metric-meta">{card.meta}</div>
                  </div>
                ))}
              </div>
            )}

            <ExecutiveSummary summary={result.summary} />

            <AnalyticsChart chart={result.chart} />

            <div className="table-panel">
              <div className="table-panel-header">
                <div>
                  <span className="panel-label">Query Result</span>
                  <h3>Query Result</h3>
                </div>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setShowRawData((current) => !current)}
                >
                  {showRawData ? "Hide raw data" : "View raw data"}
                </button>
              </div>

              <ResultTable data={result.result} compact={!showRawData} />

              {showRawData && Array.isArray(result.result) && (
                <pre className="raw-data-panel">{JSON.stringify(result.result, null, 2)}</pre>
              )}
            </div>
          </section>
        )}
      </>
    )
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-mark">I</div>
          <div>
            <div className="sidebar-name">InsightAI</div>
            <div className="sidebar-subtitle">Natural Language Analytics</div>
          </div>
        </div>

        <nav className="sidebar-nav" aria-label="Sidebar navigation">
          {navItems.map((item) => (
            <button
              key={item.label}
              className={`nav-item ${activeSection === item.label ? "active" : ""}`}
              type="button"
              onClick={() => setActiveSection(item.label)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="agent-status">
          <div className="status-pill">
            <span className="status-dot" />
            Online
          </div>
          <div className="agent-label">AI Analytics Agent</div>
        </div>
      </aside>

      <div className="main-panel">
        <header className="top-header">
          <div>
            <p className="eyebrow">{sectionMeta[activeSection]?.eyebrow || "Analytics"}</p>
            <h1>{sectionMeta[activeSection]?.title || "Analytics"}</h1>
            <p className="subtitle">{sectionMeta[activeSection]?.subtitle || "Ask questions about your business data in natural language."}</p>
          </div>

          <div className="header-actions">
            <div className="api-status">
              <span className="status-dot" style={{ backgroundColor: backendOnline ? "#10B981" : "#EF4444" }} />
              {backendOnline ? "Backend online" : "Backend offline"}
            </div>
            <button type="button" className="icon-button" aria-label="Open settings">⚙</button>
          </div>
        </header>

        <main className="content">{renderContent()}</main>
      </div>
    </div>
  )
}

export default App