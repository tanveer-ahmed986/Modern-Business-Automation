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

// Caching/dedup is handled by TanStack Query (queryKey: ['dashboard-metrics']);
// this is now a plain fetcher.
export const getDashboardMetrics = async (signal?: AbortSignal): Promise<DashboardMetrics> => {
  const response = await api.get<DashboardMetrics>('/dashboard/metrics', { signal });
  return response.data;
};

export interface DailyRevenuePoint {
  date: string;
  revenue: number | string;
}

export interface PaymentMethodTotal {
  method: string;
  total: number | string;
  count: number;
}

export interface DashboardTrends {
  daily_revenue: DailyRevenuePoint[];
  payment_breakdown: PaymentMethodTotal[];
}

export const getDashboardTrends = async (signal?: AbortSignal): Promise<DashboardTrends> => {
  const response = await api.get<DashboardTrends>('/dashboard/trends', { signal });
  return response.data;
};
