import { useState, useRef } from "react";
import Layout from "../layout/Layout";
import "../styles/upload.css";
import { FaCloudUploadAlt, FaFileCsv } from "react-icons/fa";
import api from "../services/api";
import "../styles/Page.css";

function Upload() {

  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("Waiting for upload...");
  const [datasetInfo, setDatasetInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChooseFile = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
      setUploadStatus("File selected successfully.");
    }
  };

  const handleUpload = async () => {

    if (!selectedFile) {
      alert("Please choose a dataset first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {

      setLoading(true);

      const response = await api.post(
        "/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setDatasetInfo(response.data);

      setUploadStatus(response.data.message);

    } catch (error) {

      setUploadStatus(
        error.response?.data?.detail || "Upload Failed."
      );

    } finally {

      setLoading(false);

    }

  };

  return (
    <Layout>

      <div className="page">

        <h1 className="upload-title">
          Upload Dataset
        </h1>

        <p className="upload-subtitle">
          Upload your CSV, Excel or JSON dataset to begin the AutoML pipeline.
        </p>

        {/* Upload Box */}

        <div className="page-card upload-box">

          <FaCloudUploadAlt className="upload-icon" />

          <h2>Drag & Drop Dataset Here</h2>

          <p>or</p>

          <button
            className="choose-btn"
            onClick={handleChooseFile}
          >
            Choose File
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.json"
            style={{ display: "none" }}
            onChange={handleFileChange}
          />

        </div>

        {/* File Information */}

        <div className="page-card file-card">

          <div className="file-row">

            <FaFileCsv className="csv-icon" />

            <div>

              <h3>Selected File</h3>

              <p>
                {selectedFile
                  ? selectedFile.name
                  : "No file selected"}
              </p>

            </div>

          </div>

          <div className="file-size">

            <strong>File Size</strong>

            <p>
              {selectedFile
                ? `${(selectedFile.size / 1024).toFixed(2)} KB`
                : "--"}
            </p>

          </div>

        </div>

        {/* Upload Button */}

        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload Dataset"}
        </button>

        {/* Upload Status */}

        <div className="page-card status-card">

          <h3>Upload Status</h3>

          <p>{uploadStatus}</p>

        </div>

        {/* Dataset Information */}

        {datasetInfo && (

          <div className="status-card">

            <h3>Dataset Information</h3>

            <p>
              <strong>Filename:</strong> {datasetInfo.filename}
            </p>

            <p>
              <strong>Rows:</strong> {datasetInfo.rows}
            </p>

            <p>
              <strong>Columns:</strong> {datasetInfo.columns}
            </p>

          </div>

        )}

      </div>

    </Layout>
  );
}

export default Upload;