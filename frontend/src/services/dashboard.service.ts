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

export const getDashboardMetrics = async (): Promise<DashboardMetrics> => {
  const response = await api.get<DashboardMetrics>('/dashboard/metrics');
  return response.data;
};
