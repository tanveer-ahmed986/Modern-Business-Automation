import React, { useState, useEffect } from "react";
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle,
  CardDescription
} from "@/components/ui/card";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Download, Calendar, TrendingUp, DollarSign, Package, ShoppingCart } from "lucide-react";
import reportsService, { SalesReport, ProfitLossReport } from "@/services/reports.service";
import { toast } from "sonner";

const ReportsPage: React.FC = () => {
  const [startDate, setStartDate] = useState<string>(
    new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0]
  );
  const [endDate, setEndDate] = useState<string>(
    new Date().toISOString().split("T")[0]
  );
  const [salesReport, setSalesReport] = useState<SalesReport | null>(null);
  const [plReport, setPlReport] = useState<ProfitLossReport | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const sales = await reportsService.getSalesReport(startDate, endDate);
      setSalesReport(sales);
      
      try {
        const pl = await reportsService.getProfitLossReport(startDate, endDate);
        setPlReport(pl);
      } catch (err: any) {
        console.warn("P&L report not available (likely non-premium tier)", err);
        setPlReport(null);
      }
    } catch (error: any) {
      toast.error("Failed to load reports: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleExport = () => {
    const url = reportsService.getExportSalesUrl(startDate, endDate);
    window.open(url, "_blank");
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reports & Analytics</h1>
          <p className="text-muted-foreground">Monitor your business performance and financial health.</p>
        </div>
        <Button onClick={handleExport} variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Export Sales (CSV)
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Date Range Filter
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap items-end gap-4">
          <div className="space-y-2">
            <Label htmlFor="start-date">Start Date</Label>
            <Input 
              id="start-date" 
              type="date" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)} 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="end-date">End Date</Label>
            <Input 
              id="end-date" 
              type="date" 
              value={endDate} 
              onChange={(e) => setEndDate(e.target.value)} 
            />
          </div>
          <Button onClick={fetchReports} disabled={loading}>
            {loading ? "Loading..." : "Apply Filter"}
          </Button>
        </CardContent>
      </Card>

      <Tabs defaultValue="sales" className="w-full">
        <TabsList className="grid w-full grid-cols-2 lg:w-[400px]">
          <TabsTrigger value="sales">Sales Overview</TabsTrigger>
          <TabsTrigger value="profit-loss">Profit & Loss</TabsTrigger>
        </TabsList>
        
        <TabsContent value="sales" className="space-y-6 pt-4">
          {salesReport && (
            <>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">${salesReport.summary.total_revenue.toLocaleString()}</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Sales Count</CardTitle>
                    <ShoppingCart className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{salesReport.summary.sale_count}</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Avg. Sale Value</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      ${(salesReport.summary.total_revenue / (salesReport.summary.sale_count || 1)).toFixed(2)}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Tax Collected</CardTitle>
                    <Package className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">${salesReport.summary.total_tax.toLocaleString()}</div>
                  </CardContent>
                </Card>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Card className="col-span-1">
                  <CardHeader>
                    <CardTitle>Top Products</CardTitle>
                    <CardDescription>Most sold products by quantity in this period.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Product Name</TableHead>
                          <TableHead className="text-right">Qty</TableHead>
                          <TableHead className="text-right">Revenue</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {salesReport.top_products.map((product, i) => (
                          <TableRow key={i}>
                            <TableCell className="font-medium">{product.name}</TableCell>
                            <TableCell className="text-right">{product.quantity}</TableCell>
                            <TableCell className="text-right">${product.revenue.toLocaleString()}</TableCell>
                          </TableRow>
                        ))}
                        {salesReport.top_products.length === 0 && (
                          <TableRow>
                            <TableCell colSpan={3} className="text-center py-4">No data available</TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>

                <Card className="col-span-1">
                  <CardHeader>
                    <CardTitle>Revenue by Payment Method</CardTitle>
                    <CardDescription>Breakdown of sales by how customers paid.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Method</TableHead>
                          <TableHead className="text-right">Amount</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {Object.entries(salesReport.payment_methods).map(([method, amount], i) => (
                          <TableRow key={i}>
                            <TableCell className="capitalize">{method}</TableCell>
                            <TableCell className="text-right">${amount.toLocaleString()}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>

                <Card className="col-span-1">
                  <CardHeader>
                    <CardTitle>Sales by Category</CardTitle>
                    <CardDescription>Performance across different product categories.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Category</TableHead>
                          <TableHead className="text-right">Revenue</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {salesReport.category_sales.map((cat, i) => (
                          <TableRow key={i}>
                            <TableCell className="font-medium">{cat.name}</TableCell>
                            <TableCell className="text-right">${cat.revenue.toLocaleString()}</TableCell>
                          </TableRow>
                        ))}
                        {salesReport.category_sales.length === 0 && (
                          <TableRow>
                            <TableCell colSpan={2} className="text-center py-4">No data available</TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </TabsContent>

        <TabsContent value="profit-loss" className="space-y-6 pt-4">
          {!plReport ? (
            <Card className="border-dashed">
              <CardContent className="flex flex-col items-center justify-center py-10 space-y-4">
                <Package className="h-10 w-10 text-muted-foreground" />
                <div className="text-center">
                  <h3 className="text-lg font-semibold">P&L Report Unavailable</h3>
                  <p className="text-muted-foreground">
                    This is a Premium feature. Please upgrade your package to view Gross Profit and COGS analytics.
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              <div className="grid gap-4 md:grid-cols-3">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-600">${plReport.revenue.toLocaleString()}</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">COGS (Cost of Goods Sold)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-red-600">-${plReport.cogs.toLocaleString()}</div>
                  </CardContent>
                </Card>
                <Card className="bg-slate-50 dark:bg-slate-900 border-2">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Gross Profit</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className={`text-2xl font-bold ${plReport.gross_profit >= 0 ? "text-green-600" : "text-red-600"}`}>
                      ${plReport.gross_profit.toLocaleString()}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Cash Flow Summary</CardTitle>
                  <CardDescription>Comparison of Sales Revenue vs Purchase Expenses.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center border-b pb-2">
                      <span>Total Sales (Income)</span>
                      <span className="font-semibold text-green-600">+${plReport.revenue.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center border-b pb-2">
                      <span>Total Purchases (Expense)</span>
                      <span className="font-semibold text-red-600">-${plReport.total_purchases.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center pt-2">
                      <span className="font-bold">Net Cash Flow</span>
                      <span className={`font-bold ${(plReport.revenue - plReport.total_purchases) >= 0 ? "text-green-600" : "text-red-600"}`}>
                        ${(plReport.revenue - plReport.total_purchases).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ReportsPage;
