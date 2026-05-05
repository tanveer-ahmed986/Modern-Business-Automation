import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout for all requests
});

// Add a request interceptor to include the JWT token
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('mbas_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Custom event for upgrade prompts
export const upgradeRequiredEvent = new EventTarget();

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized (session expired)
    if (error.response?.status === 401) {
      sessionStorage.removeItem('mbas_token');
      sessionStorage.removeItem('mbas_user');
      // Redirect to login with expired flag
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login?expired=true';
      }
    }

    // Handle 403 Forbidden (feature not enabled or license expired)
    if (error.response?.status === 403) {
      const detail = error.response.data?.detail || '';

      // Check if it's a feature upgrade requirement
      if (detail.includes('not enabled') || detail.includes('requires')) {
        // Emit custom event for UpgradeModal
        upgradeRequiredEvent.dispatchEvent(
          new CustomEvent('upgrade-required', {
            detail: {
              message: detail,
              requiredTier: detail.toLowerCase().includes('premium') ? 'premium' : 'standard',
            },
          })
        );
      }

      // Check if license expired
      if (detail.includes('expired')) {
        // Show license expired message
        upgradeRequiredEvent.dispatchEvent(
          new CustomEvent('license-expired', {
            detail: { message: detail },
          })
        );
      }
    }

    return Promise.reject(error);
  }
);

export default api;
