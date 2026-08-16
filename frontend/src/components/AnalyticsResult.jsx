import AnalyticsChart from "./AnalyticsChart"

function AnalyticsResult({ result }) {
  return (
    <section>
      <h2>Executive Summary</h2>

      <p>{result.summary.summary}</p>

      <h3>Key Insights</h3>

      <ul>
        {result.summary.key_insights.map((insight, index) => (
          <li key={index}>{insight}</li>
        ))}
      </ul>

      <AnalyticsChart chart={result.chart} />

      <h3>Query Result</h3>

      <table>
        <thead>
          <tr>
            {Object.keys(result.result[0]).map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {result.result.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {Object.values(row).map((value, columnIndex) => (
                <td key={columnIndex}>{String(value)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}

export default AnalyticsResult