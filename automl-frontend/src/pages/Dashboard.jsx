import { useEffect, useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Dashboard.css";
import api from "../api/api.js";
import ModelComparisonChart from "../components/ModelComparisonChart";
import DatasetQualityChart from "../components/DatasetQualityChart";

import {
  FaDatabase,
  FaTable,
  FaLayerGroup,
  FaRobot,
  FaBullseye,
  FaCheckCircle,
} from "react-icons/fa";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [modelResults, setModelResults] = useState({});
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    loadDashboard();
}, []);

const loadDashboard = async () => {

    let dashboardData = null;

    try {

      const res = await api.get("/dashboard");
      dashboardData = res.data;
      setDashboard(res.data);

    } catch (err) {

      setDashboard(null);

    }

    const modelIsTrained = !!(
      dashboardData &&
      dashboardData.model &&
      dashboardData.model.name
    );

    if (modelIsTrained) {

      try {

        const result = await api.get("/model-results");
        setModelResults(result.data);

      } catch {

        setModelResults([]);

      }

      try {

        const analysisRes = await api.get("/dataset-analysis");
        setAnalysis(analysisRes.data);

      } catch {

        setAnalysis(null);

      }

    } else {

      setModelResults([]);
      setAnalysis(null);

    }

    setLoading(false);

  };


  if (loading) {
    return (
      <Layout>
        <h2>Loading Dashboard...</h2>
      </Layout>
    );
  }

  const isModelTrained = !!(dashboard && dashboard.model && dashboard.model.name);

    if (!dashboard) {
    return (
      <Layout></Layout>
    );
  }

  if (!dashboard || !isModelTrained) {
  return (
    <Layout>
      <div className="dashboard">

        <h1 className="dashboard-title">
          🚀 AutoML Dashboard
        </h1>

        <p className="dashboard-subtitle">
          Monitor datasets, model performance, training status and analytics from one place.
        </p>

        <div className="no-model-card">
          <div className="no-model-icon">⚠️</div>
          <h2>No Trained Model Found</h2>
          <p>Please upload a dataset and train a model to view your dashboard analytics.</p>
        </div>

      </div>
    </Layout>
  );
}
  const dashboardData = [
    {
      title: "Dataset Rows",
      value: dashboard?.dataset?.rows,
      icon: <FaDatabase />,
      className: "",
    },
    {
      title: "Dataset Columns",
      value: dashboard?.dataset?.columns,
      icon: <FaTable />,
      className: "",
    },
    {
      title: "Problem Type",
      value:
        dashboard?.model?.problem_type?.charAt(0).toUpperCase() +
        dashboard?.model?.problem_type?.slice(1),
      icon: <FaLayerGroup />,
      className: "",
    },
    {
      title: "Best Model",
      value: dashboard?.model?.name,
      icon: <FaRobot />,
      className: "small-text",
    },
    {
      title: "Accuracy",
      value:
        dashboard?.model?.score != null
          ? `${(dashboard.model.score * 100).toFixed(2)}%`
          : "—",
      icon: <FaBullseye />,
      className: "",
    },
    {
      title: "Status",
      value: isModelTrained ? "Trained" : "Not Trained",
      subtext: dashboard?.model?.trained_at
        ? new Date(dashboard.model.trained_at).toLocaleString()
        : null,
      icon: <FaCheckCircle />,
      className: isModelTrained ? "status-trained" : "status-pending",
    },
  ];

  return (
    <Layout>
      <div className="dashboard">
        <h1 className="dashboard-title">🚀 AutoML Dashboard</h1>
        <p className="dashboard-subtitle">
          Monitor datasets, model performance, training status and analytics from one place.
        </p>

        <div className="dashboard-summary">

          <div className="summary-left">

            <h2>Model Overview</h2>

            <p>
              Your latest machine learning model has been successfully trained and is
              ready for prediction.
            </p>

          </div>

          <div className="summary-right">

            <span className="status-badge">
              ✅ Ready
            </span>

          </div>

        </div>

                <div className="card-container">
                {dashboardData.map((item, index) => (
                  <div className="dashboard-card" key={index}>
                    <div
                      className={
                        item.title === "Status"
                          ? "card-icon status-icon"
                          : "card-icon"
                      }
                    >
                      {item.icon}
                    </div>

                    <div className="card-title">{item.title}</div>

                    <div className={`card-value ${item.className}`}>
                      {item.value}
                    </div>

                    {item.subtext && (
                      <div className="card-subtext">{item.subtext}</div>
                    )}
                  </div>
                ))}
              </div>  

              <div className="charts-grid">

                  <ModelComparisonChart
                      data={modelResults}
                  />

                  <DatasetQualityChart
                      analysis={analysis}
                  />

              </div>

            </div>   {/* <-- This closes <div className="dashboard"> */}

          </Layout>
        );
      }

      export default Dashboard;