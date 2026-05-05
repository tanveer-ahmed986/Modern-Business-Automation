import api from './api';
import axios from 'axios';

export interface User {
  id: number;
  username: string;
  full_name: string | null;
  role: 'admin' | 'manager' | 'sales';
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Helper function to check if backend is reachable
const checkBackendHealth = async (): Promise<boolean> => {
  try {
    await axios.get(`${api.defaults.baseURL}/health`, { timeout: 5000 });
    return true;
  } catch (error) {
    return false;
  }
};

// Login with retry logic and exponential backoff
const login = async (username: string, password: string, retryCount = 0): Promise<AuthResponse> => {
  const MAX_RETRIES = 2;
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const response = await api.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.access_token) {
      sessionStorage.setItem('mbas_token', response.data.access_token);
      sessionStorage.setItem('mbas_user', JSON.stringify(response.data.user));
    }

    return response.data;
  } catch (error: any) {
    // Check if it's a timeout or network error
    const isTimeoutError = error.code === 'ECONNABORTED' || error.message?.includes('timeout');
    const isNetworkError = error.message === 'Network Error' || !error.response;

    if ((isTimeoutError || isNetworkError) && retryCount < MAX_RETRIES) {
      // Wait with exponential backoff before retrying
      const delay = Math.min(1000 * Math.pow(2, retryCount), 5000);
      await new Promise(resolve => setTimeout(resolve, delay));

      // Check if backend is healthy before retrying
      const isHealthy = await checkBackendHealth();
      if (!isHealthy) {
        throw new Error('SERVER_UNAVAILABLE');
      }

      return login(username, password, retryCount + 1);
    }

    // If it's a timeout/network error and we've exhausted retries
    if (isTimeoutError || isNetworkError) {
      throw new Error('SERVER_TIMEOUT');
    }

    throw error;
  }
};

const logout = () => {
  sessionStorage.removeItem('mbas_token');
  sessionStorage.removeItem('mbas_user');
};

const getCurrentUser = (): User | null => {
  const userStr = sessionStorage.getItem('mbas_user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {
      console.error('Failed to parse user from sessionStorage', e);
      return null;
    }
  }
  return null;
};

const isAuthenticated = (): boolean => {
  return !!sessionStorage.getItem('mbas_token');
};

const authService = {
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
};

export default authService;
