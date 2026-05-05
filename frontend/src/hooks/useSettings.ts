import { useState, useEffect } from "react";
import settingsService from "../services/settings.service";

export interface Settings {
  id: number;
  business_name: string;
  business_logo_url?: string;
  currency: string;
  tax_rate: number;
  feature_flags: Record<string, boolean>;
}

export interface UseSettingsResult {
  settings: Settings | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useSettings = (): UseSettingsResult => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSettings = async () => {
    try {
      setIsLoading(true);
      const data = await settingsService.getSettings();
      setSettings(data);
      setError(null);
    } catch (err) {
      setError("Failed to load settings");
      console.error("Error loading settings:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  return {
    settings,
    isLoading,
    error,
    refetch: fetchSettings,
  };
};

export default useSettings;
