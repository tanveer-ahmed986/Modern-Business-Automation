import api from "./api";

export interface Supplier {
  id: number;
  name: string;
  contact_person: string | null;
  phone: string | null;
  email: string | null;
  address: string | null;
  balance: number;
  created_at: string;
}

export interface SupplierCreate {
  name: string;
  contact_person?: string;
  phone?: string;
  email?: string;
  address?: string;
}

export interface SupplierUpdate {
  name?: string;
  contact_person?: string;
  phone?: string;
  email?: string;
  address?: string;
  balance?: number;
}

export interface SupplierPaymentCreate {
  supplier_id: number;
  amount: number;
  payment_method: string;
  reference_number?: string;
  notes?: string;
}

export interface SupplierPayment {
  id: number;
  supplier_id: number;
  amount: number;
  payment_method: string;
  reference_number: string | null;
  notes: string | null;
  payment_date: string;
  created_at: string;
}

export interface SupplierLedgerSummary {
  total_purchased: number;
  total_paid: number;
  outstanding_balance: number;
}

export interface SupplierLedgerData {
  supplier: { id: number; name: string; balance: number };
  summary: SupplierLedgerSummary;
  purchases: Array<{
    id: number;
    reference_number: string | null;
    grand_total: number;
    paid_amount: number;
    payment_status: string;
    created_at: string;
  }>;
  payments: Array<{
    id: number;
    amount: number;
    payment_method: string;
    reference_number: string | null;
    notes: string | null;
    payment_date: string;
  }>;
}

// Simple TTL cache for supplier list
let _suppliersCache: { data: Supplier[]; ts: number } | null = null;
const _CACHE_TTL = 60_000; // 60 seconds - prevents refetch storms on navigation
let _suppliersInflight: Promise<Supplier[]> | null = null;

const suppliersService = {
  getSuppliers: async (signal?: AbortSignal): Promise<Supplier[]> => {
    if (_suppliersCache && Date.now() - _suppliersCache.ts < _CACHE_TTL) {
      return _suppliersCache.data;
    }
    if (_suppliersInflight) return _suppliersInflight;

    _suppliersInflight = api.get("/suppliers", { signal })
      .then((response) => {
        _suppliersCache = { data: response.data, ts: Date.now() };
        return response.data;
      })
      .finally(() => { _suppliersInflight = null; });

    return _suppliersInflight;
  },

  getSupplier: async (id: number): Promise<Supplier> => {
    const response = await api.get(`/suppliers/${id}`);
    return response.data;
  },

  createSupplier: async (supplier: SupplierCreate): Promise<Supplier> => {
    const response = await api.post("/suppliers", supplier);
    _suppliersCache = null;
    return response.data;
  },

  updateSupplier: async (id: number, supplier: SupplierUpdate): Promise<Supplier> => {
    const response = await api.put(`/suppliers/${id}`, supplier);
    _suppliersCache = null;
    return response.data;
  },

  deleteSupplier: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/suppliers/${id}`);
    _suppliersCache = null;
    return response.data;
  },

  getSupplierPayments: async (id: number): Promise<SupplierPayment[]> => {
    const response = await api.get(`/suppliers/${id}/payments`);
    return response.data;
  },

  recordPayment: async (id: number, payment: Omit<SupplierPaymentCreate, 'supplier_id'>): Promise<SupplierPayment> => {
    const response = await api.post(`/suppliers/${id}/payments`, {
      ...payment,
      supplier_id: id,
    });
    _suppliersCache = null;
    return response.data;
  },

  getSupplierLedger: async (id: number, signal?: AbortSignal): Promise<SupplierLedgerData> => {
    const response = await api.get(`/suppliers/${id}/ledger`, { signal });
    return response.data;
  },
};

export default suppliersService;
