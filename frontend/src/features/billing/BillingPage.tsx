import React, { useState, useEffect, useRef } from "react";
import { 
  Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter 
} from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from "../../components/ui/table";
import { Separator } from "../../components/ui/separator";
import { Badge } from "../../components/ui/badge";
import { toast } from "sonner";
import { 
  Search, Plus, Minus, Trash2, User, CreditCard, Banknote, 
  Smartphone, Receipt, X, CheckCircle2 
} from "lucide-react";

import { useCalculator } from "./useCalculator";
import { billingService, type Customer, type Sale } from "../../services/billing.service";
import { inventoryService, type Product } from "../../services/inventory.service";
import { InvoiceTemplate } from "./InvoiceTemplate";

export const BillingPage: React.FC = () => {
  const { 
    items, addItem, removeItem, updateQuantity, clearCart,
    subtotal, taxAmount, discount, setDiscount, total, 
    taxRate, currency 
  } = useCalculator();

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  // const [isSearching, setIsSearching] = useState(false);

  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [customerSearch, setCustomerSearch] = useState("");
  
  const [paymentMethod, setPaymentMethod] = useState<"cash" | "card" | "transfer" | "credit">("cash");
  const [isProcessing, setIsProcessing] = useState(false);
  const [completedSale, setCompletedSale] = useState<Sale | null>(null);

  const searchInputRef = useRef<HTMLInputElement>(null);

  // Focus search input on load
  useEffect(() => {
    searchInputRef.current?.focus();
  }, []);

  // Product search
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (searchQuery.length >= 2) {
        // setIsSearching(true);
        try {
          const results = await inventoryService.searchProducts(searchQuery);
          setSearchResults(results);
        } catch (error) {
          console.error("Search error:", error);
        } finally {
          // setIsSearching(false);
        }
      } else {
        setSearchResults([]);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Customer search
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (customerSearch.length >= 2) {
        try {
          const results = await billingService.getCustomers(customerSearch);
          setCustomers(results);
        } catch (error) {
          console.error("Customer search error:", error);
        }
      } else {
        setCustomers([]);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [customerSearch]);

  const handleAddToCart = (product: Product) => {
    if (product.stock_quantity <= 0) {
      toast.error(`Out of stock: ${product.name}`);
      return;
    }
    addItem({
      id: product.id,
      name: product.name,
      price: product.selling_price,
      quantity: 1
    });
    setSearchQuery("");
    setSearchResults([]);
    searchInputRef.current?.focus();
  };

  const handleCompleteSale = async () => {
    if (items.length === 0) {
      toast.error("Cart is empty");
      return;
    }

    setIsProcessing(true);
    try {
      const sale = await billingService.createSale({
        customer_id: selectedCustomer?.id,
        items: items.map(i => ({ product_id: i.id, quantity: i.quantity })),
        payment_method: paymentMethod,
        discount_amount: discount
      });
      
      setCompletedSale(sale);
      toast.success("Sale completed successfully!");
      clearCart();
      setSelectedCustomer(null);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to process sale");
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (completedSale) {
    return (
      <div className="container mx-auto py-6 max-w-4xl space-y-6">
        <Card className="print:hidden">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-4">
              <CheckCircle2 size={32} />
            </div>
            <CardTitle className="text-2xl">Sale Completed!</CardTitle>
            <CardDescription>Invoice #{completedSale.id} has been generated.</CardDescription>
          </CardHeader>
          <CardFooter className="flex justify-center gap-4">
            <Button variant="outline" onClick={() => setCompletedSale(null)}>
              New Sale
            </Button>
            <Button onClick={handlePrint}>
              <Receipt className="mr-2 h-4 w-4" /> Print Invoice
            </Button>
          </CardFooter>
        </Card>

        {/* Printable Section */}
        <div className="bg-white p-8 border rounded-lg shadow-sm">
           <InvoiceTemplate sale={completedSale} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] overflow-hidden">
      <div className="flex-1 flex overflow-hidden p-6 gap-6">
        
        {/* Left Side: Product Search and Cart */}
        <div className="flex-1 flex flex-col gap-6 overflow-hidden">
          {/* Search Bar */}
          <Card className="shrink-0 border-primary/20 bg-primary/5">
            <CardContent className="p-4 relative">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  ref={searchInputRef}
                  placeholder="Search products by name or barcode... (Alt+S)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 h-12 text-lg"
                />
              </div>

              {/* Search Results Dropdown */}
              {searchResults.length > 0 && (
                <Card className="absolute left-4 right-4 top-full mt-1 z-50 shadow-xl border-primary/20 max-h-96 overflow-auto">
                  <div className="p-2 space-y-1">
                    {searchResults.map((product) => (
                      <button
                        key={product.id}
                        className="w-full flex items-center justify-between p-3 hover:bg-primary/10 rounded-md transition-colors text-left"
                        onClick={() => handleAddToCart(product)}
                      >
                        <div>
                          <p className="font-medium">{product.name}</p>
                          <p className="text-xs text-muted-foreground">{product.barcode}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-primary">{currency} {product.selling_price.toFixed(2)}</p>
                          <p className={`text-xs ${product.stock_quantity <= product.low_stock_threshold ? 'text-orange-500 font-medium' : 'text-muted-foreground'}`}>
                            Stock: {product.stock_quantity}
                          </p>
                        </div>
                      </button>
                    ))}
                  </div>
                </Card>
              )}
            </CardContent>
          </Card>

          {/* Cart Table */}
          <Card className="flex-1 overflow-hidden flex flex-col">
            <CardHeader className="py-4">
              <div className="flex justify-between items-center">
                <CardTitle className="text-lg">Current Sale Items</CardTitle>
                <Badge variant="outline">{items.length} Items</Badge>
              </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-auto p-0">
              <Table>
                <TableHeader className="sticky top-0 bg-background z-10">
                  <TableRow>
                    <TableHead>Product</TableHead>
                    <TableHead className="w-32 text-center">Quantity</TableHead>
                    <TableHead className="text-right">Price</TableHead>
                    <TableHead className="text-right">Subtotal</TableHead>
                    <TableHead className="w-12"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {items.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="h-64 text-center text-muted-foreground">
                        <div className="flex flex-col items-center gap-2">
                          <Receipt size={48} className="opacity-20" />
                          <p>Cart is empty. Search products to add.</p>
                        </div>
                      </TableCell>
                    </TableRow>
                  ) : (
                    items.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>
                          <p className="font-medium">{item.name}</p>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center justify-center gap-2">
                            <Button 
                              variant="outline" 
                              size="icon" 
                              className="h-8 w-8"
                              onClick={() => updateQuantity(item.id, item.quantity - 1)}
                            >
                              <Minus className="h-3 w-3" />
                            </Button>
                            <span className="w-8 text-center font-medium">{item.quantity}</span>
                            <Button 
                              variant="outline" 
                              size="icon" 
                              className="h-8 w-8"
                              onClick={() => updateQuantity(item.id, item.quantity + 1)}
                            >
                              <Plus className="h-3 w-3" />
                            </Button>
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          {currency} {item.price.toFixed(2)}
                        </TableCell>
                        <TableCell className="text-right font-medium">
                          {currency} {(item.price * item.quantity).toFixed(2)}
                        </TableCell>
                        <TableCell>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="text-destructive h-8 w-8"
                            onClick={() => removeItem(item.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        {/* Right Side: Checkout Details */}
        <div className="w-96 flex flex-col gap-6 shrink-0">
          {/* Customer Selection */}
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-md flex items-center gap-2">
                <User size={18} /> Customer Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {!selectedCustomer ? (
                <div className="relative">
                  <Input 
                    placeholder="Search/Add customer..." 
                    value={customerSearch}
                    onChange={(e) => setCustomerSearch(e.target.value)}
                  />
                  {customers.length > 0 && (
                    <div className="absolute left-0 right-0 top-full mt-1 bg-popover border rounded-md shadow-lg z-50 overflow-hidden">
                      {customers.map(c => (
                        <button
                          key={c.id}
                          className="w-full p-2 text-left hover:bg-accent text-sm"
                          onClick={() => {
                            setSelectedCustomer(c);
                            setCustomers([]);
                            setCustomerSearch("");
                          }}
                        >
                          <p className="font-medium">{c.name}</p>
                          <p className="text-xs text-muted-foreground">{c.phone || 'No phone'}</p>
                        </button>
                      ))}
                    </div>
                  )}
                  {customerSearch.length > 2 && customers.length === 0 && (
                    <Button 
                      variant="outline" 
                      className="w-full mt-2" 
                      onClick={async () => {
                        try {
                          const newCust = await billingService.createCustomer({ name: customerSearch });
                          setSelectedCustomer(newCust);
                          setCustomerSearch("");
                        } catch (e) {
                          toast.error("Failed to add customer");
                        }
                      }}
                    >
                      <Plus className="mr-2 h-4 w-4" /> Add "{customerSearch}"
                    </Button>
                  )}
                </div>
              ) : (
                <div className="flex items-center justify-between bg-primary/5 p-3 rounded-md border border-primary/20">
                  <div>
                    <p className="font-medium text-sm">{selectedCustomer.name}</p>
                    <p className="text-xs text-muted-foreground">{selectedCustomer.phone}</p>
                  </div>
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-8 w-8" 
                    onClick={() => setSelectedCustomer(null)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Payment and Totals */}
          <Card className="flex-1 flex flex-col">
            <CardHeader className="py-4">
              <CardTitle className="text-md">Payment & Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1">
              <div className="space-y-2">
                <label className="text-xs font-medium text-muted-foreground uppercase">Payment Method</label>
                <div className="grid grid-cols-2 gap-2">
                  <Button 
                    variant={paymentMethod === "cash" ? "default" : "outline"} 
                    className="justify-start"
                    onClick={() => setPaymentMethod("cash")}
                  >
                    <Banknote className="mr-2 h-4 w-4" /> Cash
                  </Button>
                  <Button 
                    variant={paymentMethod === "card" ? "default" : "outline"}
                    className="justify-start"
                    onClick={() => setPaymentMethod("card")}
                  >
                    <CreditCard className="mr-2 h-4 w-4" /> Card
                  </Button>
                  <Button 
                    variant={paymentMethod === "transfer" ? "default" : "outline"}
                    className="justify-start"
                    onClick={() => setPaymentMethod("transfer")}
                  >
                    <Smartphone className="mr-2 h-4 w-4" /> Transfer
                  </Button>
                  <Button 
                    variant={paymentMethod === "credit" ? "default" : "outline"}
                    className="justify-start"
                    onClick={() => setPaymentMethod("credit")}
                  >
                    <User className="mr-2 h-4 w-4" /> Credit
                  </Button>
                </div>
              </div>

              <Separator />

              <div className="space-y-3 pt-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Subtotal</span>
                  <span>{currency} {subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Tax ({taxRate}%)</span>
                  <span>{currency} {taxAmount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Discount</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">{currency}</span>
                    <Input 
                      type="number" 
                      className="h-8 w-24 text-right" 
                      value={discount}
                      onChange={(e) => setDiscount(Number(e.target.value))}
                    />
                  </div>
                </div>
                <Separator className="my-2" />
                <div className="flex justify-between items-center">
                  <span className="text-lg font-bold">Total</span>
                  <span className="text-2xl font-bold text-primary">
                    {currency} {total.toFixed(2)}
                  </span>
                </div>
              </div>
            </CardContent>
            <CardFooter className="p-4 pt-0">
              <Button 
                className="w-full h-14 text-lg font-bold" 
                size="lg"
                disabled={items.length === 0 || isProcessing}
                onClick={handleCompleteSale}
              >
                {isProcessing ? "Processing..." : "Complete Sale"}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
};
