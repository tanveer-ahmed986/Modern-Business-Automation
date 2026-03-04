import React from "react";
import { type Sale } from "../../services/billing.service";
import { useBranding } from "../../hooks/useBranding";
import { Separator } from "../../components/ui/separator";

interface InvoiceTemplateProps {
  sale: Sale;
}

export const InvoiceTemplate: React.FC<InvoiceTemplateProps> = ({ sale }) => {
  const branding = useBranding();
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="max-w-[800px] mx-auto p-4 text-black bg-white">
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
                  {branding.currency} {item.unit_price.toFixed(2)}
                </td>
                <td className="py-3 text-sm text-right font-medium">
                  {branding.currency} {item.subtotal.toFixed(2)}
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
            <span>{branding.currency} {sale.total_amount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Tax ({branding.taxRate}%)</span>
            <span>{branding.currency} {sale.tax_amount.toFixed(2)}</span>
          </div>
          {sale.discount_amount > 0 && (
            <div className="flex justify-between text-sm text-red-600">
              <span>Discount</span>
              <span>-{branding.currency} {sale.discount_amount.toFixed(2)}</span>
            </div>
          )}
          <div className="pt-2 border-t-2 border-black flex justify-between">
            <span className="font-bold text-lg">Total</span>
            <span className="font-bold text-lg">
              {branding.currency} {sale.grand_total.toFixed(2)}
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
      
      {/* Print-only CSS */}
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
        }
      `}</style>
    </div>
  );
};
