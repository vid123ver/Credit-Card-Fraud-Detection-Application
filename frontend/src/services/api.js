import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
});

export const getHealth = async () => {
  const { data } = await api.get("/health");
  return data;
};

export const getTransactions = async () => {
  const { data } = await api.get("/transactions?limit=100");
  return data.transactions ?? [];
};

export const getAlerts = async () => {
  const { data } = await api.get("/alerts?limit=100");
  return data.alerts ?? [];
};

export const getModelPerformance = async () => {
  const { data } = await api.get("/models/performance");
  return data;
};

export default api;