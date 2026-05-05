import React, { useState, useEffect } from 'react';
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

const ProductForm: React.FC<ProductFormProps> = ({
  isOpen,
  onClose,
  product,
  categories,
  onSuccess
}) => {
  const branding = useBranding();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    barcode: '',
    category_id: '',
    cost_price: 0,
    selling_price: 0,
    stock_quantity: 0,
    low_stock_threshold: 5,
    is_active: true
  });

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        barcode: product.barcode,
        category_id: product.category_id?.toString() || '',
        cost_price: Number(product.cost_price) || 0,
        selling_price: Number(product.selling_price),
        stock_quantity: product.stock_quantity,
        low_stock_threshold: product.low_stock_threshold,
        is_active: product.is_active
      });
    } else {
      setFormData({
        name: '',
        barcode: '',
        category_id: '',
        cost_price: 0,
        selling_price: 0,
        stock_quantity: 0,
        low_stock_threshold: 5,
        is_active: true
      });
    }
  }, [product, isOpen]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              type === 'number' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const payload = {
        ...formData,
        category_id: formData.category_id ? parseInt(formData.category_id) : undefined
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
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-探索-md overflow-y-auto max-h-[90vh]">
        <DialogHeader>
          <DialogTitle>{product ? 'Edit Product' : 'Add New Product'}</DialogTitle>
          <DialogDescription>
            Enter the details for your product below. Click save when you're done.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2 space-y-2">
              <Label htmlFor="name">Product Name</Label>
              <Input 
                id="name" 
                name="name" 
                value={formData.name} 
                onChange={handleChange} 
                required 
                placeholder="e.g. Wireless Mouse"
              />
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="barcode">Barcode / SKU</Label>
              <Input 
                id="barcode" 
                name="barcode" 
                value={formData.barcode} 
                onChange={handleChange} 
                required 
                placeholder="Unique identifier"
              />
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="category_id">Category</Label>
              <Select 
                value={formData.category_id} 
                onValueChange={(val) => setFormData(prev => ({ ...prev, category_id: val }))}
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
                name="cost_price" 
                type="number" 
                step="0.01"
                value={formData.cost_price} 
                onChange={handleChange} 
                required 
              />
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="selling_price">Selling Price ({branding.currency})</Label>
              <Input 
                id="selling_price" 
                name="selling_price" 
                type="number" 
                step="0.01"
                value={formData.selling_price} 
                onChange={handleChange} 
                required 
              />
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="stock_quantity">Current Stock</Label>
              <Input 
                id="stock_quantity" 
                name="stock_quantity" 
                type="number" 
                value={formData.stock_quantity} 
                onChange={handleChange} 
                required 
              />
            </div>

            <div className="col-span-1 space-y-2">
              <Label htmlFor="low_stock_threshold">Low Stock Alert at</Label>
              <Input 
                id="low_stock_threshold" 
                name="low_stock_threshold" 
                type="number" 
                value={formData.low_stock_threshold} 
                onChange={handleChange} 
                required 
              />
            </div>
            
            <div className="col-span-2 flex items-center space-x-2 pt-2">
              <input 
                id="is_active" 
                name="is_active" 
                type="checkbox" 
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={formData.is_active} 
                onChange={handleChange} 
              />
              <Label htmlFor="is_active" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
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
