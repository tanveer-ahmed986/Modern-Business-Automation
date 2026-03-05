import api from "./api";

export interface SalesReport {
  summary: {
    total_revenue: number;
    total_tax: number;
    total_discount: number;
    sale_count: number;
  };
  payment_methods: Record<string, number>;
  top_products: {
    name: string;
    quantity: number;
    revenue: number;
  }[];
  category_sales: {
    name: string;
    revenue: number;
  }[];
  period: {
    start: string;
    end: string;
  };
}

export interface ProfitLossReport {
  revenue: number;
  cogs: number;
  gross_profit: number;
  total_purchases: number;
  period: {
    start: string;
    end: string;
  };
}

class ReportsService {
  async getSalesReport(startDate?: string, endDate?: string): Promise<SalesReport> {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await api.get<SalesReport>("/reports/sales", { params });
    return response.data;
  }

  async getProfitLossReport(startDate?: string, endDate?: string): Promise<ProfitLossReport> {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await api.get<ProfitLossReport>("/reports/profit-loss", { params });
    return response.data;
  }

  getExportSalesUrl(startDate?: string, endDate?: string): string {
    const baseUrl = (api.defaults.baseURL || "").replace(/\/$/, "");
    const params = new URLSearchParams();
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
    
    const token = localStorage.getItem("token");
    if (token) params.append("token", token); // Note: Backend usually expects Bearer in header, but for simple link downloads we might need a workaround or handle it in frontend
    
    return `${baseUrl}/reports/export/sales?${params.toString()}`;
  }
}

export default new ReportsService();
