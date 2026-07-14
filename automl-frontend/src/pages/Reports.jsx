import { useEffect, useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Reports.css";

import {
  getClassificationReport,
  getConfusionMatrix,
  getRocCurve,
  getCorrelationHeatmap,
  getFeatureImportance,
  getFeatureImportanceGraph,
  getShapSummary,
} from "../api/api";

import {
  FaFileAlt,
  FaTh,
  FaChartLine,
  FaChartBar,
  FaProjectDiagram,
  FaBrain,
} from "react-icons/fa";

function Reports() {
  const [classification, setClassification] = useState(null);
  const [confusion, setConfusion] = useState(null);
  const [roc, setRoc] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [feature, setFeature] = useState(null);
  const [featureGraph, setFeatureGraph] = useState(null);
  const [shap, setShap] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const isClassification = classification?.accuracy !== undefined && classification?.accuracy !== null;

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        classificationRes,
        confusionRes,
        rocRes,
        heatmapRes,
        featureRes,
        featureGraphRes,
        shapRes,
      ] = await Promise.all([
        getClassificationReport(),
        getConfusionMatrix(),
        getRocCurve(),
        getCorrelationHeatmap(),
        getFeatureImportance(),
        getFeatureImportanceGraph(),
        getShapSummary(),
      ]);

      setClassification(classificationRes.data);
      setConfusion(confusionRes.data);
      setRoc(rocRes.data);
      setHeatmap(heatmapRes.data);
      setFeature(featureRes.data);
      setFeatureGraph(featureGraphRes.data);
      setShap(shapRes.data);
    } catch (err) {
      console.error(err);

      if (err.response?.status === 400) {
        setError("No trained model available. Please train a model first.");
      } else {
        setError("Unable to load reports. Please try again later.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <h2 style={{ padding: "30px" }}>Loading Reports...</h2>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div
          style={{
            textAlign: "center",
            padding: "80px 20px",
          }}
        >
          <h1>📄 No Reports Available</h1>

          <p
            style={{
              color: "#666",
              fontSize: "18px",
              marginTop: "15px",
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
      <div className="reports">

        <h1 className="reports-title">Reports</h1>

        <p className="reports-subtitle">
          View all generated machine learning reports and visualizations.
        </p>

        <div className="reports-grid">

          {/* Classification Report */}
          <div className="report-card">
            <div className="report-icon icon-blue">
              <FaFileAlt />
            </div>

            <div className="report-header">
              <h2>Classification Report</h2>
              <span className={`status-dot ${isClassification ? "dot-active" : "dot-inactive"}`}></span>
            </div>

            <div className="placeholder-box">
              {isClassification ? (
                <div className="metric-grid">
                  <div className="metric-row"><span>Accuracy</span><strong>{classification.accuracy}</strong></div>
                  <div className="metric-row"><span>Precision</span><strong>{classification.precision}</strong></div>
                  <div className="metric-row"><span>Recall</span><strong>{classification.recall}</strong></div>
                  <div className="metric-row"><span>F1 Score</span><strong>{classification.f1_score}</strong></div>
                  <div className="metric-row"><span>ROC AUC</span><strong>{classification.roc_auc}</strong></div>
                </div>
              ) : (
                <p className="not-applicable">Not applicable for regression models</p>
              )}
            </div>

            <p>
              Detailed precision, recall, F1-score and support for each class.
            </p>
          </div>

          {/* Confusion Matrix */}
          <div className="report-card">
            <div className="report-icon icon-blue">
              <FaTh />
            </div>

            <div className="report-header">
              <h2>Confusion Matrix</h2>
              <span className={`status-dot ${confusion?.graph_url ? "dot-active" : "dot-inactive"}`}></span>
            </div>

            <div className="placeholder-box">
              {confusion?.graph_url ? (
                <img
                  src={confusion.graph_url}
                  alt="Confusion Matrix"
                  style={{ width: "100%" }}
                />
              ) : (
                <p className="not-applicable">
                  {isClassification ? "No graph available" : "Not applicable for regression models"}
                </p>
              )}
            </div>

            <p>
              Visual representation of prediction accuracy across classes.
            </p>
          </div>

          {/* ROC */}
          <div className="report-card">
            <div className="report-icon icon-purple">
              <FaChartLine />
            </div>

            <div className="report-header">
              <h2>ROC Curve</h2>
              <span className={`status-dot ${roc?.graph_url ? "dot-active" : "dot-inactive"}`}></span>
            </div>

            <div className="placeholder-box">
              {roc?.graph_url ? (
                <img
                  src={roc.graph_url}
                  alt="ROC"
                  style={{ width: "100%" }}
                />
              ) : (
                <p className="not-applicable">
                  {isClassification ? "No graph available" : "Not applicable for regression models"}
                </p>
              )}
            </div>

            <p>
              Displays the ROC curve and AUC score.
            </p>
          </div>

          {/* Feature Importance */}
          <div className="report-card">
            <div className="report-icon icon-purple">
              <FaChartBar />
            </div>

            <div className="report-header">
              <h2>Feature Importance</h2>
              <span className={`status-dot ${featureGraph?.graph_url ? "dot-active" : "dot-inactive"}`}></span>
            </div>

            <div className="placeholder-box">
              {featureGraph?.graph_url ? (
                <img
                  src={featureGraph.graph_url}
                  alt="Feature Importance"
                  style={{ width: "100%" }}
                />
              ) : (
                <p>{feature?.message}</p>
              )}
            </div>

            <p>
              Shows the most influential features used by the trained model.
            </p>
          </div>

          {/* Heatmap */}
          <div className="report-card">
            <div className="report-icon icon-purple">
              <FaProjectDiagram />
            </div>

            <div className="report-header">
              <h2>Correlation Heatmap</h2>
              <span className={`status-dot ${heatmap?.graph_url ? "dot-active" : "dot-inactive"}`}></span>
            </div>

            <div className="placeholder-box">
              {heatmap?.graph_url ? (
                <img
                  src={heatmap.graph_url}
                  alt="Heatmap"
                  style={{ width: "100%" }}
                />
              ) : (
                <p>No graph available</p>
              )}
            </div>

            <p>
              Displays correlation among numerical features.
            </p>
          </div>

          {/* SHAP */}
          <div className="report-card">
            <div className="report-icon icon-teal">
              <FaBrain />
            </div>

            <div className="report-header">
              <h2>SHAP Summary</h2>
              <span className="status-dot dot-inactive"></span>
            </div>

            <div className="placeholder-box">
              <p className="not-applicable">{shap?.message}</p>
            </div>
            <p>
              Explains model predictions using SHAP values.
            </p>
          </div>

        </div>
      </div>
    </Layout>
  );
}

export default Reports;