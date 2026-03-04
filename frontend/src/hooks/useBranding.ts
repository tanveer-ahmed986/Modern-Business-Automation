import { useState, useEffect } from "react";
import settingsService from "../services/settings.service";

export interface Branding {
  businessName: string;
  logoUrl?: string;
  currency: string;
  taxRate: number;
  isLoading: boolean;
  error: string | null;
}

export const useBranding = () => {
  const [branding, setBranding] = useState<Branding>({
    businessName: "MBAS",
    currency: "USD",
    taxRate: 0,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const fetchBranding = async () => {
      try {
        const settings = await settingsService.getSettings();
        setBranding({
          businessName: settings.business_name,
          logoUrl: settings.business_logo_url,
          currency: settings.currency,
          taxRate: settings.tax_rate,
          isLoading: false,
          error: null,
        });
      } catch (err) {
        setBranding((prev) => ({
          ...prev,
          isLoading: false,
          error: "Failed to load branding settings",
        }));
      }
    };

    fetchBranding();
  }, []);

  return branding;
};

export default useBranding;
