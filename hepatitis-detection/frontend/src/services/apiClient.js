/**
 * API Client Service
 * Handles all communication with the backend Flask API
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status}`, response.data);
    return response;
  },
  (error) => {
    console.error('[API Error]', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

/**
 * API Service
 */
const ApiService = {
  /**
   * Get health status of the API
   */
  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  /**
   * Get API information
   */
  getInfo: async () => {
    const response = await apiClient.get('/info');
    return response.data;
  },

  /**
   * Make a prediction for a patient
   * @param {Object} patientData - Patient medical data
   * @returns {Promise} Prediction result
   */
  predict: async (patientData) => {
    try {
      const response = await apiClient.post('/predict', patientData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Prediction failed. Please check your input.',
        status: error.response?.status || 500,
      };
    }
  },

  /**
   * Save a prediction result to the database
   * @param {Object} predictionData - Prediction data to save
   * @returns {Promise} Save result
   */
  savePrediction: async (predictionData) => {
    try {
      const response = await apiClient.post('/save', predictionData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to save prediction.',
        status: error.response?.status || 500,
      };
    }
  },

  /**
   * Retrieve prediction history
   * @param {Number} limit - Maximum records to retrieve
   * @returns {Promise} History data
   */
  getHistory: async (limit = 100) => {
    try {
      const response = await apiClient.get('/history', {
        params: { limit },
      });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to retrieve history.',
        status: error.response?.status || 500,
      };
    }
  },
};

export default ApiService;
