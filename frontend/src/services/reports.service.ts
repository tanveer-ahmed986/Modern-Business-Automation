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

  /**
   * Download the sales CSV via an authenticated request (Bearer header from
   * the api interceptor) and save it through a temporary anchor element.
   * Replaces the old window.open approach, which leaked the token in the URL,
   * read the wrong storage key (always 401), and was intercepted by the
   * service worker's SPA navigation fallback.
   */
  async downloadSalesCsv(startDate?: string, endDate?: string): Promise<void> {
    const params: Record<string, string> = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    const response = await api.get("/reports/export/sales", {
      params,
      responseType: "blob",
    });

    const url = URL.createObjectURL(response.data as Blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `sales_report_${startDate || "start"}_${endDate || "end"}.csv`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }
}

export default new ReportsService();
