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

// Long TTL because settings rarely change during a session.
// Multiple hooks (useBranding, useCalculator) and pages (SupplierLedger,
// PurchasePage) all call getSettings() on mount — without a cache this
// caused 3-5 redundant API calls on every navigation.
const CACHE_TTL = 300_000; // 5 minutes - settings rarely change during a session

class SettingsService {
  private _cache: { data: Settings; ts: number } | null = null;
  private _inflight: Promise<Settings> | null = null;

  async getSettings(): Promise<Settings> {
    // Return cached value if fresh
    if (this._cache && Date.now() - this._cache.ts < CACHE_TTL) {
      return this._cache.data;
    }
    // Deduplicate concurrent requests (e.g. useBranding + useCalculator
    // both fire on the same render cycle)
    if (this._inflight) return this._inflight;

    this._inflight = api.get<Settings>("/settings/")
      .then((r) => {
        this._cache = { data: r.data, ts: Date.now() };
        return r.data;
      })
      .finally(() => { this._inflight = null; });

    return this._inflight;
  }

  async updateSettings(settings: Partial<Settings>): Promise<Settings> {
    const response = await api.put<Settings>("/settings/", settings);
    this._cache = { data: response.data, ts: Date.now() };
    return response.data;
  }
}

export const settingsService = new SettingsService();
export default settingsService;
