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

// Module-level cache so the hook returns instantly after first successful load.
// This eliminates redundant renders/loading states when navigating between sections.
let _brandingCache: Branding | null = null;

export const useBranding = () => {
  const [branding, setBranding] = useState<Branding>(
    _brandingCache || {
      businessName: "MBAS",
      currency: "USD",
      taxRate: 0,
      isLoading: true,
      error: null,
    }
  );

  useEffect(() => {
    // If already cached, set immediately and skip fetch
    if (_brandingCache) {
      setBranding(_brandingCache);
      return;
    }

    const controller = new AbortController();
    const fetchBranding = async () => {
      try {
        const settings = await settingsService.getSettings();
        if (controller.signal.aborted) return;
        const result: Branding = {
          businessName: settings.business_name,
          logoUrl: settings.business_logo_url,
          currency: settings.currency,
          taxRate: settings.tax_rate,
          isLoading: false,
          error: null,
        };
        _brandingCache = result;
        setBranding(result);
      } catch (err) {
        if (controller.signal.aborted) return;
        setBranding((prev) => ({
          ...prev,
          isLoading: false,
          error: "Failed to load branding settings",
        }));
      }
    };

    fetchBranding();
    return () => { controller.abort(); };
  }, []);

  return branding;
};

export default useBranding;
