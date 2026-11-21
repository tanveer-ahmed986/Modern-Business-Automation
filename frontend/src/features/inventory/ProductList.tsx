import React, { useState, useMemo } from 'react';
import {
  Plus,
  Search,
  MoreHorizontal,
  Edit,
  Trash2,
  AlertTriangle,
  RefreshCcw,
  Loader2,
  Settings2
} from 'lucide-react';
import type { ColumnDef } from "@tanstack/react-table";
import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { DataTable } from "@/components/ui/data-table";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import {
  inventoryService,
  type Product,
} from '@/services/inventory.service';
import authService from '@/services/auth.service';
import { toast } from 'sonner';
import { useBranding } from '@/hooks/useBranding';
import { useDebounce } from '@/hooks/useDebounce';

import ProductForm from './ProductForm';

const PAGE_SIZE_OPTIONS = [25, 50, 100];

const ProductList: React.FC = () => {
  const branding = useBranding();
  const queryClient = useQueryClient();

  // Server-side pagination + filter state
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [categoryId, setCategoryId] = useState<number | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedSearchQuery = useDebounce(searchQuery, 400);
  const isSearching = debouncedSearchQuery.trim().length > 0;

  // Modal state
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | undefined>(undefined);
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState('');

  const currentUser = authService.getCurrentUser();
  const isAdminOrManager = currentUser?.role === 'admin' || currentUser?.role === 'manager';

  // --- Queries (TanStack Query replaces the old service-level TTL caches) ---
  const categoriesQuery = useQuery({
    queryKey: ['categories'],
    queryFn: ({ signal }) => inventoryService.getCategories(signal),
  });

  const productsQuery = useQuery({
    queryKey: ['products', { page, pageSize, categoryId }],
    queryFn: ({ signal }) =>
      inventoryService.getProducts({ page, page_size: pageSize, category_id: categoryId }, signal),
    placeholderData: keepPreviousData, // table stays filled while paging
    enabled: !isSearching,
  });

  const searchResultsQuery = useQuery({
    queryKey: ['product-search', debouncedSearchQuery],
    // Inventory management view: include deactivated products in search
    queryFn: ({ signal }) =>
      inventoryService.searchProducts(debouncedSearchQuery, 1, 50, signal, true),
    enabled: isSearching,
  });

  const activeQuery = isSearching ? searchResultsQuery : productsQuery;
  const products = activeQuery.data?.items ?? [];
  const pagination = productsQuery.data?.pagination;
  const totalPages = pagination?.total_pages ?? 1;

  const invalidateProducts = () => {
    queryClient.invalidateQueries({ queryKey: ['products'] });
    queryClient.invalidateQueries({ queryKey: ['product-search'] });
  };

  // --- Mutations ---
  const deleteProductMutation = useMutation({
    mutationFn: (id: number) => inventoryService.deleteProduct(id),
    onSuccess: (result) => {
      toast.success(
        result.soft_deleted
          ? 'Product has sales history — deactivated instead of deleted'
          : 'Product deleted successfully'
      );
      invalidateProducts();
    },
    onError: () => toast.error('Failed to delete product'),
  });

  const addCategoryMutation = useMutation({
    mutationFn: (name: string) => inventoryService.createCategory(name),
    onSuccess: () => {
      setNewCategoryName('');
      toast.success('Category created');
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
    onError: () => toast.error('Failed to create category'),
  });

  const deleteCategoryMutation = useMutation({
    mutationFn: (id: number) => inventoryService.deleteCategory(id),
    onSuccess: (_data, id) => {
      toast.success('Category deleted');
      if (categoryId === id) setCategoryId(undefined);
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
    onError: (error: any) =>
      toast.error(error.response?.data?.detail || 'Failed to delete category'),
  });

  const [deleteTarget, setDeleteTarget] = useState<Product | undefined>(undefined);

  const confirmDelete = () => {
    if (deleteTarget) deleteProductMutation.mutate(deleteTarget.id);
    setDeleteTarget(undefined);
  };

  const categories = categoriesQuery.data ?? [];

  const columns: ColumnDef<Product>[] = useMemo(() => [
    {
      accessorKey: "barcode",
      header: "Barcode",
      cell: ({ row }) => <span className="font-mono text-xs">{row.getValue("barcode")}</span>,
    },
    {
      accessorKey: "name",
      header: "Product Name",
      cell: ({ row }) => (
        <div className="flex flex-col">
          <span className="font-medium">{row.getValue("name")}</span>
          <span className="text-xs text-muted-foreground">{row.original.category?.name || 'No Category'}</span>
        </div>
      ),
    },
    {
      accessorKey: "stock_quantity",
      header: "Stock",
      cell: ({ row }) => {
        const stock = row.getValue("stock_quantity") as number;
        const threshold = row.original.low_stock_threshold;
        const isLow = stock <= threshold;

        return (
          <div className="flex items-center">
            <span className={isLow ? "text-red-600 font-bold" : ""}>{stock}</span>
            {isLow && (
              <span title="Low stock alert">
                <AlertTriangle className="ml-2 h-4 w-4 text-amber-500" />
              </span>
            )}
          </div>
        )
      },
    },
    {
      accessorKey: "selling_price",
      header: "Selling Price",
      cell: ({ row }) => {
        const amount = parseFloat(row.getValue("selling_price"));
        return <div className="font-medium">{branding.currency} {amount.toFixed(2)}</div>;
      },
    },
    ...(isAdminOrManager ? [{
      accessorKey: "cost_price",
      header: "Cost Price",
      cell: ({ row }: { row: any }) => {
        const amount = parseFloat(row.getValue("cost_price") || 0);
        return <div className="text-muted-foreground">{branding.currency} {amount.toFixed(2)}</div>;
      },
    }] : []),
    {
      accessorKey: "is_active",
      header: "Status",
      cell: ({ row }) => {
        const isActive = row.getValue("is_active") as boolean;
        return (
          <Badge variant={isActive ? "default" : "secondary"}>
            {isActive ? "Active" : "Inactive"}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const product = row.original;

        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem onClick={() => navigator.clipboard.writeText(product.barcode)}>
                Copy barcode
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => {
                // Defer to the next tick: opening a Dialog synchronously from
                // a DropdownMenuItem races Radix's body pointer-events lock
                // between the closing menu and the opening dialog, leaving
                // the whole page unclickable (document.body stuck at
                // `pointer-events: none`) until the dropdown fully unmounts.
                setTimeout(() => {
                  setSelectedProduct(product);
                  setIsFormOpen(true);
                }, 0);
              }}>
                <Edit className="mr-2 h-4 w-4" />
                Edit Product
              </DropdownMenuItem>
              {isAdminOrManager && (
                <DropdownMenuItem
                  className="text-red-600 focus:text-red-600"
                  onClick={() => setTimeout(() => setDeleteTarget(product), 0)}
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Product
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ], [isAdminOrManager, branding.currency]);

  const isInitialLoading = activeQuery.isLoading && products.length === 0;
  const isRefreshing = activeQuery.isFetching && !activeQuery.isLoading;

  if (isInitialLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2 text-slate-500 font-medium">Loading inventory...</span>
      </div>
    );
  }

  if (activeQuery.isError && products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4">
        <AlertTriangle className="h-12 w-12 text-amber-500" />
        <p className="text-muted-foreground">Could not load inventory data.</p>
        <Button onClick={() => activeQuery.refetch()}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Inventory Management</h2>
          <p className="text-muted-foreground">Manage your products, categories, and track stock levels.</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon" onClick={() => activeQuery.refetch()} disabled={isRefreshing}>
            <RefreshCcw className={cn("h-4 w-4", isRefreshing && "animate-spin")} />
          </Button>
          <Button onClick={() => {
            setSelectedProduct(undefined);
            setIsFormOpen(true);
          }}>
            <Plus className="mr-2 h-4 w-4" />
            Add Product
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-1">
          <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
            <div>
              <CardTitle className="text-lg">Categories</CardTitle>
              <CardDescription>Filter inventory</CardDescription>
            </div>
            <Dialog open={isCategoryModalOpen} onOpenChange={setIsCategoryModalOpen}>
              <DialogTrigger asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <Settings2 className="h-4 w-4" />
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Manage Categories</DialogTitle>
                  <CardDescription>Add or remove product categories</CardDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="flex items-center gap-2">
                    <Input
                      placeholder="Category name..."
                      value={newCategoryName}
                      onChange={(e) => setNewCategoryName(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && newCategoryName.trim() && addCategoryMutation.mutate(newCategoryName.trim())}
                    />
                    <Button
                      onClick={() => newCategoryName.trim() && addCategoryMutation.mutate(newCategoryName.trim())}
                      disabled={addCategoryMutation.isPending}
                    >
                      Add
                    </Button>
                  </div>
                  <div className="max-h-[300px] overflow-y-auto space-y-2">
                    {categories.map(cat => (
                      <div key={cat.id} className="flex items-center justify-between p-2 rounded-md border">
                        <span>{cat.name}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 text-red-500 hover:text-red-700 hover:bg-red-50"
                          onClick={() => deleteCategoryMutation.mutate(cat.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <Button
                variant={categoryId === undefined ? "secondary" : "ghost"}
                className="w-full justify-start font-normal"
                onClick={() => { setCategoryId(undefined); setPage(1); }}
              >
                All Products
                {pagination && categoryId === undefined && (
                  <Badge variant="secondary" className="ml-auto">{pagination.total_count}</Badge>
                )}
              </Button>
              {categories.map(category => (
                <Button
                  key={category.id}
                  variant={categoryId === category.id ? "secondary" : "ghost"}
                  className="w-full justify-start font-normal"
                  onClick={() => { setCategoryId(category.id); setPage(1); setSearchQuery(''); }}
                >
                  {category.name}
                  {pagination && categoryId === category.id && (
                    <Badge variant="secondary" className="ml-auto">{pagination.total_count}</Badge>
                  )}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-lg font-bold">Product List</CardTitle>
                <CardDescription>
                  {isSearching
                    ? `${searchResultsQuery.data?.pagination.total_count ?? 0} search results`
                    : `${pagination?.total_count ?? 0} products`}
                </CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search name or barcode..."
                    className="pl-8 w-[200px] md:w-[250px] h-9"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <DataTable
              columns={columns}
              data={products}
              isLoading={activeQuery.isLoading}
              page={page}
              pageCount={isSearching ? 1 : totalPages}
              onPageChange={setPage}
              pageSize={isSearching ? undefined : pageSize}
              onPageSizeChange={isSearching ? undefined : (size) => { setPageSize(size); setPage(1); }}
              pageSizeOptions={PAGE_SIZE_OPTIONS}
              totalCount={isSearching ? searchResultsQuery.data?.pagination.total_count : pagination?.total_count}
              emptyTitle="No products found."
              emptyDescription={isSearching ? "Try a different search term." : "Add your first product to get started."}
            />
          </CardContent>
        </Card>
      </div>

      {isFormOpen && (
        <ProductForm
          isOpen={isFormOpen}
          onClose={() => setIsFormOpen(false)}
          product={selectedProduct}
          categories={categories}
          onSuccess={() => {
            setIsFormOpen(false);
            invalidateProducts();
          }}
        />
      )}

      <AlertDialog open={!!deleteTarget} onOpenChange={(open) => !open && setDeleteTarget(undefined)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete "{deleteTarget?.name}"?</AlertDialogTitle>
            <AlertDialogDescription>
              If this product has sales history it will be deactivated instead of deleted.
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default ProductList;
