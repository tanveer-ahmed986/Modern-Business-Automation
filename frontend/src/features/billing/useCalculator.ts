import { useState, useMemo, useEffect } from "react";
import { settingsService, type Settings } from "../../services/settings.service";

export interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

export const useCalculator = () => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [discount, setDiscount] = useState<number>(0);
  const [settings, setSettings] = useState<Settings | null>(null);

  useEffect(() => {
    settingsService.getSettings().then(setSettings);
  }, []);

  const subtotal = useMemo(() => {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }, [items]);

  const taxAmount = useMemo(() => {
    if (!settings) return 0;
    return subtotal * (settings.tax_rate / 100);
  }, [subtotal, settings]);

  const total = useMemo(() => {
    return subtotal + taxAmount - discount;
  }, [subtotal, taxAmount, discount]);

  const addItem = (item: CartItem) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.id === item.id);
      if (existing) {
        return prev.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
        );
      }
      return [...prev, item];
    });
  };

  const removeItem = (id: number) => {
    setItems((prev) => prev.filter((i) => i.id !== id));
  };

  const updateQuantity = (id: number, quantity: number) => {
    if (quantity <= 0) {
      removeItem(id);
      return;
    }
    setItems((prev) =>
      prev.map((i) => (i.id === id ? { ...i, quantity } : i))
    );
  };

  const clearCart = () => {
    setItems([]);
    setDiscount(0);
  };

  return {
    items,
    discount,
    subtotal,
    taxAmount,
    total,
    addItem,
    removeItem,
    updateQuantity,
    setDiscount,
    clearCart,
    taxRate: settings?.tax_rate || 0,
    currency: settings?.currency || "USD",
  };
};
