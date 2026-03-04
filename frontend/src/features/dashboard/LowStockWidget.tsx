import React from 'react';
import { AlertTriangle, CheckCircle, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router';

interface LowStockWidgetProps {
  count: number;
}

export const LowStockWidget: React.FC<LowStockWidgetProps> = ({ count }) => {
  const navigate = useNavigate();

  return (
    <Card className={count > 0 ? "border-destructive/50 bg-destructive/5" : "border-primary/20 bg-primary/5"}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">Inventory Health</CardTitle>
        {count > 0 ? (
          <AlertTriangle className="h-4 w-4 text-destructive" />
        ) : (
          <CheckCircle className="h-4 w-4 text-primary" />
        )}
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <div className="text-2xl font-bold">
              {count > 0 ? `${count} Items Low` : "All Healthy"}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {count > 0 
                ? "Immediate attention required for stock levels." 
                : "All products are above their low stock thresholds."}
            </p>
          </div>
          
          {count > 0 && (
            <Button 
              variant="outline" 
              size="sm" 
              className="w-full justify-between"
              onClick={() => navigate('/inventory')}
            >
              View Low Stock Items
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
