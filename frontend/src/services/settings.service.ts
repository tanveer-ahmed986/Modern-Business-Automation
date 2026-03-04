import api from "./api";

export interface Settings {
  id: number;
  business_name: string;
  business_logo_url?: string;
  tax_rate: number;
  currency: string;
  feature_flags: Record<string, boolean>;
  updated_at: string;
}

class SettingsService {
  async getSettings(): Promise<Settings> {
    const response = await api.get<Settings>("/settings/");
    return response.data;
  }

  async updateSettings(settings: Partial<Settings>): Promise<Settings> {
    const response = await api.put<Settings>("/settings/", settings);
    return response.data;
  }
}

export const settingsService = new SettingsService();
export default settingsService;
