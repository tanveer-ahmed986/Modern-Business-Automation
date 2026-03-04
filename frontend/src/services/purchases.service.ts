import api from "./api";
import type { Supplier } from "./suppliers.service";

export const PurchaseStatus = {
  ORDERED: "ordered",
  RECEIVED: "received",
  CANCELLED: "cancelled",
} as const;

export type PurchaseStatus = typeof PurchaseStatus[keyof typeof PurchaseStatus];

export const PaymentStatus = {
  PAID: "paid",
  PARTIAL: "partial",
  UNPAID: "unpaid",
} as const;

export type PaymentStatus = typeof PaymentStatus[keyof typeof PaymentStatus];

export interface PurchaseItem {
  id: number;
  purchase_id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  cost_price: number;
  subtotal: number;
}

export interface Purchase {
  id: number;
  supplier_id: number | null;
  user_id: number;
  reference_number: string | null;
  total_amount: number;
  tax_amount: number;
  discount_amount: number;
  grand_total: number;
  paid_amount: number;
  status: PurchaseStatus;
  payment_status: PaymentStatus;
  notes: string | null;
  created_at: string;
  items: PurchaseItem[];
  supplier?: Supplier;
}

export interface PurchaseItemCreate {
  product_id: number;
  quantity: number;
  cost_price: number;
}

export interface PurchaseCreate {
  supplier_id?: number;
  reference_number?: string;
  items: PurchaseItemCreate[];
  tax_amount?: number;
  discount_amount?: number;
  paid_amount?: number;
  notes?: string;
}

const purchasesService = {
  getPurchases: async (params?: { supplier_id?: number; skip?: number; limit?: number }): Promise<Purchase[]> => {
    const response = await api.get("/purchases", { params });
    return response.data;
  },

  getPurchase: async (id: number): Promise<Purchase> => {
    const response = await api.get(`/purchases/${id}`);
    return response.data;
  },

  createPurchase: async (purchase: PurchaseCreate): Promise<Purchase> => {
    const response = await api.post("/purchases", purchase);
    return response.data;
  },
};

export default purchasesService;
