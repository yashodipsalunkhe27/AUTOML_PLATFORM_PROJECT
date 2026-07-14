import { useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Settings.css";
import api from "../api/api";

import {
  FaCog,
  FaLink,
  FaTrash,
  FaSave,
  FaDatabase,
} from "react-icons/fa";

function Settings() {

  // API URL State
  const [apiUrl, setApiUrl] = useState(
    localStorage.getItem("apiUrl") || "http://127.0.0.1:8000"
  );

  // Loading State
  const [loading, setLoading] = useState(false);

  // ===========================
  // Save Settings
  // ===========================
  const saveSettings = () => {

    localStorage.setItem("apiUrl", apiUrl);

    alert("Settings Saved Successfully!");

  };

  // ===========================
  // Delete Model
  // ===========================
  const deleteModel = async () => {

    const confirmDelete = window.confirm(
      "Are you sure you want to delete the trained model?"
    );

    if (!confirmDelete) return;

    try {

      setLoading(true);

      const res = await api.delete("/delete-model");

      alert(res.data.message);

    } catch (err) {

      console.log(err);

      alert("Failed to delete model.");

    } finally {

      setLoading(false);

    }

  };

  return (
    <Layout>

      <div className="settings">

        <h1 className="settings-title">
          <FaCog />
          Settings
        </h1>

        <p className="settings-subtitle">
          Configure your AutoML platform preferences and project settings.
        </p>

        {/* ===========================
            API Configuration
        =========================== */}

        <div className="settings-card">

          <h2>
            <FaLink className="card-icon" />
            API Configuration
          </h2>

          <label>Backend API URL</label>

          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
          />

          <button
            className="save-btn"
            onClick={saveSettings}
          >
            <FaSave />
            Save Settings
          </button>

        </div>

        {/* ===========================
            Project Data
        =========================== */}

        <div className="settings-card">

          <h2>
            <FaDatabase className="card-icon" />
            Project Data
          </h2>

          <p>
            Delete the trained model and all generated artifacts.
          </p>

          <button
            className="delete-btn"
            onClick={deleteModel}
            disabled={loading}
          >
            <FaTrash />

            {loading ? "Deleting..." : "Delete Model"}

          </button>

        </div>

      </div>

    </Layout>
  );
}

export default Settings;