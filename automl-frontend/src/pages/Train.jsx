import { useEffect, useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Train.css";
import api from "../services/api";
import "../styles/Page.css";

import {
  FaRobot,
  FaPlayCircle,
  FaBullseye,
  FaCheckCircle,
  FaCogs,
} from "react-icons/fa";

function Train() {
  const [analysisData, setAnalysisData] = useState(null);
  const [selectedTarget, setSelectedTarget] = useState("");
  const [trainingData, setTrainingData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load dataset analysis
  useEffect(() => {
    fetchAnalysis();
  }, []);

  const fetchAnalysis = async () => {
    try {
      const response = await api.get("/dataset-analysis");
      setAnalysisData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleTrain = async () => {
    if (!selectedTarget) {
      alert("Please select the target column.");
      return;
    }

    try {
      setLoading(true);
      setTrainingData(null); // clear old results before starting new training

      const response = await api.post(
        `/train?target_column=${selectedTarget}`
      );

      setTrainingData(response.data);

    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Training failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="train">

        <h1 className="train-title">
          Train Model
        </h1>

        <p className="train-subtitle">
          Configure the target column and train the best machine learning model.
        </p>

        <div className="train-card">

          <label>
            Target Column
          </label>

          <select
            value={selectedTarget}
            onChange={(e) => setSelectedTarget(e.target.value)}
          >
            <option value="">
              Select Target Column
            </option>

            {analysisData?.column_names?.map((column, index) => (
              <option key={index} value={column}>
                {column}
              </option>
            ))}
          </select>

          <label>
            Problem Type
          </label>

          <input
            type="text"
            value={trainingData?.problem_type || "Not Detected"}
            readOnly
          />

          <button
            className="train-btn"
            onClick={handleTrain}
            disabled={loading}
          >
            <FaPlayCircle />

            {loading ? "Training..." : "Train Model"}

          </button>

        </div>

        <div className="result-grid">

          <div className="result-card">

            <FaCheckCircle className="icon success" />

            <h3>Training Status</h3>

            <h2>
              {loading
                ? "Training..."
                : trainingData
                ? "Completed"
                : "Ready to Train"}
            </h2>

          </div>

          <div className="result-card">

            <FaRobot className="icon" />

            <h3>Best Model</h3>

            <h2>
              {trainingData?.best_model || "--"}
            </h2>

          </div>

          <div className="result-card">

            <FaBullseye className="icon" />

            <h3>
              Best Score
            </h3>

            <h2>
              {trainingData?.best_score ?? "--"}
            </h2>

          </div>

          <div className="result-card">

            <FaCogs className="icon" />

            <h3>
              Cross Validation
            </h3>

            <h2>
              {trainingData?.cross_validation?.mean_r2 ??
                trainingData?.cross_validation?.mean_accuracy ??
                "--"}
            </h2>

          </div>

        </div>

        <div className="parameter-card">

          <h2>
            Best Parameters
          </h2>

          {trainingData?.best_parameters &&
          Object.keys(trainingData.best_parameters).length > 0 ? (

            Object.entries(trainingData.best_parameters).map(
              ([key, value]) => (

                <div className="parameter-row" key={key}>

                  <span>{key}</span>

                  <strong>{String(value)}</strong>

                </div>

              )
            )

          ) : (

            <p>
              No hyperparameters available.
            </p>

          )}

        </div>

      </div>
    </Layout>
  );
}

export default Train;