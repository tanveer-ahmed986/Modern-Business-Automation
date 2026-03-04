import api from "./api";

export interface Category {
  id: number;
  name: string;
}

export interface Product {
  id: number;
  name: string;
  category_id?: number;
  barcode: string;
  cost_price?: number; // Only for Admin/Manager
  selling_price: number;
  stock_quantity: number;
  low_stock_threshold: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  category?: Category;
}

export interface ProductCreate {
  name: string;
  category_id?: number;
  barcode: string;
  cost_price: number;
  selling_price: number;
  stock_quantity: number;
  low_stock_threshold: number;
  is_active?: boolean;
}

export interface ProductUpdate {
  name?: string;
  category_id?: number;
  barcode?: string;
  cost_price?: number;
  selling_price?: number;
  stock_quantity?: number;
  low_stock_threshold?: number;
  is_active?: boolean;
}

class InventoryService {
  // --- Categories ---
  async getCategories(): Promise<Category[]> {
    const response = await api.get<Category[]>("/inventory/categories");
    return response.data;
  }

  async createCategory(name: string): Promise<Category> {
    const response = await api.post<Category>("/inventory/categories", { name });
    return response.data;
  }

  async updateCategory(id: number, name: string): Promise<Category> {
    const response = await api.put<Category>(`/inventory/categories/${id}`, { name });
    return response.data;
  }

  async deleteCategory(id: number): Promise<void> {
    await api.delete(`/inventory/categories/${id}`);
  }

  // --- Products ---
  async getProducts(params?: { skip?: number; limit?: number; category_id?: number }): Promise<Product[]> {
    const response = await api.get<Product[]>("/inventory/products", { params });
    return response.data;
  }

  async searchProducts(query: string, limit: number = 20): Promise<Product[]> {
    const response = await api.get<Product[]>("/inventory/products/search", { params: { query, limit } });
    return response.data;
  }

  async getProduct(id: number): Promise<Product> {
    const response = await api.get<Product>(`/inventory/products/${id}`);
    return response.data;
  }

  async createProduct(product: ProductCreate): Promise<Product> {
    const response = await api.post<Product>("/inventory/products", product);
    return response.data;
  }

  async updateProduct(id: number, product: ProductUpdate): Promise<Product> {
    const response = await api.put<Product>(`/inventory/products/${id}`, product);
    return response.data;
  }

  async deleteProduct(id: number): Promise<void> {
    await api.delete(`/inventory/products/${id}`);
  }
}

export const inventoryService = new InventoryService();
export default inventoryService;
