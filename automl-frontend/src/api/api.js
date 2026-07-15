import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Reports
export const getClassificationReport = () =>
  api.get("/classification-report");

export const getConfusionMatrix = () =>
  api.get("/confusion-matrix-graph");

export const getRocCurve = () =>
  api.get("/roc-curve-graph");

export const getCorrelationHeatmap = () =>
  api.get("/correlation-heatmap");

export const getFeatureImportance = () =>
  api.get("/feature-importance");

export const getFeatureImportanceGraph = () =>
  api.get("/feature-importance-graph");

export const getShapSummary = () =>
  api.get("/shap-summary");

export default api;