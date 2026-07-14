import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function ModelComparisonChart({ data }) {

  // API already returns an array
  const chartData = (data || []).map((item) => ({
    model: item.model
      .replace("Support Vector Machine", "SVM")
      .replace("K-Nearest Neighbors", "KNN")
      .replace("Random Forest", "Random Forest")
      .replace("Decision Tree", "Decision Tree")
      .replace("Logistic Regression", "Logistic")
      .replace("Extra Trees Classifier", "Extra Trees")
      .replace("XGBoost Classifier", "XGBoost")
      .replace("CatBoost Classifier", "CatBoost"),

    score: Number((item.score * 100).toFixed(2)),
  }));

  return (
    <div className="chart-card">

      <h2 className="chart-title">
        📊 Model Comparison
      </h2>

      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={chartData}
          margin={{
            top: 20,
            right: 20,
            left: 20,
            bottom: 80,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="model"
            angle={-25}
            textAnchor="end"
            interval={0}
            height={90}
            tick={{
              fontSize: 14,
              fontWeight: 600,
            }}
          />

          <YAxis
            domain={[0, 100]}
            label={{
              value: "Accuracy (%)",
              angle: -90,
              position: "insideLeft",
            }}
          />

          <Tooltip
            formatter={(value) => [`${value}%`, "Accuracy"]}
          />

          <Bar
            dataKey="score"
            fill="#2563eb"
            radius={[8, 8, 0, 0]}
          />

        </BarChart>
      </ResponsiveContainer>

    </div>
  );
}

export default ModelComparisonChart;