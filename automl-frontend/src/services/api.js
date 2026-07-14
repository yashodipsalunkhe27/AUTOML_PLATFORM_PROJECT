import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;

export const getDatasetAnalysis = async () => {
    const response = await api.get("/dataset-analysis");
    return response.data;
};

