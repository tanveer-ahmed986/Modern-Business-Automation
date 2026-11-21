import api from "./api";

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_count: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: PaginationMeta;
}

export interface Category {
  id: number;
  name: string;
}

export interface Product {
  id: number;
  name: string;
  category_id?: number;
  barcode: string;
  cost_price?: number | string; // Only for Admin/Manager - can be string from backend
  selling_price: number | string; // Can be string (Decimal) from backend
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

// NOTE: the hand-rolled TTL caches that used to live here were replaced by
// TanStack Query (see main.tsx QueryClientProvider). Components cache via
// useQuery keys and invalidate on mutations — services are now plain fetchers.

class InventoryService {
  // --- Categories ---
  async getCategories(signal?: AbortSignal): Promise<Category[]> {
    const response = await api.get<Category[]>("/inventory/categories", { signal });
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
  async getProducts(
    params?: { page?: number; page_size?: number; category_id?: number; is_active?: boolean },
    signal?: AbortSignal
  ): Promise<PaginatedResponse<Product>> {
    const response = await api.get<PaginatedResponse<Product>>("/inventory/products", { params, signal });
    return response.data;
  }

  // Backward compatibility: get all products (for components not yet updated)
  async getAllProducts(signal?: AbortSignal): Promise<Product[]> {
    const response = await this.getProducts({ page: 1, page_size: 1000 }, signal);
    return response.items;
  }

  async searchProducts(
    query: string,
    page: number = 1,
    page_size: number = 20,
    signal?: AbortSignal,
    includeInactive: boolean = false
  ): Promise<PaginatedResponse<Product>> {
    const response = await api.get<PaginatedResponse<Product>>("/inventory/products/search", {
      params: { query, page, page_size, include_inactive: includeInactive },
      signal
    });
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

  async deleteProduct(id: number): Promise<{ message: string; soft_deleted: boolean }> {
    const response = await api.delete<{ message: string; soft_deleted: boolean }>(`/inventory/products/${id}`);
    return response.data;
  }
}

export const inventoryService = new InventoryService();
export default inventoryService;
