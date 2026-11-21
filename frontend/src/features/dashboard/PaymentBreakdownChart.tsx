import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import type { PaymentMethodTotal } from '@/services/dashboard.service';

interface PaymentBreakdownChartProps {
  data: PaymentMethodTotal[];
  currency: string;
}

// CSS-variable-driven palette so the chart stays themed across light/dark.
const COLORS = [
  'hsl(var(--primary))',
  'hsl(217.2 91.2% 59.8%)',
  'hsl(142.1 76.2% 36.3%)',
  'hsl(38 92% 50%)',
];

export const PaymentBreakdownChart: React.FC<PaymentBreakdownChartProps> = ({ data, currency }) => {
  const chartData = data.map((d) => ({
    name: d.method,
    value: typeof d.total === 'string' ? parseFloat(d.total) : d.total,
    count: d.count,
  }));

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-[220px] text-sm text-muted-foreground">
        No payments recorded in this period.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          innerRadius={50}
          outerRadius={80}
          paddingAngle={2}
        >
          {chartData.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: 'hsl(var(--popover))',
            borderColor: 'hsl(var(--border))',
            borderRadius: 8,
            fontSize: 12,
          }}
          formatter={(value: any, _name: any, item: any) => [
            `${currency} ${Number(value).toFixed(2)} (${item.payload.count})`,
            item.payload.name,
          ]}
        />
        <Legend
          formatter={(value) => <span className="capitalize text-xs">{value}</span>}
          iconSize={8}
        />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default PaymentBreakdownChart;
