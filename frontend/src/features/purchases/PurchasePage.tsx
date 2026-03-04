import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { 
  Trash2, 
  Search, 
  ArrowLeft, 
  ShoppingCart, 
  Save,
  User
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import suppliersService from "@/services/suppliers.service";
import type { Supplier } from "@/services/suppliers.service";
import inventoryService from "@/services/inventory.service";
import type { Product } from "@/services/inventory.service";
import purchasesService from "@/services/purchases.service";
import type { PurchaseCreate } from "@/services/purchases.service";
import { toast } from "sonner";

interface CartItem {
  product: Product;
  quantity: number;
  cost_price: number;
}

export default function PurchasePage() {
  const navigate = useNavigate();
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [selectedSupplierId, setSelectedSupplierId] = useState<string>("");
  const [referenceNumber, setReferenceNumber] = useState("");
  const [notes, setNotes] = useState("");
  const [taxAmount, setTaxAmount] = useState(0);
  const [discountAmount, setDiscountAmount] = useState(0);
  const [paidAmount, setPaidAmount] = useState(0);

  // Product Search State
  const [productSearch, setProductSearch] = useState("");
  const [searchResults, setSearchResults] = useState<Product[]>([]);

  // Cart State
  const [cart, setCart] = useState<CartItem[]>([]);

  useEffect(() => {
    loadSuppliers();
  }, []);

  const loadSuppliers = async () => {
    try {
      const data = await suppliersService.getSuppliers();
      setSuppliers(data);
    } catch (error) {
      toast.error("Failed to load suppliers");
    }
  };

  const handleProductSearch = async (query: string) => {
    setProductSearch(query);
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const results = await inventoryService.searchProducts(query);
      setSearchResults(results);
    } catch (error) {
      console.error("Search failed", error);
    }
  };

  const addToCart = (product: Product) => {
    const existing = cart.find((item) => item.product.id === product.id);
    if (existing) {
      setCart(
        cart.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setCart([...cart, { 
        product, 
        quantity: 1, 
        cost_price: product.cost_price || 0 
      }]);
    }
    setProductSearch("");
    setSearchResults([]);
  };

  const removeFromCart = (productId: number) => {
    setCart(cart.filter((item) => item.product.id !== productId));
  };

  const updateQuantity = (productId: number, quantity: number) => {
    if (quantity < 1) return;
    setCart(
      cart.map((item) =>
        item.product.id === productId ? { ...item, quantity } : item
      )
    );
  };

  const updateCostPrice = (productId: number, cost_price: number) => {
    if (cost_price < 0) return;
    setCart(
      cart.map((item) =>
        item.product.id === productId ? { ...item, cost_price } : item
      )
    );
  };

  const totalAmount = cart.reduce((sum, item) => sum + item.cost_price * item.quantity, 0);
  const grandTotal = totalAmount + taxAmount - discountAmount;

  const handleSubmit = async () => {
    if (cart.length === 0) {
      toast.error("Cart is empty");
      return;
    }

    try {
      const purchaseData: PurchaseCreate = {
        supplier_id: selectedSupplierId ? parseInt(selectedSupplierId) : undefined,
        reference_number: referenceNumber,
        items: cart.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
          cost_price: item.cost_price,
        })),
        tax_amount: taxAmount,
        discount_amount: discountAmount,
        paid_amount: paidAmount,
        notes: notes,
      };

      await purchasesService.createPurchase(purchaseData);
      toast.success("Purchase recorded successfully");
      navigate("/inventory"); // Redirect to inventory to see updated stock
    } catch (error) {
      toast.error("Failed to record purchase");
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold tracking-tight">New Purchase</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Form & Items */}
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <User className="h-5 w-5" /> Supplier Information
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Supplier</Label>
                <Select value={selectedSupplierId} onValueChange={setSelectedSupplierId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a supplier" />
                  </SelectTrigger>
                  <SelectContent>
                    {suppliers.map((s) => (
                      <SelectItem key={s.id} value={s.id.toString()}>
                        {s.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Reference Number</Label>
                <Input 
                  placeholder="e.g. INV-2024-001" 
                  value={referenceNumber}
                  onChange={(e) => setReferenceNumber(e.target.value)}
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <ShoppingCart className="h-5 w-5" /> Purchase Items
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search products by name or barcode..."
                  className="pl-10"
                  value={productSearch}
                  onChange={(e) => handleProductSearch(e.target.value)}
                />
                {searchResults.length > 0 && (
                  <div className="absolute z-10 w-full mt-1 bg-popover border rounded-md shadow-lg max-h-60 overflow-auto">
                    {searchResults.map((product) => (
                      <div
                        key={product.id}
                        className="p-3 hover:bg-accent cursor-pointer flex justify-between items-center border-b last:border-0"
                        onClick={() => addToCart(product)}
                      >
                        <div>
                          <div className="font-medium">{product.name}</div>
                          <div className="text-xs text-muted-foreground">{product.barcode}</div>
                        </div>
                        <div className="text-sm font-bold">
                          ${(product.cost_price || 0).toLocaleString()}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="border rounded-md overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Product</TableHead>
                      <TableHead className="w-24">Qty</TableHead>
                      <TableHead className="w-32">Cost Price</TableHead>
                      <TableHead className="w-32">Subtotal</TableHead>
                      <TableHead className="w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {cart.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                          No items added yet. Search products above.
                        </TableCell>
                      </TableRow>
                    ) : (
                      cart.map((item) => (
                        <TableRow key={item.product.id}>
                          <TableCell>
                            <div className="font-medium">{item.product.name}</div>
                            <div className="text-xs text-muted-foreground">{item.product.barcode}</div>
                          </TableCell>
                          <TableCell>
                            <Input
                              type="number"
                              min="1"
                              value={item.quantity}
                              onChange={(e) => updateQuantity(item.product.id, parseInt(e.target.value) || 0)}
                              className="h-8 px-2"
                            />
                          </TableCell>
                          <TableCell>
                            <Input
                              type="number"
                              step="0.01"
                              value={item.cost_price}
                              onChange={(e) => updateCostPrice(item.product.id, parseFloat(e.target.value) || 0)}
                              className="h-8 px-2"
                            />
                          </TableCell>
                          <TableCell className="font-medium">
                            ${(item.cost_price * item.quantity).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8 text-destructive"
                              onClick={() => removeFromCart(item.product.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Summary */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>${totalAmount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <Label>Tax Amount</Label>
                  <Input 
                    type="number" 
                    className="w-24 h-8 text-right" 
                    value={taxAmount}
                    onChange={(e) => setTaxAmount(parseFloat(e.target.value) || 0)}
                  />
                </div>
                <div className="flex justify-between items-center text-sm">
                  <Label>Discount</Label>
                  <Input 
                    type="number" 
                    className="w-24 h-8 text-right" 
                    value={discountAmount}
                    onChange={(e) => setDiscountAmount(parseFloat(e.target.value) || 0)}
                  />
                </div>
              </div>
              <div className="pt-4 border-t flex justify-between items-center font-bold text-lg">
                <span>Total</span>
                <span>${grandTotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="space-y-2 pt-4">
                <Label className="text-primary">Amount Paid</Label>
                <Input 
                  type="number" 
                  className="text-right text-lg font-bold" 
                  value={paidAmount}
                  onChange={(e) => setPaidAmount(parseFloat(e.target.value) || 0)}
                />
              </div>
              <div className="space-y-2 pt-2">
                <Label>Notes</Label>
                <textarea 
                  className="w-full min-h-[80px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Additional details..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button className="w-full gap-2 py-6 text-lg" onClick={handleSubmit}>
                <Save className="h-5 w-5" /> Record Purchase
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
