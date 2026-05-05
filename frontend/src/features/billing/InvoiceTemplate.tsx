import React, { useState } from "react";
import { type Sale } from "../../services/billing.service";
import { useBranding } from "../../hooks/useBranding";
import { Separator } from "../../components/ui/separator";
import { Button } from "../../components/ui/button";
import { Printer } from "lucide-react";

interface InvoiceTemplateProps {
  sale: Sale;
  printFormat?: 'thermal' | 'a4';
}

export const InvoiceTemplate: React.FC<InvoiceTemplateProps> = ({ sale, printFormat = 'a4' }) => {
  const branding = useBranding();
  const [format, setFormat] = useState<'thermal' | 'a4'>(printFormat);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  // Helper to safely convert Decimal strings to numbers and format
  const formatAmount = (amount: number | string): string => {
    const num = typeof amount === 'string' ? parseFloat(amount) : amount;
    return num.toFixed(2);
  };

  const handlePrint = (selectedFormat: 'thermal' | 'a4') => {
    setFormat(selectedFormat);
    setTimeout(() => window.print(), 100);
  };

  // Thermal receipt layout (58mm/80mm paper roll)
  const ThermalReceipt = () => (
    <div className="thermal-receipt max-w-[300px] mx-auto p-4 text-black bg-white text-xs">
      <div className="text-center mb-4">
        <h2 className="text-lg font-bold">{branding.businessName}</h2>
        <p className="text-xs">Tax ID: {branding.taxRate}%</p>
        <p className="text-xs mt-2">{formatDate(sale.created_at)}</p>
        <p className="text-xs font-mono">Invoice #{sale.id}</p>
      </div>

      <div className="border-t border-b border-dashed border-gray-400 py-2 my-2">
        {sale.customer ? (
          <>
            <p className="font-bold">{sale.customer.name}</p>
            {sale.customer.phone && <p>{sale.customer.phone}</p>}
          </>
        ) : (
          <p className="italic">Walk-in Customer</p>
        )}
      </div>

      <table className="w-full mb-2">
        <tbody>
          {sale.items.map((item) => (
            <React.Fragment key={item.id}>
              <tr>
                <td colSpan={3} className="font-medium">{item.product_name}</td>
              </tr>
              <tr className="text-xs">
                <td>{item.quantity} x {branding.currency}{formatAmount(item.unit_price)}</td>
                <td></td>
                <td className="text-right font-medium">{branding.currency}{formatAmount(item.subtotal)}</td>
              </tr>
            </React.Fragment>
          ))}
        </tbody>
      </table>

      <div className="border-t border-dashed border-gray-400 pt-2 mt-2 space-y-1">
        <div className="flex justify-between">
          <span>Subtotal:</span>
          <span>{branding.currency}{formatAmount(sale.total_amount)}</span>
        </div>
        <div className="flex justify-between">
          <span>Tax ({branding.taxRate}%):</span>
          <span>{branding.currency}{formatAmount(sale.tax_amount)}</span>
        </div>
        {parseFloat(sale.discount_amount as any) > 0 && (
          <>
            <div className="flex justify-between text-red-600">
              <span>Discount:</span>
              <span>-{branding.currency}{formatAmount(sale.discount_amount)}</span>
            </div>
            <div className="flex justify-between font-bold bg-green-100 px-2 py-1">
              <span>YOU SAVED:</span>
              <span>{branding.currency}{formatAmount(sale.discount_amount)}</span>
            </div>
          </>
        )}
        <div className="flex justify-between font-bold text-base border-t border-double border-gray-800 pt-2 mt-2">
          <span>TOTAL:</span>
          <span>{branding.currency}{formatAmount(sale.grand_total)}</span>
        </div>
        <div className="flex justify-between text-xs mt-2">
          <span>Payment:</span>
          <span className="uppercase">{sale.payment_method}</span>
        </div>
      </div>

      <div className="text-center mt-4 pt-4 border-t border-dashed">
        <p className="font-medium">Thank you for your business!</p>
        <p className="text-xs mt-1">Come again!</p>
      </div>
    </div>
  );

  // A4 page layout (dealers/suppliers)
  const A4Invoice = () => (
    <div className="a4-invoice max-w-[800px] mx-auto p-4 text-black bg-white">
      {/* Header */}
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold uppercase tracking-tighter">INVOICE</h1>
          <p className="text-sm text-gray-500">#{sale.id}</p>
          <div className="mt-4">
            <p className="text-xs uppercase font-bold text-gray-400">Date</p>
            <p className="text-sm font-medium">{formatDate(sale.created_at)}</p>
          </div>
        </div>
        
        <div className="text-right">
          <h2 className="text-xl font-bold">{branding.businessName}</h2>
          <p className="text-sm text-gray-600">Offline Business Automation</p>
          <p className="text-sm text-gray-600">Tax ID: {branding.taxRate}% Applied</p>
        </div>
      </div>

      <Separator className="my-6" />

      {/* Bill To */}
      <div className="mb-8">
        <p className="text-xs uppercase font-bold text-gray-400 mb-1">Bill To</p>
        {sale.customer ? (
          <div>
            <p className="font-bold">{sale.customer.name}</p>
            {sale.customer.phone && <p className="text-sm text-gray-600">{sale.customer.phone}</p>}
            {sale.customer.address && <p className="text-sm text-gray-600">{sale.customer.address}</p>}
          </div>
        ) : (
          <p className="text-sm italic text-gray-500">Guest Customer</p>
        )}
      </div>

      {/* Items Table */}
      <div className="mb-8">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b-2 border-black">
              <th className="py-2 text-sm font-bold uppercase">Item Description</th>
              <th className="py-2 text-sm font-bold uppercase text-center">Qty</th>
              <th className="py-2 text-sm font-bold uppercase text-right">Unit Price</th>
              <th className="py-2 text-sm font-bold uppercase text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {sale.items.map((item) => (
              <tr key={item.id} className="border-b border-gray-200">
                <td className="py-3 text-sm font-medium">{item.product_name}</td>
                <td className="py-3 text-sm text-center">{item.quantity}</td>
                <td className="py-3 text-sm text-right">
                  {branding.currency} {formatAmount(item.unit_price)}
                </td>
                <td className="py-3 text-sm text-right font-medium">
                  {branding.currency} {formatAmount(item.subtotal)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Totals */}
      <div className="flex justify-end">
        <div className="w-64 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Subtotal</span>
            <span>{branding.currency} {formatAmount(sale.total_amount)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Tax ({branding.taxRate}%)</span>
            <span>{branding.currency} {formatAmount(sale.tax_amount)}</span>
          </div>
          {parseFloat(sale.discount_amount as any) > 0 && (
            <>
              <div className="flex justify-between text-sm text-red-600">
                <span>Discount</span>
                <span>-{branding.currency} {formatAmount(sale.discount_amount)}</span>
              </div>
              <div className="flex justify-between text-sm font-bold text-green-600 bg-green-50 px-2 py-1 rounded">
                <span>YOU SAVED</span>
                <span>{branding.currency} {formatAmount(sale.discount_amount)}</span>
              </div>
            </>
          )}
          <div className="pt-2 border-t-2 border-black flex justify-between">
            <span className="font-bold text-lg">Total</span>
            <span className="font-bold text-lg">
              {branding.currency} {formatAmount(sale.grand_total)}
            </span>
          </div>
          <div className="mt-4 pt-4 text-right">
            <p className="text-xs uppercase font-bold text-gray-400">Payment Method</p>
            <p className="text-sm font-bold uppercase">{sale.payment_method}</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-20 text-center border-t border-gray-100 pt-8">
        <p className="text-sm font-medium">Thank you for your business!</p>
        <p className="text-xs text-gray-400 mt-1 italic">
          This is a computer-generated invoice. No signature required.
        </p>
      </div>
      
      {/* Footer */}
      <div className="mt-20 text-center border-t border-gray-100 pt-8">
        <p className="text-sm font-medium">Thank you for your business!</p>
        <p className="text-xs text-gray-400 mt-1 italic">
          This is a computer-generated invoice. No signature required.
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Print Format Selector - Hidden when printing */}
      <div className="print:hidden mb-4 flex justify-center gap-4">
        <Button
          variant={format === 'thermal' ? 'default' : 'outline'}
          onClick={() => handlePrint('thermal')}
          className="gap-2"
        >
          <Printer className="h-4 w-4" />
          Print Receipt (Thermal)
        </Button>
        <Button
          variant={format === 'a4' ? 'default' : 'outline'}
          onClick={() => handlePrint('a4')}
          className="gap-2"
        >
          <Printer className="h-4 w-4" />
          Print Invoice (A4)
        </Button>
      </div>

      {/* Invoice Display */}
      <div id="printable-invoice">
        {format === 'thermal' ? <ThermalReceipt /> : <A4Invoice />}
      </div>

      {/* Print-specific CSS */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #printable-invoice, #printable-invoice * {
            visibility: visible;
          }
          #printable-invoice {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }

          /* Thermal receipt print settings */
          .thermal-receipt {
            width: 80mm;
            max-width: 80mm;
            font-size: 10pt;
          }

          /* A4 print settings */
          .a4-invoice {
            width: 210mm;
            padding: 20mm;
          }

          @page {
            margin: 0;
          }
        }
      `}</style>
    </>
  );
};
