import { useEffect, useState } from "react";
import Layout from "../layout/Layout";
import "../styles/Prediction.css";
import api from "../services/api";
import "../styles/Page.css";

import {
  FaMagic,
  FaCheckCircle,
} from "react-icons/fa";

const getPredictionMessage = (prediction) => {
  return `Predicted Class: ${prediction}`;
};
function Prediction() {

  const [schema, setSchema] = useState({});
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // =============================
  // Load Prediction Schema
  // =============================
  useEffect(() => {

    const loadSchema = async () => {

      try {

        const response = await api.get("/prediction-schema");

        setSchema(response.data);

        const initialData = {};

        Object.entries(response.data).forEach(([key, type]) => {

          initialData[key] =
            type === "number"
              ? ""
              : "";

        });

        setFormData(initialData);

      } catch (error) {

        alert(
          error.response?.data?.detail ||
          "Unable to load prediction schema."
        );

      }

    };

    loadSchema();

  }, []);

  // =============================
  // Input Change
  // =============================
  const handleChange = (name, value) => {

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

  };

  // =============================
  // Predict
  // =============================
  const handlePredict = async () => {

    for (const key in formData) {
      if (formData[key] === "") {
        alert(`${key} is required`);
        return;
      }
    }

    try {

      setLoading(true);

      const payload = {};

      Object.entries(schema).forEach(([key, type]) => {

        payload[key] =
          type === "number"
            ? Number(formData[key])
            : formData[key];

      });

      const response = await api.post(
        "/predict",
        payload
      );

      setResult(response.data);

    } catch (error) {

      alert(
        error.response?.data?.detail ||
        "Prediction failed."
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <Layout>

      <div className="page">

        <div className="page-header">

          <h1 className="page-title">
          Prediction
          </h1>

          <p className="page-subtitle">
          Predict the output using the trained Machine Learning model.
          </p>

          </div>

        <div className="page-card prediction-card">

          <div className="form-grid">

            {Object.entries(schema).map(([field, type]) => (

              <div
                className="form-group"
                key={field}
              >

                <label>{field}</label>

                {field === "Gender" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>

                ) : field === "Married" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                
                ) : field === "Dependents" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3+">3+</option>
                  </select>
                ) : field === "Education" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="Graduate">Graduate</option>
                    <option value="Not Graduate">Not Graduate</option>
                  </select>
                ) : field === "Self_Employed" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                ) : field === "Property_Area" ? (
                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="Urban">Urban</option>
                    <option value="Semiurban">Semiurban</option>
                    <option value="Rural">Rural</option>
                  </select>

                ) : field === "Credit_History" ? (

                  <select
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="1">1</option>
                    <option value="0">0</option>
                  </select>

                ) : type === "number" ? (

                  <input
                    type="number"
                    placeholder={`Enter ${field}`}
                    value={formData[field] || ""}
                    onChange={(e) => handleChange(field, e.target.value)}
                  />

                ) : (

                  <input
                    type="text"
                    placeholder={`Enter ${field}`}
                    value={formData[field] || ""}
                    onChange={(e) => handleChange(field, e.target.value)}
                  />

                )}

              </div>

            ))}

          </div>

          <button
            className="predict-btn"
            onClick={handlePredict}
            disabled={loading}
          >

            <FaMagic />

            {loading
              ? "Predicting..."
              : "Predict"}

          </button>

          <button
            className="reset-btn"
            onClick={() => {

              setResult(null);

              const resetData = {};

              Object.keys(schema).forEach((key) => {
                resetData[key] = "";
              });

              setFormData(resetData);

            }}
          >

            Reset

          </button>

        </div>

                {result && (

          <div className="page-card result-card">

            <h2>
              <FaCheckCircle className="result-icon" />
              Prediction Result
            </h2>

            <div className="result-row">
              <span>Problem Type</span>
              <strong>{result.problem_type}</strong>
            </div>

            <div className="result-row">
              <span>Prediction</span>

              <strong>

                {result.problem_type === "classification"
                  ? getPredictionMessage(result.prediction)
                  : result.predicted_value}

              </strong>
            </div>

            {result.problem_type === "classification" && (
              <div className="result-row">
                <span>Confidence</span>

                <strong>
                  {result.confidence_percent
                    ? Number(result.confidence_percent).toFixed(2)
                    : "0.00"}
                  %
                </strong>
              </div>
            )}

            <div className="result-row">
              <span>Model Used</span>

              <strong>{result.model_used}</strong>
            </div>

          </div>

        )}

      </div>

    </Layout>

  );

}

export default Prediction;