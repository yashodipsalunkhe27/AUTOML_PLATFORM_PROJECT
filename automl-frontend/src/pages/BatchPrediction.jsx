import { useState } from "react";
import Layout from "../layout/Layout";
import "../styles/BatchPrediction.css";
import api from "../services/api";


import {
  FaFileCsv,
  FaUpload,
  FaDownload,
  FaChartPie,
  FaCheckCircle,
  FaTimesCircle,
  FaDatabase,
} from "react-icons/fa";

function BatchPrediction() {

  const [selectedFile, setSelectedFile] = useState(null);
  const [totalRows, setTotalRows] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");

  // ===========================
  // File Selection
  // ===========================

  const handleFileChange = (e) => {

    const file = e.target.files[0];

    if (!file) return;

    setSelectedFile(file);

    setUploadMessage(`✅ ${file.name} uploaded successfully`);

    // Count CSV rows
    const reader = new FileReader();

    reader.onload = (event) => {

      const text = event.target.result;

      const rows = text
        .trim()
        .split("\n").length - 1;

      setTotalRows(rows);

    };

    reader.readAsText(file);

  };

  // ===========================
  // Batch Prediction
  // ===========================

  const handleBatchPredict = async () => {

    if (!selectedFile) {

      alert("Please choose a CSV file.");

      return;

    }

    try {

      setLoading(true);

      setResult(null);

      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );

      const response = await api.post(

        "/batch-predict",

        formData,

        {

          headers: {

            "Content-Type":
              "multipart/form-data",

          },

        }

      );

      setResult(response.data);

    }

    catch (error) {

      alert(

        error.response?.data?.detail ||

        "Batch prediction failed."

      );

    }

    finally {

      setLoading(false);

    }

  };

  // ===========================
  // Download Predictions
  // ===========================

  const handleDownload = () => {

    if (!result?.download_url) return;

    window.open(
      result.download_url,
      "_blank"
    );

  };

  return (

    <Layout>

      <div className="batch">

        <h1 className="batch-title">

          Batch Prediction

        </h1>

        <p className="batch-subtitle">

          Upload a CSV dataset and predict multiple records at once.

        </p>

        {/* Upload Card */}

          <div
            className={`upload-card ${dragActive ? "drag-active" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragActive(false);

              const file = e.dataTransfer.files[0];

              if (!file) return;

              setSelectedFile(file);

              const reader = new FileReader();

              reader.onload = (event) => {
                const text = event.target.result;
                const rows = text.trim().split("\n").length - 1;
                setTotalRows(rows);
              };

              reader.readAsText(file);
            }}
          >

            <FaFileCsv className="upload-icon" />

            <h2>Upload CSV Dataset</h2>

            <input
              id="csv-upload"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              hidden
            />

            <label htmlFor="csv-upload" className="upload-label">
              Choose CSV File
            </label>

            <p className="drag-text">
              Or Drag & Drop CSV Here
            </p>

            {uploadMessage && (
            <p className="upload-success">
              {uploadMessage}
            </p>
          )}

          <div className="file-info">

            <div className="file-row">

              <span>

                Selected File

              </span>

              <strong>

                {selectedFile
                  ? selectedFile.name
                  : "--"}

              </strong>

            </div>

            <div className="file-row">

              <span>

                Total Rows

              </span>

              <strong>

                {totalRows || "--"}

              </strong>

            </div>

          </div>

          <button

            className="predict-btn"

            onClick={handleBatchPredict}

            disabled={loading}

          >

            <FaUpload />

            {loading
              ? "Predicting..."
              : "Predict Batch"}

          </button>

        </div>

        {/* Result */}

        {result && (

          <>

          <div className="success-banner">
            🎉 Batch Prediction Completed Successfully
          </div>

            <div className="summary-card">

              <h2>
                <FaChartPie />
                Prediction Summary
              </h2>

              <div className="summary-grid">

                <div className="summary-box">

                  <h3>
                    <FaDatabase />
                    Rows Processed
                  </h3>

                  <p>{result.rows_processed}</p>

                </div>

                {result.problem_type === "classification" ? (

                  <>

                    <div className="summary-box approved">

                      <h3>
                        <FaCheckCircle />
                        Approved
                      </h3>

                      <p>{result.prediction_summary?.Approved || 0}</p>

                    </div>

                    <div className="summary-box rejected">

                      <h3>
                        <FaTimesCircle />
                        Rejected
                      </h3>

                      <p>{result.prediction_summary?.Rejected || 0}</p>

                    </div>

                  </>

                ) : (

                  <>

                    <div className="summary-box approved">

                      <h3>
                        <FaCheckCircle />
                        Average Prediction
                      </h3>

                      <p>{result.regression_summary?.average ?? "--"}</p>

                    </div>

                    <div className="summary-box rejected">

                      <h3>
                        <FaTimesCircle />
                        Min / Max
                      </h3>

                      <p>
                        {result.regression_summary
                          ? `${result.regression_summary.minimum} / ${result.regression_summary.maximum}`
                          : "--"}
                      </p>

                    </div>

                  </>

                )}

              </div>   {/* Close summary-grid */}

              </div>   {/* Close summary-card */}

              <div className="download-card">

                <p className="download-text">
                  ✔ Your prediction file is ready.
                </p>

                <button
                  className="download-btn"
                  onClick={handleDownload}
                >

                  <FaDownload />

                  Download prediction_results.csv

                </button>

              </div>

          </>

        )}

      </div>

    </Layout>

  );

}

export default BatchPrediction;