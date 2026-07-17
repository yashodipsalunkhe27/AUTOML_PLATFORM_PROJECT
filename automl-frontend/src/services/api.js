import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;

export const getDatasetAnalysis = async () => {
    const response = await api.get("/dataset-analysis");
    return response.data;
};

