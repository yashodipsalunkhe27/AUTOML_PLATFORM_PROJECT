import { useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Analysis.css";
import api from "../services/api";
import "../styles/Page.css";

import {
  FaTable,
  FaDatabase,
  FaExclamationTriangle,
  FaClone,
  FaBullseye,
  FaLayerGroup,
} from "react-icons/fa";

function Analysis() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);

  const [targetColumn, setTargetColumn] = useState("");
  const [problemType, setProblemType] = useState("");

  const handleAnalysis = async () => {
    try {
      setLoading(true);

      const response = await api.get("/dataset-analysis");

      setAnalysisData(response.data);

      // Reset selection when a new dataset is analyzed
      setTargetColumn("");
      setProblemType("");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to analyze dataset."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleTargetChange = (e) => {
    const selected = e.target.value;

    setTargetColumn(selected);
    localStorage.setItem("targetColumn", selected);

    if (!analysisData) return;

    const dtype = analysisData.data_types[selected];

    if (
      dtype === "object" ||
      dtype === "str"
    ) {
      setProblemType("Classification");
      return;
    }

    if (
      dtype.includes("int") ||
      dtype.includes("float")
    ) {
      setProblemType("Regression");
      return;
    }

    setProblemType("Unknown");
  };

  const totalMissing =
    analysisData?.missing_values
      ? Object.values(
          analysisData.missing_values
        ).reduce((sum, value) => sum + value, 0)
      : "--";

  return (
    <Layout>
      <div className="page analysis">

        <div className="page-header">

          <h1 className="page-title">
          Dataset Analysis
          </h1>

          <p className="page-subtitle">
          Explore your uploaded dataset information before training the model.
          </p>

          </div>

        <div className="analysis-grid">

          <div className="page-card analysis-card">
            <FaTable className="analysis-icon" />
            <h3>Rows</h3>
            <h2>{analysisData?.rows ?? "--"}</h2>
          </div>

          <div className="page-card analysis-card">
            <FaDatabase className="analysis-icon" />
            <h3>Columns</h3>
            <h2>{analysisData?.columns ?? "--"}</h2>
          </div>

          <div className="page-card analysis-card">
            <FaExclamationTriangle className="analysis-icon warning" />
            <h3>Missing Values</h3>
            <h2>{totalMissing}</h2>
          </div>

          <div className="page-card analysis-card">
            <FaClone className="analysis-icon success" />
            <h3>Duplicate Rows</h3>
            <h2>{analysisData?.duplicate_rows ?? "--"}</h2>
          </div>

        </div>

        <div className="info-grid">

          <div className="page-card info-card">

            <div className="card-header">
              <FaBullseye />
              <span>Target Column</span>
            </div>

            <select
              value={targetColumn}
              onChange={handleTargetChange}
              disabled={!analysisData}
              style={{
                width: "100%",
                padding: "10px",
                marginTop: "15px",
                borderRadius: "8px",
                fontSize: "15px",
              }}
            >
              <option value="">
                Select Target Column
              </option>

              {analysisData?.column_names?.map((column) => (
                <option
                  key={column}
                  value={column}
                >
                  {column}
                </option>
              ))}
            </select>

          </div>

          <div className="page-card info-card">

            <div className="card-header">
              <FaLayerGroup />
              <span>Problem Type</span>
            </div>

            <p>
              {problemType || "Not Detected"}
            </p>

          </div>

        </div>

        <div className="column-grid">

          <div className="page-card column-card">

            <h3>Numerical Columns</h3>

            <ul>
              {analysisData?.numerical_columns?.length ? (
                analysisData.numerical_columns.map(
                  (col, index) => (
                    <li key={index}>
                      {col}
                    </li>
                  )
                )
              ) : (
                <li>No Numerical Columns</li>
              )}
            </ul>

          </div>

          <div className="page-card column-card">

            <h3>Categorical Columns</h3>

            <ul>
              {analysisData?.categorical_columns?.length ? (
                analysisData.categorical_columns.map(
                  (col, index) => (
                    <li key={index}>
                      {col}
                    </li>
                  )
                )
              ) : (
                <li>No Categorical Columns</li>
              )}
            </ul>

          </div>

        </div>

        <div className="button-area">

          <button
            className="analyze-btn"
            onClick={handleAnalysis}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Dataset"}
          </button>

        </div>

      </div>
    </Layout>
  );
}

export default Analysis;