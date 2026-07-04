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

// Simple in-memory TTL cache to avoid re-fetching data when navigating between sections
interface CacheEntry<T> { data: T; timestamp: number; }
const CACHE_TTL = 60_000; // 60 seconds - longer TTL prevents refetch storms on navigation

class InventoryService {
  // Cache management disabled for paginated API (pagination makes caching complex)
  // private _productsCache: CacheEntry<Product[]> | null = null;
  private _categoriesCache: CacheEntry<Category[]> | null = null;
  // Cache recent search queries so repeated/similar typing doesn't hit API
  private _searchCache = new Map<string, CacheEntry<Product[]>>();

  // Deduplicate concurrent requests (prevents multiple mounts from firing duplicate fetches)
  // private _productsInflight: Promise<Product[]> | null = null;
  private _categoriesInflight: Promise<Category[]> | null = null;

  /** Clear caches after mutations so next read fetches fresh data */
  private _invalidate() {
    // this._productsCache = null;
    this._categoriesCache = null;
    this._searchCache.clear();
  }

  // --- Categories ---
  async getCategories(signal?: AbortSignal): Promise<Category[]> {
    if (this._categoriesCache && Date.now() - this._categoriesCache.timestamp < CACHE_TTL) {
      return this._categoriesCache.data;
    }
    if (this._categoriesInflight) return this._categoriesInflight;

    this._categoriesInflight = api.get<Category[]>("/inventory/categories", { signal })
      .then((response) => {
        this._categoriesCache = { data: response.data, timestamp: Date.now() };
        return response.data;
      })
      .finally(() => { this._categoriesInflight = null; });

    return this._categoriesInflight;
  }

  async createCategory(name: string): Promise<Category> {
    const response = await api.post<Category>("/inventory/categories", { name });
    this._categoriesCache = null;
    return response.data;
  }

  async updateCategory(id: number, name: string): Promise<Category> {
    const response = await api.put<Category>(`/inventory/categories/${id}`, { name });
    this._categoriesCache = null;
    return response.data;
  }

  async deleteCategory(id: number): Promise<void> {
    await api.delete(`/inventory/categories/${id}`);
    this._categoriesCache = null;
  }

  // --- Products ---
  async getProducts(params?: { page?: number; page_size?: number; category_id?: number }, signal?: AbortSignal): Promise<PaginatedResponse<Product>> {
    const response = await api.get<PaginatedResponse<Product>>("/inventory/products", { params, signal });
    return response.data;
  }

  // Backward compatibility: get all products (for components not yet updated)
  async getAllProducts(signal?: AbortSignal): Promise<Product[]> {
    const response = await this.getProducts({ page: 1, page_size: 1000 }, signal);
    return response.items;
  }

  async searchProducts(query: string, page: number = 1, page_size: number = 20, signal?: AbortSignal): Promise<PaginatedResponse<Product>> {
    const key = `${query}|${page}|${page_size}`;
    const cached = this._searchCache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
      // Return cached data in paginated format
      return {
        items: cached.data,
        pagination: {
          page,
          page_size,
          total_count: cached.data.length,
          total_pages: 1
        }
      };
    }

    const response = await api.get<PaginatedResponse<Product>>("/inventory/products/search", {
      params: { query, page, page_size },
      signal
    });

    this._searchCache.set(key, { data: response.data.items, timestamp: Date.now() });

    // Evict oldest entries (by timestamp) to prevent memory growth
    if (this._searchCache.size > 50) {
      let oldestKey: string | undefined;
      let oldestTs = Infinity;
      for (const [k, v] of this._searchCache) {
        if (v.timestamp < oldestTs) {
          oldestTs = v.timestamp;
          oldestKey = k;
        }
      }
      if (oldestKey !== undefined) this._searchCache.delete(oldestKey);
    }

    return response.data;
  }

  async getProduct(id: number): Promise<Product> {
    const response = await api.get<Product>(`/inventory/products/${id}`);
    return response.data;
  }

  async createProduct(product: ProductCreate): Promise<Product> {
    const response = await api.post<Product>("/inventory/products", product);
    this._invalidate();
    return response.data;
  }

  async updateProduct(id: number, product: ProductUpdate): Promise<Product> {
    const response = await api.put<Product>(`/inventory/products/${id}`, product);
    this._invalidate();
    return response.data;
  }

  async deleteProduct(id: number): Promise<void> {
    await api.delete(`/inventory/products/${id}`);
    this._invalidate();
  }
}

export const inventoryService = new InventoryService();
export default inventoryService;
