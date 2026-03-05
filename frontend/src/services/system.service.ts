import api from "./api";

export interface BackupRecord {
  filename: string;
  path: string;
  size: number;
  created_at: string;
}

class SystemService {
  async listBackups(): Promise<BackupRecord[]> {
    const response = await api.get<BackupRecord[]>("/system/backups");
    return response.data;
  }

  async createBackup(): Promise<{ message: string; path: string }> {
    const response = await api.post<{ message: string; path: string }>("/system/backup");
    return response.data;
  }

  async restoreBackup(filename: string): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>(`/system/restore?backup_filename=${encodeURIComponent(filename)}`);
    return response.data;
  }
}

export default new SystemService();
