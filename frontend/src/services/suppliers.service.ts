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

const suppliersService = {
  getSuppliers: async (): Promise<Supplier[]> => {
    const response = await api.get("/suppliers");
    return response.data;
  },

  getSupplier: async (id: number): Promise<Supplier> => {
    const response = await api.get(`/suppliers/${id}`);
    return response.data;
  },

  createSupplier: async (supplier: SupplierCreate): Promise<Supplier> => {
    const response = await api.post("/suppliers", supplier);
    return response.data;
  },

  updateSupplier: async (id: number, supplier: SupplierUpdate): Promise<Supplier> => {
    const response = await api.put(`/suppliers/${id}`, supplier);
    return response.data;
  },

  deleteSupplier: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/suppliers/${id}`);
    return response.data;
  },
};

export default suppliersService;
