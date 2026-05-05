import api from './api';

export interface User {
  id: number;
  username: string;
  full_name?: string;
  role: 'admin' | 'manager' | 'sales';
  is_active: boolean;
  created_at: string;
}

export interface UserCreate {
  username: string;
  full_name?: string;
  password: string;
  role: 'admin' | 'manager' | 'sales';
  is_active: boolean;
}

class UsersService {
  async getUsers(): Promise<User[]> {
    const response = await api.get<User[]>('/users/');
    return response.data;
  }

  async createUser(userData: UserCreate): Promise<User> {
    const response = await api.post<User>('/users/', userData);
    return response.data;
  }

  async updateUser(userId: number, userData: UserCreate): Promise<User> {
    const response = await api.put<User>(`/users/${userId}`, userData);
    return response.data;
  }

  async deleteUser(userId: number): Promise<void> {
    await api.delete(`/users/${userId}`);
  }
}

const usersService = new UsersService();
export default usersService;
export { usersService };
