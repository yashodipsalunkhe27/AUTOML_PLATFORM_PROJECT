import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

function DatasetQualityChart({ analysis }) {

  if (!analysis) return null;

  const totalMissing = Object.values(analysis.missing_values).reduce(
    (a, b) => a + b,
    0
  );

  const hasIssues =
    totalMissing > 0 ||
    analysis.duplicate_rows > 0 ||
    analysis.constant_columns.length > 0;

  const data = [
    {
      name: "Missing Values",
      value: totalMissing,
    },
    {
      name: "Duplicate Rows",
      value: analysis.duplicate_rows,
    },
    {
      name: "Constant Columns",
      value: analysis.constant_columns.length,
    },
  ];

  const colors = [
    "#ef4444",
    "#3b82f6",
    "#10b981",
  ];

  return (
    <div className="chart-card">

      <h2 className="chart-title">
        📊 Dataset Quality
      </h2>

      {!hasIssues ? (

        <div
          style={{
            textAlign: "center",
            padding: "60px 20px",
            color: "#16a34a",
            fontSize: "18px",
            fontWeight: "600",
          }}
        >
          ✅ No data quality issues detected — dataset is clean!
        </div>

      ) : (

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="name" />

          <YAxis />

          <Tooltip />

          <Bar dataKey="value" radius={[8,8,0,0]}>
            {data.map((entry,index)=>(
              <Cell
                key={index}
                fill={colors[index]}
              />
            ))}
          </Bar>

        </BarChart>
      </ResponsiveContainer>

      )}

    </div>
  );
}

export default DatasetQualityChart;