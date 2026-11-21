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
  Smartphone, Receipt, X, CheckCircle2, PauseCircle, History
} from "lucide-react";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription
} from "../../components/ui/dialog";

import { useCalculator, type CartItem } from "./useCalculator";
import { billingService, type Customer, type Sale } from "../../services/billing.service";
import { inventoryService, type Product } from "../../services/inventory.service";
import { InvoiceTemplate } from "./InvoiceTemplate";

const HELD_SALES_STORAGE_KEY = "mbas_held_sales";

interface HeldSale {
  holdId: string;
  heldAt: number;
  items: CartItem[];
  discount: number;
  customer: Customer | null;
  paymentMethod: "cash" | "card" | "transfer" | "credit";
}

const BillingPage: React.FC = () => {
  const {
    items, addItem, removeItem, updateQuantity, clearCart, loadCart,
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
  const [cashTendered, setCashTendered] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [completedSale, setCompletedSale] = useState<Sale | null>(null);

  const [heldSales, setHeldSales] = useState<HeldSale[]>(() => {
    try {
      const raw = localStorage.getItem(HELD_SALES_STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  });
  const [isHeldDialogOpen, setIsHeldDialogOpen] = useState(false);

  useEffect(() => {
    localStorage.setItem(HELD_SALES_STORAGE_KEY, JSON.stringify(heldSales));
  }, [heldSales]);

  const tenderedAmount = parseFloat(cashTendered) || 0;
  const changeDue = tenderedAmount - total;
  // Cash tendered is only a convenience for calculating change - it's optional.
  // Only block checkout when the cashier has actually typed an amount that's
  // short of the total; an empty field must never block "Complete Sale".
  const cashInsufficient = paymentMethod === "cash" && items.length > 0 && cashTendered !== "" && tenderedAmount < total;

  const searchInputRef = useRef<HTMLInputElement>(null);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  // Focus search input on load
  useEffect(() => {
    searchInputRef.current?.focus();
  }, []);

  // Abort controller for cancelling search on unmount/new search
  const searchAbortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => { searchAbortRef.current?.abort(); };
  }, []);

  // Product search - works for both barcode scanner and manual typing
  useEffect(() => {
    if (searchQuery.length < 1) {
      setSearchResults([]);
      setSelectedIndex(-1);
      return;
    }

    const timer = setTimeout(async () => {
      searchAbortRef.current?.abort();
      const controller = new AbortController();
      searchAbortRef.current = controller;
      try {
        const response = await inventoryService.searchProducts(searchQuery, 1, 20, controller.signal);
        if (controller.signal.aborted) return;
        setSearchResults(response.items);
        if (response.items.length === 1 && response.items[0].barcode === searchQuery) {
          setSelectedIndex(0);
        } else {
          setSelectedIndex(-1);
        }
      } catch (error: any) {
        if (controller.signal.aborted) return;
        console.error("Search error:", error);
      }
    }, 150); // Faster debounce for POS responsiveness

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Customer search with abort signal
  const customerAbortRef = useRef<AbortController | null>(null);
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (customerSearch.length >= 2) {
        customerAbortRef.current?.abort();
        const controller = new AbortController();
        customerAbortRef.current = controller;
        try {
          const results = await billingService.getCustomers(customerSearch);
          if (controller.signal.aborted) return;
          setCustomers(results);
        } catch (error: any) {
          if (controller.signal.aborted) return;
          console.error("Customer search error:", error);
        }
      } else {
        setCustomers([]);
      }
    }, 300);

    return () => { clearTimeout(timer); customerAbortRef.current?.abort(); };
  }, [customerSearch]);

  const handleAddToCart = (product: Product) => {
    if (product.stock_quantity <= 0) {
      toast.error(`Out of stock: ${product.name}`);
      return;
    }
    addItem({
      id: product.id,
      name: product.name,
      price: typeof product.selling_price === 'string' ? parseFloat(product.selling_price) : product.selling_price,
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
    if (cashInsufficient) {
      toast.error("Cash received is less than the total due");
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
      setCashTendered("");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to process sale");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleHoldSale = () => {
    if (items.length === 0) {
      toast.error("Cart is empty");
      return;
    }
    const held: HeldSale = {
      holdId: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      heldAt: Date.now(),
      items,
      discount,
      customer: selectedCustomer,
      paymentMethod,
    };
    setHeldSales((prev) => [held, ...prev]);
    loadCart([], 0);
    setSelectedCustomer(null);
    setPaymentMethod("cash");
    setCashTendered("");
    toast.success("Sale held — resume it anytime from \"Held Sales\"");
    searchInputRef.current?.focus();
  };

  const handleResumeSale = (holdId: string) => {
    if (items.length > 0) {
      toast.error("Complete or hold the current sale before resuming another one");
      return;
    }
    const held = heldSales.find((h) => h.holdId === holdId);
    if (!held) return;
    loadCart(held.items, held.discount);
    setSelectedCustomer(held.customer);
    setPaymentMethod(held.paymentMethod);
    setHeldSales((prev) => prev.filter((h) => h.holdId !== holdId));
    setIsHeldDialogOpen(false);
    toast.success("Sale resumed");
  };

  const handleDeleteHeldSale = (holdId: string) => {
    setHeldSales((prev) => prev.filter((h) => h.holdId !== holdId));
  };

  // Keyboard-first checkout: Ctrl/Cmd+Enter completes the sale from anywhere on the page.
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && !completedSale) {
        e.preventDefault();
        handleCompleteSale();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleCompleteSale, completedSale]);

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
            <p className="text-sm text-muted-foreground mt-2">
              Choose your preferred print format below
            </p>
          </CardHeader>
          <CardFooter className="flex justify-center gap-4">
            <Button variant="outline" onClick={() => setCompletedSale(null)}>
              New Sale
            </Button>
          </CardFooter>
        </Card>

        {/* Printable Section with Format Selector */}
        <div className="bg-white p-8 border rounded-lg shadow-sm">
           <InvoiceTemplate sale={completedSale} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
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
                  onKeyDown={(e) => {
                    if (e.key === "Escape") {
                      e.preventDefault();
                      setSearchResults([]);
                      setSelectedIndex(-1);
                      return;
                    }
                    if (searchResults.length === 0) return;
                    if (e.key === "ArrowDown") {
                      e.preventDefault();
                      setSelectedIndex((prev) =>
                        prev < searchResults.length - 1 ? prev + 1 : 0
                      );
                    } else if (e.key === "ArrowUp") {
                      e.preventDefault();
                      setSelectedIndex((prev) =>
                        prev > 0 ? prev - 1 : searchResults.length - 1
                      );
                    } else if (e.key === "Enter") {
                      e.preventDefault();
                      // Use selected index, or first item if none selected
                      const idx = selectedIndex >= 0 ? selectedIndex : 0;
                      if (searchResults[idx]) {
                        handleAddToCart(searchResults[idx]);
                      }
                    }
                  }}
                  className="pl-10 h-12 text-lg"
                />
              </div>

              {/* Search Results Dropdown */}
              {searchResults.length > 0 && (
                <Card className="absolute left-4 right-4 top-full mt-1 z-50 shadow-xl border-primary/20 max-h-96 overflow-auto">
                  <div className="p-2 space-y-1">
                    {searchResults.map((product, index) => (
                      <button
                        key={product.id}
                        ref={(el) => {
                          if (index === selectedIndex && el) {
                            el.scrollIntoView({ block: "nearest" });
                          }
                        }}
                        className={`w-full flex items-center justify-between p-3 rounded-md transition-colors text-left ${
                          index === selectedIndex
                            ? "bg-primary/20 ring-1 ring-primary/30"
                            : "hover:bg-primary/10"
                        }`}
                        onClick={() => handleAddToCart(product)}
                        onMouseEnter={() => setSelectedIndex(index)}
                      >
                        <div>
                          <p className="font-medium">{product.name}</p>
                          <p className="text-xs text-muted-foreground">{product.barcode}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-primary">{currency} {(typeof product.selling_price === 'string' ? parseFloat(product.selling_price) : product.selling_price).toFixed(2)}</p>
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
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleHoldSale}
                    disabled={items.length === 0 || isProcessing}
                  >
                    <PauseCircle className="mr-2 h-4 w-4" /> Hold Sale
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setIsHeldDialogOpen(true)}>
                    <History className="mr-2 h-4 w-4" /> Held Sales
                    {heldSales.length > 0 && (
                      <Badge variant="secondary" className="ml-2">{heldSales.length}</Badge>
                    )}
                  </Button>
                  <Badge variant="outline">{items.length} Items</Badge>
                </div>
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
        <div className="w-96 flex flex-col gap-6 shrink-0 overflow-y-auto">
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
          <Card className="flex-1 flex flex-col min-h-0">
            <CardHeader className="py-4 shrink-0">
              <CardTitle className="text-md">Payment & Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1 overflow-y-auto">
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
                    onClick={() => { setPaymentMethod("card"); setCashTendered(""); }}
                  >
                    <CreditCard className="mr-2 h-4 w-4" /> Card
                  </Button>
                  <Button
                    variant={paymentMethod === "transfer" ? "default" : "outline"}
                    className="justify-start"
                    onClick={() => { setPaymentMethod("transfer"); setCashTendered(""); }}
                  >
                    <Smartphone className="mr-2 h-4 w-4" /> Transfer
                  </Button>
                  <Button
                    variant={paymentMethod === "credit" ? "default" : "outline"}
                    className="justify-start"
                    onClick={() => { setPaymentMethod("credit"); setCashTendered(""); }}
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

                {paymentMethod === "cash" && (
                  <div className="space-y-2 pt-1">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">Cash Received</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted-foreground">{currency}</span>
                        <Input
                          type="number"
                          className="h-8 w-24 text-right"
                          value={cashTendered}
                          onChange={(e) => setCashTendered(e.target.value)}
                          placeholder="0.00"
                        />
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-sm font-medium">
                      <span className={cashInsufficient ? "text-destructive" : "text-muted-foreground"}>
                        {cashInsufficient ? "Amount Due" : "Change Due"}
                      </span>
                      <span className={cashInsufficient ? "text-destructive" : "text-emerald-600"}>
                        {currency} {Math.abs(changeDue).toFixed(2)}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
            <CardFooter className="p-4 pt-0 shrink-0 border-t bg-background">
              <Button
                className="w-full h-14 text-lg font-bold"
                size="lg"
                disabled={items.length === 0 || isProcessing || cashInsufficient}
                onClick={handleCompleteSale}
                title="Ctrl+Enter to complete sale"
              >
                {isProcessing ? "Processing..." : "Complete Sale"}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>

      <Dialog open={isHeldDialogOpen} onOpenChange={setIsHeldDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Held Sales</DialogTitle>
            <DialogDescription>
              Resume a parked sale to continue checkout, or remove it.
            </DialogDescription>
          </DialogHeader>
          <div className="max-h-96 overflow-y-auto space-y-2">
            {heldSales.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">
                No held sales.
              </p>
            ) : (
              heldSales.map((h) => {
                const heldSubtotal = h.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
                return (
                  <div key={h.holdId} className="flex items-center justify-between p-3 border rounded-md">
                    <div>
                      <p className="font-medium text-sm">{h.customer?.name || "Walk-in"}</p>
                      <p className="text-xs text-muted-foreground">
                        {h.items.length} item{h.items.length !== 1 ? "s" : ""} · {currency} {heldSubtotal.toFixed(2)} · held {new Date(h.heldAt).toLocaleTimeString()}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button size="sm" onClick={() => handleResumeSale(h.holdId)}>Resume</Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        className="text-destructive h-8 w-8"
                        onClick={() => handleDeleteHeldSale(h.holdId)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export { BillingPage };
export default BillingPage;
