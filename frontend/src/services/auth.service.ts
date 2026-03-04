import api from './api';

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

const login = async (username: string, password: string): Promise<AuthResponse> => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await api.post<AuthResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (response.data.access_token) {
    localStorage.setItem('mbas_token', response.data.access_token);
    localStorage.setItem('mbas_user', JSON.stringify(response.data.user));
  }

  return response.data;
};

const logout = () => {
  localStorage.removeItem('mbas_token');
  localStorage.removeItem('mbas_user');
};

const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('mbas_user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {
      console.error('Failed to parse user from localStorage', e);
      return null;
    }
  }
  return null;
};

const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('mbas_token');
};

const authService = {
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
};

export default authService;
