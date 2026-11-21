import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  inventoryService,
  type Product,
  type Category,
  type ProductCreate,
  type ProductUpdate
} from '@/services/inventory.service';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';
import { useBranding } from '@/hooks/useBranding';

interface ProductFormProps {
  isOpen: boolean;
  onClose: () => void;
  product?: Product;
  categories: Category[];
  onSuccess: () => void;
}

const productSchema = z.object({
  name: z.string().min(1, 'Product name is required'),
  barcode: z.string().min(1, 'Barcode / SKU is required'),
  category_id: z.string().optional(),
  cost_price: z.coerce.number().min(0, 'Cost price cannot be negative'),
  selling_price: z.coerce.number().min(0.01, 'Selling price must be greater than 0'),
  stock_quantity: z.coerce.number().int('Stock must be a whole number').min(0, 'Stock cannot be negative'),
  low_stock_threshold: z.coerce.number().int('Must be a whole number').min(0, 'Cannot be negative'),
  is_active: z.boolean(),
});

type ProductFormInput = z.input<typeof productSchema>;
type ProductFormOutput = z.output<typeof productSchema>;

const emptyDefaults: ProductFormInput = {
  name: '',
  barcode: '',
  category_id: '',
  cost_price: 0,
  selling_price: 0,
  stock_quantity: 0,
  low_stock_threshold: 5,
  is_active: true,
};

const ProductForm: React.FC<ProductFormProps> = ({
  isOpen,
  onClose,
  product,
  categories,
  onSuccess
}) => {
  const branding = useBranding();

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProductFormInput, any, ProductFormOutput>({
    resolver: zodResolver(productSchema),
    defaultValues: emptyDefaults,
  });

  useEffect(() => {
    if (product) {
      reset({
        name: product.name,
        barcode: product.barcode,
        category_id: product.category_id?.toString() || '',
        cost_price: Number(product.cost_price) || 0,
        selling_price: Number(product.selling_price),
        stock_quantity: product.stock_quantity,
        low_stock_threshold: product.low_stock_threshold,
        is_active: product.is_active,
      });
    } else {
      reset(emptyDefaults);
    }
  }, [product, isOpen, reset]);

  const onSubmit = async (values: ProductFormOutput) => {
    try {
      const payload = {
        ...values,
        category_id: values.category_id ? parseInt(values.category_id) : undefined,
      };

      if (product) {
        await inventoryService.updateProduct(product.id, payload as ProductUpdate);
        toast.success('Product updated successfully');
      } else {
        await inventoryService.createProduct(payload as ProductCreate);
        toast.success('Product created successfully');
      }
      onSuccess();
    } catch (error: any) {
      console.error('Failed to save product:', error);
      const detail = error.response?.data?.detail;
      toast.error(detail || 'Failed to save product. Barcode might already exist.');
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md overflow-y-auto max-h-[90vh]">
        <DialogHeader>
          <DialogTitle>{product ? 'Edit Product' : 'Add New Product'}</DialogTitle>
          <DialogDescription>
            Enter the details for your product below. Click save when you're done.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2 space-y-2">
              <Label htmlFor="name">Product Name</Label>
              <Input
                id="name"
                {...register('name')}
                placeholder="e.g. Wireless Mouse"
                aria-invalid={!!errors.name}
              />
              {errors.name && <p className="text-xs text-destructive">{errors.name.message}</p>}
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="barcode">Barcode / SKU</Label>
              <Input
                id="barcode"
                {...register('barcode')}
                placeholder="Unique identifier"
                aria-invalid={!!errors.barcode}
              />
              {errors.barcode && <p className="text-xs text-destructive">{errors.barcode.message}</p>}
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="category_id">Category</Label>
              <Select
                value={watch('category_id')}
                onValueChange={(val) => setValue('category_id', val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(cat => (
                    <SelectItem key={cat.id} value={cat.id.toString()}>
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="cost_price">Cost Price ({branding.currency})</Label>
              <Input
                id="cost_price"
                type="number"
                step="0.01"
                {...register('cost_price')}
                aria-invalid={!!errors.cost_price}
              />
              {errors.cost_price && <p className="text-xs text-destructive">{errors.cost_price.message}</p>}
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="selling_price">Selling Price ({branding.currency})</Label>
              <Input
                id="selling_price"
                type="number"
                step="0.01"
                {...register('selling_price')}
                aria-invalid={!!errors.selling_price}
              />
              {errors.selling_price && <p className="text-xs text-destructive">{errors.selling_price.message}</p>}
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="stock_quantity">Current Stock</Label>
              <Input
                id="stock_quantity"
                type="number"
                {...register('stock_quantity')}
                aria-invalid={!!errors.stock_quantity}
              />
              {errors.stock_quantity && <p className="text-xs text-destructive">{errors.stock_quantity.message}</p>}
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="low_stock_threshold">Low Stock Alert at</Label>
              <Input
                id="low_stock_threshold"
                type="number"
                {...register('low_stock_threshold')}
                aria-invalid={!!errors.low_stock_threshold}
              />
              {errors.low_stock_threshold && (
                <p className="text-xs text-destructive">{errors.low_stock_threshold.message}</p>
              )}
            </div>

            <div className="col-span-2 flex items-center space-x-2 pt-2">
              <input
                id="is_active"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={watch('is_active')}
                onChange={(e) => setValue('is_active', e.target.checked)}
              />
              <Label htmlFor="is_active" className="text-sm font-medium leading-none">
                Product is active and available for sale
              </Label>
            </div>
          </div>

          <DialogFooter className="pt-4">
            <Button type="button" variant="outline" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {product ? 'Update Product' : 'Create Product'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default ProductForm;
