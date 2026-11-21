import React, { useMemo, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { ColumnDef } from '@tanstack/react-table';
import { History, Loader2, RotateCcw, AlertTriangle } from 'lucide-react';
import {
  Card, CardContent, CardDescription, CardHeader, CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { DataTable } from '@/components/ui/data-table';
import { toast } from 'sonner';
import { billingService, type Sale } from '@/services/billing.service';
import authService from '@/services/auth.service';
import reportsService from '@/services/reports.service';
import { useBranding } from '@/hooks/useBranding';

const PAGE_SIZE = 25;

const statusVariant = (status: string): 'default' | 'secondary' | 'destructive' => {
  if (status === 'completed') return 'default';
  if (status === 'refunded') return 'destructive';
  return 'secondary';
};

const SalesHistoryPage: React.FC = () => {
  const branding = useBranding();
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [refundTarget, setRefundTarget] = useState<Sale | null>(null);

  const currentUser = authService.getCurrentUser();
  const canRefund = currentUser?.role === 'admin' || currentUser?.role === 'manager';

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['sales', page],
    queryFn: () => billingService.getSales({ page, page_size: PAGE_SIZE }),
    placeholderData: (previous) => previous, // keep table filled while paging
  });

  const refundMutation = useMutation({
    mutationFn: (saleId: number) => billingService.refundSale(saleId),
    onSuccess: (sale) => {
      toast.success(`Invoice ${sale.invoice_number} refunded — stock restored`);
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-metrics'] });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Refund failed');
    },
    onSettled: () => setRefundTarget(null),
  });

  const totalPages = data?.pagination.total_pages ?? 1;

  const handleExportCsv = async () => {
    try {
      await reportsService.downloadSalesCsv();
    } catch {
      toast.error('Failed to export sales CSV');
    }
  };

  const columns: ColumnDef<Sale>[] = useMemo(() => [
    {
      accessorKey: 'invoice_number',
      header: 'Invoice #',
      cell: ({ row }) => <span className="font-mono text-xs">{row.original.invoice_number}</span>,
    },
    {
      accessorKey: 'created_at',
      header: 'Date',
      cell: ({ row }) => (
        <span className="whitespace-nowrap">
          {new Date(row.original.created_at + 'Z').toLocaleString()}
        </span>
      ),
    },
    {
      id: 'customer',
      header: 'Customer',
      cell: ({ row }) => row.original.customer?.name || 'Walk-in',
    },
    {
      id: 'items',
      header: () => <span className="block text-center">Items</span>,
      cell: ({ row }) => <span className="block text-center">{row.original.items.length}</span>,
    },
    {
      accessorKey: 'payment_method',
      header: 'Payment',
      cell: ({ row }) => <span className="capitalize">{row.original.payment_method}</span>,
    },
    {
      accessorKey: 'grand_total',
      header: () => <span className="block text-right">Total</span>,
      cell: ({ row }) => (
        <span className="block text-right font-medium">
          {branding.currency} {Number(row.original.grand_total).toFixed(2)}
        </span>
      ),
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => (
        <Badge variant={statusVariant(row.original.status)} className="capitalize">
          {row.original.status}
        </Badge>
      ),
    },
    ...(canRefund ? [{
      id: 'actions',
      header: '',
      cell: ({ row }: { row: { original: Sale } }): React.ReactNode => {
        const sale = row.original;
        if (sale.status !== 'completed') return null;
        if (refundTarget?.id === sale.id) {
          return (
            <div className="flex gap-1">
              <Button
                size="sm"
                variant="destructive"
                className="h-7 px-2 text-xs"
                disabled={refundMutation.isPending}
                onClick={() => refundMutation.mutate(sale.id)}
              >
                {refundMutation.isPending ? '...' : 'Confirm'}
              </Button>
              <Button
                size="sm"
                variant="ghost"
                className="h-7 px-2 text-xs"
                onClick={() => setRefundTarget(null)}
              >
                Cancel
              </Button>
            </div>
          );
        }
        return (
          <Button
            size="sm"
            variant="outline"
            className="h-7 px-2 text-xs"
            onClick={() => setRefundTarget(sale)}
          >
            <RotateCcw className="mr-1 h-3 w-3" /> Refund
          </Button>
        );
      },
    }] : []),
  ], [branding.currency, canRefund, refundTarget, refundMutation.isPending]);

  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (isError && !data) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4">
        <AlertTriangle className="h-12 w-12 text-amber-500" />
        <p className="text-muted-foreground">Could not load sales history.</p>
        <Button onClick={() => refetch()}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <History className="h-7 w-7" /> Sales History
        </h2>
        <p className="text-muted-foreground">
          All invoices, newest first.{canRefund && ' Refunding a sale restores its stock.'}
        </p>
      </div>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-lg">Invoices</CardTitle>
          <CardDescription>
            {data?.pagination.total_count ?? 0} total sales
          </CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            columns={columns}
            data={data?.items ?? []}
            isLoading={isLoading}
            page={page}
            pageCount={totalPages}
            onPageChange={setPage}
            totalCount={data?.pagination.total_count}
            onExportCsv={handleExportCsv}
            emptyTitle="No sales recorded yet."
          />
        </CardContent>
      </Card>
    </div>
  );
};

export default SalesHistoryPage;
