import { useMemo, useState } from "react"
import QueryInput from "./components/QueryInput"
import ExecutiveSummary from "./components/ExecutiveSummary"
import AnalyticsChart from "./components/AnalyticsChart"
import ResultTable from "./components/ResultTable"
import "./App.css"

const API_URL = "http://localhost:8000/analytics/query"

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

  const overviewStats = [
    { label: "Monthly revenue", value: "$82.4K", delta: "+12.6%" },
    { label: "Orders", value: "2,184", delta: "+8.1%" },
    { label: "Avg. order value", value: "$378", delta: "+3.2%" },
    { label: "Conversion rate", value: "4.9%", delta: "+0.7%" },
  ]

  const queryList = queryHistory.length
    ? queryHistory
    : [
        "Show total sales by product",
        "Which customers have placed the most orders?",
        "Compare sales across cities",
      ]

  const savedInsightCards = result?.summary?.key_insights?.length
    ? result.summary.key_insights.map((insight, index) => ({
        title: `Insight ${index + 1}`,
        body: insight,
        category: index % 2 === 0 ? "Revenue" : "Behavior",
      }))
    : [
        {
          title: "Top revenue driver",
          body: "Product A accounted for 38% of revenue and remains the strongest growth contributor.",
          category: "Revenue",
        },
        {
          title: "Customer retention",
          body: "Repeat buyers are purchasing 24% more often than new customers after the last campaign.",
          category: "Behavior",
        },
        {
          title: "Regional opportunity",
          body: "The West region is trending 11% above the national average for conversion efficiency.",
          category: "Market",
        },
      ]

  const settingsCards = [
    { title: "Data source", detail: "PostgreSQL • Production", status: "Connected" },
    { title: "AI model", detail: "GPT-4.1 mini • Reasoning enabled", status: "Optimized" },
    { title: "Dashboard defaults", detail: "Light theme • 4 KPI cards • Auto refresh", status: "Active" },
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
        <section className="results-panel overview-panel">
          <div className="overview-hero">
            <div className="overview-copy">
              <span className="panel-label">Overview</span>
              <h2>Business health at a glance</h2>
              <p>
                Monitor growth, conversion quality, and customer momentum across the business in one dashboard.
              </p>
            </div>

            <div className="overview-actions">
              <button type="button" className="primary-button">Generate report</button>
              <button type="button" className="secondary-button">Export</button>
            </div>
          </div>

          <div className="overview-stat-grid">
            {overviewStats.map((stat) => (
              <div key={stat.label} className="overview-stat-card">
                <div className="overview-stat-label">{stat.label}</div>
                <div className="overview-stat-row">
                  <div className="overview-stat-value">{stat.value}</div>
                  <span className="overview-stat-delta">{stat.delta}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="section-grid two-col">
            <div className="info-card overview-visual-card">
              <div className="card-header">
                <h3>Revenue trend</h3>
                <span className="card-icon">↗</span>
              </div>

              <div className="chart-summary-row">
                <div>
                  <div className="summary-figure">$236.8K</div>
                  <div className="summary-caption">This quarter</div>
                </div>
                <span className="summary-badge positive">+18.4%</span>
              </div>

              <div className="sparkline" aria-label="Revenue trend chart">
                <span className="spark spark-1" />
                <span className="spark spark-2" />
                <span className="spark spark-3" />
                <span className="spark spark-4" />
                <span className="spark spark-5" />
                <span className="spark spark-6" />
              </div>
            </div>

            <div className="info-card">
              <div className="card-header">
                <h3>Key focus areas</h3>
                <span className="card-icon">◎</span>
              </div>

              <div className="focus-list">
                <div className="focus-row">
                  <span>Enterprise sales</span>
                  <strong>78%</strong>
                </div>
                <div className="progress"><span style={{ width: "78%" }} /></div>

                <div className="focus-row">
                  <span>Retention</span>
                  <strong>64%</strong>
                </div>
                <div className="progress"><span style={{ width: "64%" }} /></div>

                <div className="focus-row">
                  <span>Pipeline coverage</span>
                  <strong>91%</strong>
                </div>
                <div className="progress"><span style={{ width: "91%" }} /></div>
              </div>
            </div>
          </div>

          <div className="section-grid three-col">
            <div className="info-card compact-card">
              <div className="card-header">
                <h3>Top channel</h3>
                <span className="card-icon small-icon">◌</span>
              </div>
              <div className="mini-stat">Organic search</div>
              <div className="mini-value">$61.4K</div>
              <div className="mini-caption">+14.3% month over month</div>
            </div>

            <div className="info-card compact-card">
              <div className="card-header">
                <h3>Goal progress</h3>
                <span className="card-icon small-icon">◔</span>
              </div>
              <div className="mini-stat">Q3 target</div>
              <div className="mini-value">82%</div>
              <div className="mini-caption">On track to hit goal</div>
            </div>

            <div className="info-card compact-card">
              <div className="card-header">
                <h3>Customer health</h3>
                <span className="card-icon small-icon">◍</span>
              </div>
              <div className="mini-stat">NPS</div>
              <div className="mini-value">+52</div>
              <div className="mini-caption">Strong satisfaction score</div>
            </div>
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
            <div className="result-meta">
              <span>{queryList.length} saved queries</span>
            </div>
          </div>

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
                  <span>{index === 0 ? "Completed today" : index === 1 ? "Completed yesterday" : "Completed last week"}</span>
                </div>
                <span className="history-status success">Done</span>
              </button>
            ))}
          </div>
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
            <div className="result-meta">
              <span>{savedInsightCards.length} insights</span>
            </div>
          </div>

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
              <h3>Notifications</h3>
              <span className="toggle-badge on">On</span>
            </div>
            <p>Receive summary emails when a report is generated or a threshold is crossed.</p>
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
              <button type="button" className="primary-button" onClick={() => analyzeQuestion(result?.question || "Show total sales by product") }>
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
              <span className="status-dot" />
              Backend online
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