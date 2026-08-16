import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts"

function convertData(data, yAxis) {
  if (!Array.isArray(data)) {
    return []
  }

  return data.map((row) => ({
    ...row,
    ...(yAxis && {
      [yAxis]: Number(row[yAxis]),
    }),
  }))
}

function AnalyticsChart({ chart }) {
  if (!chart) {
    return null
  }

  if (chart.chart_type === "table") {
    return null
  }

  const data = convertData(
    chart.data,
    chart.y_axis
  )

  if (!data.length) {
    return null
  }

  const chartType = chart.chart_type

  return (
    <section className="chart-card">

      <div className="card-header">
        <div>
          <span className="card-label">
            VISUALIZATION
          </span>

          <h3>{chart.title}</h3>
        </div>

        <span className="chart-type">
          {chartType}
        </span>
      </div>

      <div className="chart-container">

        {chartType === "bar" && (
          <BarChart
            width={760}
            height={400}
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 10,
              bottom: 60,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#252525"
            />

            <XAxis
              dataKey={chart.x_axis}
              stroke="#888"
              angle={-25}
              textAnchor="end"
              interval={0}
            />

            <YAxis
              stroke="#888"
            />

            <Tooltip
              contentStyle={{
                background: "#161616",
                border: "1px solid #333",
                borderRadius: "10px",
                color: "#fff",
              }}
            />

            <Bar
              dataKey={chart.y_axis}
              fill="#f59e0b"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        )}

        {chartType === "line" && (
          <LineChart
            width={760}
            height={400}
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 10,
              bottom: 40,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#252525"
            />

            <XAxis
              dataKey={chart.x_axis}
              stroke="#888"
            />

            <YAxis
              stroke="#888"
            />

            <Tooltip
              contentStyle={{
                background: "#161616",
                border: "1px solid #333",
                borderRadius: "10px",
                color: "#fff",
              }}
            />

            <Line
              type="monotone"
              dataKey={chart.y_axis}
              stroke="#f59e0b"
              strokeWidth={3}
              dot={{
                r: 5,
              }}
            />
          </LineChart>
        )}

        {chartType === "pie" && (
          <PieChart
            width={760}
            height={400}
          >
            <Pie
              data={data}
              dataKey={chart.y_axis}
              nameKey={chart.x_axis}
              cx="50%"
              cy="50%"
              outerRadius={140}
              label
            >
              {data.map((_, index) => (
                <Cell
                  key={index}
                  fill={
                    [
                      "#f59e0b",
                      "#fbbf24",
                      "#d97706",
                      "#92400e",
                      "#78350f",
                    ][index % 5]
                  }
                />
              ))}
            </Pie>

            <Tooltip
              contentStyle={{
                background: "#161616",
                border: "1px solid #333",
                borderRadius: "10px",
                color: "#fff",
              }}
            />

            <Legend />
          </PieChart>
        )}

      </div>

    </section>
  )
}

export default AnalyticsChart