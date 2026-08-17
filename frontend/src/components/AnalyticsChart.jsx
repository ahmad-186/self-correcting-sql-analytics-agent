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
  ResponsiveContainer,
} from "recharts"

const chartColors = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#6366F1", "#8B5CF6"]

function convertData(data, yAxis) {
  if (!Array.isArray(data)) {
    return []
  }

  return data.map((row) => ({
    ...row,
    ...(yAxis && Number.isFinite(Number(row?.[yAxis])) && { [yAxis]: Number(row[yAxis]) }),
  }))
}

function AnalyticsChart({ chart }) {
  if (!chart || chart.chart_type === "table" || chart.chart_type === "none") {
    return null
  }

  const data = convertData(chart.data, chart.y_axis)

  if (!Array.isArray(data) || !data.length) {
    return null
  }

  const chartType = chart.chart_type

  return (
    <section className="chart-card">
      <div className="card-header chart-header">
        <div>
          <span className="card-label">Visualization</span>
          <h3>{chart.title || "Insight chart"}</h3>
        </div>
        <span className="chart-type-badge">{chartType}</span>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height={360}>
          {chartType === "bar" && (
            <BarChart
              data={data}
              margin={{ top: 16, right: 12, left: 0, bottom: 42 }}
            >
              <CartesianGrid stroke="#E5E7EB" strokeDasharray="4 4" vertical={false} />
              <XAxis
                dataKey={chart.x_axis}
                stroke="#6B7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                angle={-18}
                textAnchor="end"
                interval={0}
                height={70}
              />
              <YAxis stroke="#6B7280" tickLine={false} axisLine={false} fontSize={12} />
              <Tooltip
                formatter={(value) => [new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(Number(value)), chart.y_axis]}
                labelStyle={{ color: "#111827" }}
                contentStyle={{
                  background: "#FFFFFF",
                  border: "1px solid #E5E7EB",
                  borderRadius: "12px",
                  color: "#111827",
                  boxShadow: "0 12px 28px rgba(15, 23, 42, 0.08)",
                }}
              />
              <Bar dataKey={chart.y_axis} fill="#4F46E5" radius={[10, 10, 0, 0]} />
            </BarChart>
          )}

          {chartType === "line" && (
            <LineChart data={data} margin={{ top: 16, right: 12, left: 0, bottom: 32 }}>
              <CartesianGrid stroke="#E5E7EB" strokeDasharray="4 4" vertical={false} />
              <XAxis dataKey={chart.x_axis} stroke="#6B7280" tickLine={false} axisLine={false} fontSize={12} />
              <YAxis stroke="#6B7280" tickLine={false} axisLine={false} fontSize={12} />
              <Tooltip
                formatter={(value) => [new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(Number(value)), chart.y_axis]}
                labelStyle={{ color: "#111827" }}
                contentStyle={{
                  background: "#FFFFFF",
                  border: "1px solid #E5E7EB",
                  borderRadius: "12px",
                  color: "#111827",
                  boxShadow: "0 12px 28px rgba(15, 23, 42, 0.08)",
                }}
              />
              <Line
                type="monotone"
                dataKey={chart.y_axis}
                stroke="#4F46E5"
                strokeWidth={3}
                dot={{ r: 4, fill: "#4F46E5", strokeWidth: 0 }}
                activeDot={{ r: 6, fill: "#4F46E5" }}
              />
            </LineChart>
          )}

          {chartType === "pie" && (
            <PieChart>
              <Tooltip
                formatter={(value, name) => [new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(Number(value)), name]}
                labelStyle={{ color: "#111827" }}
                contentStyle={{
                  background: "#FFFFFF",
                  border: "1px solid #E5E7EB",
                  borderRadius: "12px",
                  color: "#111827",
                  boxShadow: "0 12px 28px rgba(15, 23, 42, 0.08)",
                }}
              />
              <Pie
                data={data}
                dataKey={chart.y_axis}
                nameKey={chart.x_axis}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={110}
                paddingAngle={3}
              >
                {data.map((entry, index) => (
                  <Cell key={`${entry[chart.x_axis] ?? index}`} fill={chartColors[index % chartColors.length]} />
                ))}
              </Pie>
            </PieChart>
          )}
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default AnalyticsChart
