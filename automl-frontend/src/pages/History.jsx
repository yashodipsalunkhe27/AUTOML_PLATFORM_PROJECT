import { useEffect, useState } from "react";
import Layout from "../layout/Layout";
import "../styles/History.css";
import api from "../api/api";

import {
  FaHistory,
  FaSearch,
  FaEye,
  FaDatabase,
  FaRobot,
  FaBullseye,
  FaClock,
  FaCogs,
  FaBrain,
  FaCopy
} from "react-icons/fa";

function History() {
  const [historyData, setHistoryData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedHistory, setSelectedHistory] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await api.get("/training-history");

      setHistoryData(res.data);
      setFilteredData(res.data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const query = search.toLowerCase();

    const result = historyData.filter(
      (item) =>
        (item.dataset || "").toLowerCase().includes(query) ||
        (item.best_model || "").toLowerCase().includes(query) ||
        (item.problem_type || "").toLowerCase().includes(query)
    );

    setFilteredData(result);
  }, [search, historyData]);

  if (loading) {
    return (
      <Layout>
        <h2>Loading History...</h2>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="history">
        <h1 className="history-title">
          <FaHistory /> Training History
        </h1>

        <p className="history-subtitle">
          View previously trained machine learning models and their performance.
        </p>

        <div className="search-box">
          <FaSearch className="search-icon" />

          <input
            type="text"
            placeholder="Search by dataset or model..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="history-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Dataset</th>
                <th>Problem Type</th>
                <th>Best Model</th>
                <th>Score</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {filteredData.length > 0 ? (
                filteredData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.timestamp}</td>

                    <td>{item.dataset}</td>

                    <td style={{ textTransform: "capitalize" }}>
                      {item.problem_type}
                    </td>

                    <td>{item.best_model}</td>

                    <td>
                      {item.problem_type === "classification"
                        ? `${(item.accuracy * 100).toFixed(2)}%`
                        : item.r2_score}
                    </td>

                    <td>
                      <span className="status completed">
                        Completed
                      </span>
                    </td>

                    <td>
                      <button
                        className="view-btn"
                        onClick={() => setSelectedHistory(item)}
                      >
                        <FaEye /> View
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7">No history found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {selectedHistory && (

        <div className="modal-overlay">

        <div className="modal">

        <h2 className="modal-title">
        📋 Training Details
        </h2>

        {/* Dataset */}

        <div className="detail-item">

        <div className="detail-label">
        <FaDatabase />
        Dataset
        </div>

        <div className="detail-value">
        {selectedHistory.dataset}
        </div>

        </div>

        {/* Problem Type */}

        <div className="detail-item">

        <div className="detail-label">
        <FaBrain />
        Problem Type
        </div>

        <div className="detail-value">
        {selectedHistory.problem_type}
        </div>

        </div>

        {/* Best Model */}

        <div className="detail-item">

        <div className="detail-label">
        <FaRobot />
        Best Model
        </div>

        <div className="detail-value">
        {selectedHistory.best_model}
        </div>

        </div>

        {/* Accuracy */}

        <div className="detail-item">

        <div className="detail-label">
        <FaBullseye />
        Accuracy
        </div>

        <div className="detail-value">

        <span className="score-badge">

        {selectedHistory.problem_type === "classification"
        ? `${(selectedHistory.accuracy * 100).toFixed(2)}%`
        : selectedHistory.r2_score}

        </span>

        </div>

        </div>

        {/* Timestamp */}

        <div className="detail-item">

        <div className="detail-label">
        <FaClock />
        Timestamp
        </div>

        <div className="detail-value">
        {selectedHistory.timestamp}
        </div>

        </div>

        {/* Best Parameters */}

        <div className="detail-item">

        <div className="parameter-header">

        <div className="detail-label">
        <FaCogs />
        Best Parameters
        </div>

        <button
        className="copy-btn"
        onClick={() =>
        navigator.clipboard.writeText(
        JSON.stringify(
        selectedHistory.best_parameters,
        null,
        2
        )
        )
        }
        >

        <FaCopy />

        Copy

        </button>

        </div>

        <pre className="parameter-box">

        {JSON.stringify(
        selectedHistory.best_parameters,
        null,
        2
        )}

        </pre>

        </div>

        <button
        className="close-btn"
        onClick={() => setSelectedHistory(null)}
        >

        Close Details

        </button>

        </div>

        </div>

        )}
      </div>
    </Layout>
  );
}

export default History;