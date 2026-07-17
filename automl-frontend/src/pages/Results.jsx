import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../layout/Layout";
import "../styles/Results.css";

import {
  FaRobot,
  FaBullseye,
  FaChartLine,
  FaMedal,
  FaCheckCircle,
} from "react-icons/fa";

const Results = () => {
  const [modelInfo, setModelInfo] = useState(null);
  const [modelResults, setModelResults] = useState([]);
  const [classificationReport, setClassificationReport] = useState(null);
  const [featureImportance, setFeatureImportance] = useState(null);
  const [confusionMatrix, setConfusionMatrix] = useState(null);
  const [rocCurve, setRocCurve] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const isClassification =
    classificationReport?.accuracy !== undefined &&
    classificationReport?.accuracy !== null;

  const loadResults = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        modelInfoRes,
        modelResultsRes,
        reportRes,
        featureRes,
        confusionRes,
        rocRes,
      ] = await Promise.all([
        axios.get(`${import.meta.env.VITE_API_URL}/model-info`),
        axios.get(`${import.meta.env.VITE_API_URL}/model-results`),
        axios.get(`${import.meta.env.VITE_API_URL}/classification-report`),
        axios.get(`${import.meta.env.VITE_API_URL}/feature-importance`),
        axios.get(`${import.meta.env.VITE_API_URL}/confusion-matrix-graph`),
        axios.get(`${import.meta.env.VITE_API_URL}/roc-curve-graph`),
      ]);

      setModelInfo(modelInfoRes.data);
      setModelResults(modelResultsRes.data || []);
      setClassificationReport(reportRes.data);
      setFeatureImportance(featureRes.data);
      setConfusionMatrix(confusionRes.data);
      setRocCurve(rocRes.data);

    } catch (err) {
      console.error(err);

      if (
        err.response?.status === 400 ||
        err.response?.status === 404
      ) {
        setError(
          "No trained model found. Please upload a dataset and train a model first."
        );
      } else {
        setError(
          "Unable to load results. Please try again later."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResults();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div style={{ padding: "100px", textAlign: "center" }}>
          <h2>Loading Results...</h2>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div
          style={{
            textAlign: "center",
            padding: "100px",
          }}
        >
          <h2>📊 No Results Available</h2>

          <p
            style={{
              marginTop: "15px",
              color: "#666",
              fontSize: "18px",
            }}
          >
            {error}
          </p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="results">

        <h1 className="results-title">
          📊 Model Results Dashboard
        </h1>

        <p className="results-subtitle">
          Complete performance report of the trained Machine Learning model.
        </p>

        <div className="metrics-grid">

          <div className="metric-card">
            <FaRobot className="metric-icon" />
            <div className="metric-title">Best Model</div>
            <div className="metric-value">{modelInfo?.model_name}</div>
          </div>

          <div className="metric-card">
            <FaBullseye className="metric-icon" />
            <div className="metric-title">
              {isClassification ? "Accuracy" : "R² Score"}
            </div>
            <div className="metric-value">
              {modelInfo?.accuracy ?? modelInfo?.r2_score ?? "—"}
            </div>
          </div>

          <div className="metric-card">
            <FaChartLine className="metric-icon" />
            <div className="metric-title">
              {isClassification ? "F1 Score" : "Best Score"}
            </div>
            <div className="metric-value">
              {modelInfo?.f1_score ?? modelInfo?.best_score ?? "—"}
            </div>
          </div>

          <div className="metric-card">
            <FaCheckCircle className="metric-icon" />
            <div className="metric-title">Status</div>
            <div className="metric-value">
              {modelInfo?.training_status}
            </div>
          </div>

        </div>

        <div className="table-section">

          <div className="table-header">
            <FaMedal className="table-icon" />
            <h2>Model Ranking</h2>
          </div>

          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Model</th>
                <th>Score</th>
              </tr>
            </thead>

            <tbody>
              {modelResults.length > 0 ? (
                modelResults.map((item, index) => (
                  <tr key={index}>
                    <td>{item.rank}</td>
                    <td>{item.model}</td>
                    <td>{item.score}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3">No Results Available</td>
                </tr>
              )}
            </tbody>
          </table>

        </div>
{isClassification ? (

          <div className="metrics-grid">

            <div className="metric-card">
              <div className="metric-title">Accuracy</div>
              <div className="metric-value">
                {classificationReport?.accuracy}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-title">ROC AUC</div>
              <div className="metric-value">
                {classificationReport?.roc_auc}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-title">MCC</div>
              <div className="metric-value">
                {classificationReport?.mcc}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-title">Kappa</div>
              <div className="metric-value">
                {classificationReport?.kappa}
              </div>
            </div>

          </div>

        ) : (

          <div className="not-applicable-banner">
            ℹ️ Accuracy, ROC AUC, MCC, and Kappa are classification-only metrics — not applicable for this regression model.
          </div>

        )}

        <div className="graph-card">

          <div className="graph-header">
            📊 Feature Importance
          </div>

          <div className="graph-body">

            {featureImportance?.message ? (
              <p className="graph-message">
                {featureImportance.message}
              </p>
            ) : (
              <img
                src={featureImportance?.graph_url}
                alt="Feature Importance"
                className="graph-image"
              />
            )}

          </div>

        </div>

        <div className="graph-card">

          <div className="graph-header">
            🧮 Confusion Matrix
          </div>

          <div className="graph-body">

            {confusionMatrix?.graph_url ? (
              <img
                src={confusionMatrix.graph_url}
                alt="Confusion Matrix"
                className="graph-image"
              />
            ) : (
              <p>No confusion matrix available</p>
            )}

          </div>

        </div>

        <div className="graph-card">

          <div className="graph-header">
            📈 ROC Curve
          </div>

          <div className="graph-body">

            {rocCurve?.graph_url ? (
              <img
                src={rocCurve.graph_url}
                alt="ROC Curve"
                className="graph-image"
              />
            ) : (
              <p>No ROC Curve Available</p>
            )}

          </div>

        </div>

      </div>
    </Layout>
  );
};

export default Results;