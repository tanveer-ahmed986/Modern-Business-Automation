import api from "./api";

export interface BackupRecord {
  filename: string;
  path: string;
  size: number;
  created_at: string;
}

export interface BackupSchedule {
  enabled: boolean;
  hour: number;
  minute: number;
}

export interface BackupStats {
  database_size: number;
  database_size_mb: number;
  backup_count: number;
  backup_total_size: number;
  backup_total_size_mb: number;
  oldest_backup: string | null;
  newest_backup: string | null;
  storage_location: string;
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

  async getBackupSchedule(): Promise<{ schedule: BackupSchedule; next_backup: string | null }> {
    const response = await api.get<{ schedule: BackupSchedule; next_backup: string | null }>("/system/backup/schedule");
    return response.data;
  }

  async updateBackupSchedule(schedule: BackupSchedule): Promise<{ message: string; schedule: BackupSchedule }> {
    const response = await api.post<{ message: string; schedule: BackupSchedule }>("/system/backup/schedule", schedule);
    return response.data;
  }

  async triggerBackupNow(): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>("/system/backup/trigger");
    return response.data;
  }

  async getBackupStats(): Promise<BackupStats> {
    const response = await api.get<BackupStats>("/system/backup/stats");
    return response.data;
  }
}

const systemService = new SystemService();
export default systemService;
export { systemService };
