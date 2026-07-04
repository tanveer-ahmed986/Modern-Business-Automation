import axios from 'axios';
import type { AxiosRequestConfig } from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15s timeout (writes are serialized server-side, no long busy waits)
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

// ---------------------------------------------------------------------------
// Automatic retry for transient failures (GET only – never retry mutations)
// ---------------------------------------------------------------------------
api.interceptors.response.use(undefined, async (error) => {
  if (axios.isCancel(error)) return Promise.reject(error);

  const config = error.config;
  if (!config) return Promise.reject(error);

  // Only retry safe, idempotent methods (GET/HEAD/OPTIONS)
  const safeMethod = ['get', 'head', 'options'].includes((config.method || '').toLowerCase());
  const retryCount: number = (config as any).__retryCount || 0;
  const isRetryable = !error.response || error.response.status >= 500;

  if (safeMethod && isRetryable && retryCount < 2) {
    (config as any).__retryCount = retryCount + 1;
    // Exponential backoff: 1s, 2s
    await new Promise(r => setTimeout(r, 1000 * (retryCount + 1)));
    return api(config);
  }

  return Promise.reject(error);
});

// Add a response interceptor to handle auth / license errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Silently ignore cancelled requests (user navigated away)
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }

    // Handle 401 Unauthorized (session expired)
    // Skip for /auth/login - that endpoint returns 401 for bad credentials,
    // which is NOT an expired session and should be handled by the login form.
    if (error.response?.status === 401) {
      const requestUrl = error.config?.url || '';
      const isLoginRequest = requestUrl.includes('/auth/login');

      if (!isLoginRequest) {
        sessionStorage.removeItem('mbas_token');
        sessionStorage.removeItem('mbas_user');
        // Redirect to login with expired flag
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login?expired=true';
        }
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

/**
 * Creates an AbortController and returns it along with an axios config
 * that uses it. Components should call controller.abort() on unmount.
 */
export function createCancellableRequest(): { controller: AbortController; config: AxiosRequestConfig } {
  const controller = new AbortController();
  return { controller, config: { signal: controller.signal } };
}

export default api;
