import { useState } from "react"

function QueryInput({ onSubmit, loading }) {
  const [question, setQuestion] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!question.trim() || loading) {
      return
    }

    onSubmit(question)
  }

  return (
    <form
      className="query-form"
      onSubmit={handleSubmit}
    >
      <div className="query-input-wrapper">
        <div className="search-icon">
          ⌕
        </div>

        <input
          type="text"
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask something about your business data..."
          disabled={loading}
        />

        <button
          type="submit"
          disabled={!question.trim() || loading}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>
    </form>
  )
}

export default QueryInput