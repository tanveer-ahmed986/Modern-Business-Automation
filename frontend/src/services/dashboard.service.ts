import api from './api';

export interface MetricCard {
  title: string;
  value: string;
  description?: string;
  trend?: number;
  icon?: string;
}

export interface RecentSale {
  id: number;
  customer_name: string;
  grand_total: number | string;
  created_at: string;
  status: string;
}

export interface TopProduct {
  id: number;
  name: string;
  total_quantity: number;
  total_revenue: number | string;
}

export interface DashboardMetrics {
  cards: MetricCard[];
  recent_sales: RecentSale[];
  top_products: TopProduct[];
  low_stock_count: number;
}

// Cache dashboard metrics so switching away and back loads instantly.
// Invalidated after 60s so data stays reasonably fresh while preventing refetch storms.
let _metricsCache: { data: DashboardMetrics; ts: number } | null = null;
const _CACHE_TTL = 60_000;

// Deduplicate concurrent calls (e.g. StrictMode double-mount)
let _inflight: Promise<DashboardMetrics> | null = null;

export const getDashboardMetrics = async (signal?: AbortSignal): Promise<DashboardMetrics> => {
  if (_metricsCache && Date.now() - _metricsCache.ts < _CACHE_TTL) {
    return _metricsCache.data;
  }
  // Return stale cache immediately if available (stale-while-revalidate)
  // The caller gets instant data; next call after TTL will fetch fresh data.
  if (_metricsCache) {
    // Trigger background refresh (non-blocking)
    if (!_inflight) {
      _inflight = api.get<DashboardMetrics>('/dashboard/metrics', { signal })
        .then((response) => {
          _metricsCache = { data: response.data, ts: Date.now() };
          return response.data;
        })
        .catch(() => _metricsCache!.data)
        .finally(() => { _inflight = null; });
    }
    return _metricsCache.data;
  }
  if (_inflight) return _inflight;

  _inflight = api.get<DashboardMetrics>('/dashboard/metrics', { signal })
    .then((response) => {
      _metricsCache = { data: response.data, ts: Date.now() };
      return response.data;
    })
    .finally(() => { _inflight = null; });

  return _inflight;
};
