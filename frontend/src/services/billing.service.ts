import api from "./api";

export interface SaleItemCreate {
  product_id: number;
  quantity: number;
}

export interface SaleCreate {
  customer_id?: number;
  items: SaleItemCreate[];
  payment_method: "cash" | "card" | "transfer" | "credit";
  discount_amount: number;
}

export interface Customer {
  id: number;
  name: string;
  phone?: string;
  email?: string;
  address?: string;
  created_at: string;
}

export interface SaleItem {
  id: number;
  sale_id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface Sale {
  id: number;
  invoice_number: string;
  customer_id?: number;
  user_id: number;
  total_amount: number | string;
  tax_amount: number | string;
  discount_amount: number | string;
  grand_total: number | string;
  payment_method: string;
  status: string;
  created_at: string;
  items: SaleItem[];
  customer?: Customer;
}

export interface PaginatedSales {
  items: Sale[];
  pagination: {
    page: number;
    page_size: number;
    total_count: number;
    total_pages: number;
  };
}

export const billingService = {
  createSale: async (saleData: SaleCreate): Promise<Sale> => {
    const response = await api.post<Sale>("/billing/sales", saleData);
    return response.data;
  },

  getSales: async (params?: { page?: number; page_size?: number }): Promise<PaginatedSales> => {
    const response = await api.get<PaginatedSales>("/billing/sales", { params });
    return response.data;
  },

  refundSale: async (saleId: number): Promise<Sale> => {
    const response = await api.post<Sale>(`/billing/sales/${saleId}/refund`);
    return response.data;
  },

  getSale: async (saleId: number): Promise<Sale> => {
    const response = await api.get<Sale>(`/billing/sales/${saleId}`);
    return response.data;
  },

  getCustomers: async (search?: string): Promise<Customer[]> => {
    const response = await api.get<Customer[]>("/billing/customers", { params: { search } });
    return response.data;
  },

  createCustomer: async (customerData: Partial<Customer>): Promise<Customer> => {
    const response = await api.post<Customer>("/billing/customers", customerData);
    return response.data;
  },
};
