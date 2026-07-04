import { useState, useEffect, useRef } from "react";
import type { ChangeEvent, FormEvent } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Plus,
  Search,
  History,
  Edit,
  DollarSign,
  ArrowLeft,
  Building2,
  CheckCircle2,
} from "lucide-react";
import suppliersService from "@/services/suppliers.service";
import type { Supplier, SupplierLedgerData } from "@/services/suppliers.service";
import settingsService from "@/services/settings.service";
import type { Settings } from "@/services/settings.service";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";

export default function SupplierLedger() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);
  const [settings, setSettings] = useState<Settings | null>(null);

  // Payment dialog state
  const [isPaymentDialogOpen, setIsPaymentDialogOpen] = useState(false);
  const [paymentSupplierId, setPaymentSupplierId] = useState<number | null>(null);
  const [paymentAmount, setPaymentAmount] = useState(0);
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [paymentReference, setPaymentReference] = useState("");
  const [paymentNotes, setPaymentNotes] = useState("");
  const [isSubmittingPayment, setIsSubmittingPayment] = useState(false);

  // Ledger detail view state
  const [selectedSupplierLedger, setSelectedSupplierLedger] = useState<SupplierLedgerData | null>(null);
  const [isLedgerLoading, setIsLedgerLoading] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    name: "",
    contact_person: "",
    phone: "",
    email: "",
    address: "",
  });

  const currency = settings?.currency || "USD";
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    abortRef.current = controller;
    loadSuppliers(controller.signal);
    loadSettings();
    return () => { controller.abort(); ledgerAbortRef.current?.abort(); };
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsService.getSettings();
      setSettings(data);
    } catch (error) {
      console.error("Failed to load settings");
    }
  };

  const loadSuppliers = async (signal?: AbortSignal) => {
    try {
      setLoading(true);
      const data = await suppliersService.getSuppliers(signal);
      if (signal?.aborted) return;
      setSuppliers(data);
    } catch (error: any) {
      if (signal?.aborted) return;
      toast.error("Failed to load suppliers");
    } finally {
      if (!signal?.aborted) setLoading(false);
    }
  };

  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const filteredSuppliers = suppliers.filter(
    (s) =>
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (s.phone && s.phone.includes(searchQuery)) ||
      (s.contact_person && s.contact_person.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (editingSupplier) {
        await suppliersService.updateSupplier(editingSupplier.id, formData);
        toast.success("Supplier updated successfully");
      } else {
        await suppliersService.createSupplier(formData);
        toast.success("Supplier created successfully");
      }
      setIsDialogOpen(false);
      setEditingSupplier(null);
      setFormData({ name: "", contact_person: "", phone: "", email: "", address: "" });
      loadSuppliers();
    } catch (error) {
      toast.error("Operation failed");
    }
  };

  const handleEdit = (supplier: Supplier) => {
    setEditingSupplier(supplier);
    setFormData({
      name: supplier.name,
      contact_person: supplier.contact_person || "",
      phone: supplier.phone || "",
      email: supplier.email || "",
      address: supplier.address || "",
    });
    setIsDialogOpen(true);
  };

  const openPaymentDialog = (supplier: Supplier) => {
    setPaymentSupplierId(supplier.id);
    setPaymentAmount(supplier.balance);
    setPaymentMethod("cash");
    setPaymentReference("");
    setPaymentNotes("");
    setIsPaymentDialogOpen(true);
  };

  const handleRecordPayment = async (e: FormEvent) => {
    e.preventDefault();
    if (!paymentSupplierId || paymentAmount <= 0) return;

    setIsSubmittingPayment(true);
    try {
      await suppliersService.recordPayment(paymentSupplierId, {
        amount: paymentAmount,
        payment_method: paymentMethod,
        reference_number: paymentReference || undefined,
        notes: paymentNotes || undefined,
      });
      toast.success("Payment recorded successfully");
      setIsPaymentDialogOpen(false);
      loadSuppliers();
      // Refresh ledger if viewing
      if (selectedSupplierLedger && selectedSupplierLedger.supplier.id === paymentSupplierId) {
        loadLedger(paymentSupplierId);
      }
    } catch (error) {
      toast.error("Failed to record payment");
    } finally {
      setIsSubmittingPayment(false);
    }
  };

  const ledgerAbortRef = useRef<AbortController | null>(null);

  const loadLedger = async (supplierId: number) => {
    ledgerAbortRef.current?.abort();
    const controller = new AbortController();
    ledgerAbortRef.current = controller;

    setIsLedgerLoading(true);
    try {
      const data = await suppliersService.getSupplierLedger(supplierId, controller.signal);
      if (controller.signal.aborted) return;
      setSelectedSupplierLedger(data);
    } catch (error: any) {
      if (controller.signal.aborted) return;
      toast.error("Failed to load supplier ledger");
    } finally {
      if (!controller.signal.aborted) setIsLedgerLoading(false);
    }
  };

  const handleViewLedger = (supplier: Supplier) => {
    loadLedger(supplier.id);
  };

  // ---- LEDGER LOADING STATE ----
  if (isLedgerLoading && !selectedSupplierLedger) {
    return (
      <div className="flex items-center justify-center h-full min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        <span className="ml-2 text-muted-foreground">Loading ledger...</span>
      </div>
    );
  }

  // ---- LEDGER DETAIL VIEW ----
  if (selectedSupplierLedger) {
    const ledger = selectedSupplierLedger;
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => setSelectedSupplierLedger(null)}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{ledger.supplier.name}</h1>
            <p className="text-muted-foreground">Payment Ledger & Balance Details</p>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Building2 className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Total Purchased</p>
                  <p className="text-2xl font-bold">{currency} {ledger.summary.total_purchased.toLocaleString(undefined, { minimumFractionDigits: 2 })}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Total Paid</p>
                  <p className="text-2xl font-bold text-green-600">{currency} {ledger.summary.total_paid.toLocaleString(undefined, { minimumFractionDigits: 2 })}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className={ledger.summary.outstanding_balance > 0 ? "border-destructive/50" : "border-green-500/50"}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${ledger.summary.outstanding_balance > 0 ? "bg-red-100" : "bg-green-100"}`}>
                    <DollarSign className={`h-5 w-5 ${ledger.summary.outstanding_balance > 0 ? "text-red-600" : "text-green-600"}`} />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Outstanding Balance</p>
                    <p className={`text-2xl font-bold ${ledger.summary.outstanding_balance > 0 ? "text-destructive" : "text-green-600"}`}>
                      {currency} {ledger.summary.outstanding_balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                </div>
                {ledger.summary.outstanding_balance > 0 && (
                  <Button
                    size="sm"
                    onClick={() => {
                      const supplier = suppliers.find(s => s.id === ledger.supplier.id);
                      if (supplier) openPaymentDialog(supplier);
                    }}
                  >
                    <DollarSign className="mr-1 h-4 w-4" /> Record Payment
                  </Button>
                )}
                {ledger.summary.outstanding_balance === 0 && (
                  <Badge variant="default" className="bg-green-600">Fully Paid</Badge>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Purchase History */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Purchase History</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Reference</TableHead>
                  <TableHead>Total Amount</TableHead>
                  <TableHead>Paid on Purchase</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {ledger.purchases.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-6 text-muted-foreground">No purchases recorded.</TableCell>
                  </TableRow>
                ) : (
                  ledger.purchases.map((p) => (
                    <TableRow key={p.id}>
                      <TableCell>{new Date(p.created_at).toLocaleDateString()}</TableCell>
                      <TableCell>{p.reference_number || `PO-${p.id}`}</TableCell>
                      <TableCell className="font-medium">{currency} {p.grand_total.toLocaleString(undefined, { minimumFractionDigits: 2 })}</TableCell>
                      <TableCell>{currency} {p.paid_amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</TableCell>
                      <TableCell>
                        <Badge variant={
                          p.payment_status === "paid" ? "default" :
                          p.payment_status === "partial" ? "secondary" : "destructive"
                        }>
                          {p.payment_status === "paid" ? "Paid" :
                           p.payment_status === "partial" ? "Partial" : "Unpaid"}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Payment History */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Payment History</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Amount</TableHead>
                  <TableHead>Method</TableHead>
                  <TableHead>Reference</TableHead>
                  <TableHead>Notes</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {ledger.payments.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-6 text-muted-foreground">No payments recorded yet.</TableCell>
                  </TableRow>
                ) : (
                  ledger.payments.map((pay) => (
                    <TableRow key={pay.id}>
                      <TableCell>{new Date(pay.payment_date).toLocaleDateString()}</TableCell>
                      <TableCell className="font-medium text-green-600">{currency} {pay.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</TableCell>
                      <TableCell className="capitalize">{pay.payment_method.replace("_", " ")}</TableCell>
                      <TableCell>{pay.reference_number || "—"}</TableCell>
                      <TableCell className="text-muted-foreground">{pay.notes || "—"}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    );
  }

  // ---- MAIN LIST VIEW ----
  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Supplier Ledger</h1>
          <p className="text-muted-foreground">Manage your suppliers, track outstanding balances and record payments.</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={(open) => {
          setIsDialogOpen(open);
          if (!open) {
            setEditingSupplier(null);
            setFormData({ name: "", contact_person: "", phone: "", email: "", address: "" });
          }
        }}>
          <DialogTrigger asChild>
            <Button className="flex items-center gap-2">
              <Plus className="h-4 w-4" /> Add Supplier
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>{editingSupplier ? "Edit Supplier" : "Add New Supplier"}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="name">Business Name</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g. Acme Wholesale"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="contact">Contact Person</Label>
                <Input
                  id="contact"
                  value={formData.contact_person}
                  onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })}
                  placeholder="e.g. John Doe"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    placeholder="+1234567890"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="supplier@example.com"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  placeholder="123 Warehouse St."
                />
              </div>
              <DialogFooter>
                <Button type="submit" className="w-full">
                  {editingSupplier ? "Update Supplier" : "Create Supplier"}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Payment Dialog */}
      <Dialog open={isPaymentDialogOpen} onOpenChange={setIsPaymentDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Record Payment to Supplier</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleRecordPayment} className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>Payment Amount ({currency})</Label>
              <Input
                type="number"
                step="0.01"
                min="0.01"
                value={paymentAmount}
                onChange={(e) => setPaymentAmount(parseFloat(e.target.value) || 0)}
                required
                className="text-lg font-bold"
              />
            </div>
            <div className="space-y-2">
              <Label>Payment Method</Label>
              <Select value={paymentMethod} onValueChange={setPaymentMethod}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cash">Cash</SelectItem>
                  <SelectItem value="bank_transfer">Bank Transfer</SelectItem>
                  <SelectItem value="check">Check</SelectItem>
                  <SelectItem value="online">Online Payment</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Reference Number (Optional)</Label>
              <Input
                value={paymentReference}
                onChange={(e) => setPaymentReference(e.target.value)}
                placeholder="e.g. TRX-12345"
              />
            </div>
            <div className="space-y-2">
              <Label>Notes (Optional)</Label>
              <textarea
                className="w-full min-h-[60px] rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={paymentNotes}
                onChange={(e) => setPaymentNotes(e.target.value)}
                placeholder="Payment details..."
              />
            </div>
            <DialogFooter>
              <Button type="submit" className="w-full" disabled={isSubmittingPayment || paymentAmount <= 0}>
                {isSubmittingPayment ? "Recording..." : "Record Payment"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search suppliers by name, phone or contact..."
                className="pl-10"
                value={searchQuery}
                onChange={handleSearch}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Supplier Name</TableHead>
                <TableHead>Contact Person</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Outstanding Balance</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8">Loading suppliers...</TableCell>
                </TableRow>
              ) : filteredSuppliers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8">No suppliers found.</TableCell>
                </TableRow>
              ) : (
                filteredSuppliers.map((supplier) => (
                  <TableRow key={supplier.id}>
                    <TableCell className="font-medium">{supplier.name}</TableCell>
                    <TableCell>{supplier.contact_person || "\u2014"}</TableCell>
                    <TableCell>{supplier.phone || "\u2014"}</TableCell>
                    <TableCell>
                      <span className={supplier.balance > 0 ? "text-destructive font-bold" : "text-green-600 font-medium"}>
                        {currency} {supplier.balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </span>
                    </TableCell>
                    <TableCell>
                      {supplier.balance > 0 ? (
                        <Badge variant="destructive">Pending</Badge>
                      ) : (
                        <Badge variant="default" className="bg-green-600">Cleared</Badge>
                      )}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-1">
                        <Button variant="ghost" size="icon" title="Edit Supplier" onClick={() => handleEdit(supplier)}>
                          <Edit className="h-4 w-4" />
                        </Button>
                        {supplier.balance > 0 && (
                          <Button variant="ghost" size="icon" title="Record Payment" onClick={() => openPaymentDialog(supplier)}>
                            <DollarSign className="h-4 w-4 text-green-600" />
                          </Button>
                        )}
                        <Button variant="ghost" size="icon" title="View Ledger" onClick={() => handleViewLedger(supplier)}>
                          <History className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
