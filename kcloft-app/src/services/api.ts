import axios from "axios";
import type { AxiosInstance, InternalAxiosRequestConfig } from "axios";
import { getAccessToken } from "../auth/authService";

// Base URL for your FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add Bearer token
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const token = await getAccessToken();
    console.log("API Request - Token retrieved:", token ? "Yes (length: " + token.length + ")" : "No");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("API Request - Authorization header set");
    } else {
      console.warn("API Request - No token available, request will likely fail");
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Prevent infinite retry loops
      const retryCount = error.config?.__retryCount || 0;
      if (retryCount >= 1) {
        console.error("Max retry attempts reached for 401 error");
        return Promise.reject(error);
      }
      
      // Token might be expired, try to get a new one
      const token = await getAccessToken();
      if (token && error.config) {
        error.config.__retryCount = retryCount + 1;
        error.config.headers = error.config.headers || {};
        error.config.headers.Authorization = `Bearer ${token}`;
        return apiClient.request(error.config);
      } else {
        console.error("Failed to get access token for retry");
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

