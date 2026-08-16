import { useState } from "react"
import QueryInput from "./components/QueryInput"
import ExecutiveSummary from "./components/ExecutiveSummary"
import AnalyticsChart from "./components/AnalyticsChart"
import ResultTable from "./components/ResultTable"
import "./App.css"

const API_URL = "http://localhost:8000/analytics/query"

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeQuestion = async (question) => {
    if (!question.trim()) return

    setLoading(true)
    setError(null)

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
          data?.message ||
          data?.detail ||
          "Something went wrong while processing your request."
        )
      }

      setResult(data)
    } catch (err) {
      setResult(null)
      setError(err.message || "Unable to connect to the analytics API.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">A</div>

          <div>
            <h1>Analytics AI</h1>
            <span>Natural Language Business Intelligence</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div className="hero-badge">
            AI ANALYTICS ENGINE
          </div>

          <h2>
            Ask your business
            <span> anything.</span>
          </h2>

          <p>
            Query your PostgreSQL data using natural language.
            The analytics agent generates, validates, executes,
            analyzes, and visualizes the answer automatically.
          </p>

          <QueryInput
            onSubmit={analyzeQuestion}
            loading={loading}
          />

          <div className="example-queries">
            <span>Try:</span>

            <button
              onClick={() =>
                analyzeQuestion("Show total sales by product")
              }
            >
              Total sales by product
            </button>

            <button
              onClick={() =>
                analyzeQuestion("Show all customers")
              }
            >
              All customers
            </button>

            <button
              onClick={() =>
                analyzeQuestion("Show monthly sales")
              }
            >
              Monthly sales
            </button>
          </div>
        </section>

        {error && (
          <section className="error-card">
            <div className="error-icon">!</div>

            <div>
              <h3>Unable to process request</h3>
              <p>{error}</p>
            </div>
          </section>
        )}

        {loading && (
          <section className="loading-card">
            <div className="loader"></div>

            <div>
              <h3>Analyzing your data</h3>
              <p>
                Generating SQL, validating the query, executing it,
                and preparing your analysis...
              </p>
            </div>
          </section>
        )}

        {result && !loading && (
          <section className="results">

            <div className="result-header">
              <div>
                <span className="section-label">
                  ANALYSIS RESULT
                </span>

                <h2>
                  {result.question}
                </h2>
              </div>

              <div className="result-badge">
                Query completed
              </div>
            </div>

            <ExecutiveSummary
              summary={result.summary}
            />

            <AnalyticsChart
              chart={result.chart}
            />

            <ResultTable
              data={result.result}
            />

          </section>
        )}
      </main>

      <footer>
        <span>
          Analytics AI
        </span>

        <span>
          Self-Correcting Natural Language SQL Agent
        </span>
      </footer>
    </div>
  )
}

export default App