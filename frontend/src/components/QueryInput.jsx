import { useState } from "react"

function QueryInput({ onSubmit, loading, suggestions = [] }) {
  const [question, setQuestion] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!question.trim() || loading) {
      return
    }

    onSubmit(question)
  }

  return (
    <form className="query-form" onSubmit={handleSubmit}>
      <div className="query-input-wrapper">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="e.g. Show total sales by product"
          disabled={loading}
          rows={4}
          aria-label="Ask your data"
        />

        <button type="submit" disabled={!question.trim() || loading}>
          {loading ? "Analyzing your data..." : "Analyze"}
        </button>
      </div>

      {suggestions.length > 0 && (
        <div className="suggestion-list" aria-label="Suggested questions">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              className="suggestion-pill"
              onClick={() => !loading && setQuestion(suggestion)}
              disabled={loading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </form>
  )
}

export default QueryInput