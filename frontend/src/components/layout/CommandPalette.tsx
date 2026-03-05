import React, { useState, useEffect, useCallback } from "react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "cmdk";
import { LayoutDashboard, Package, ShoppingCart, Settings, Users, BarChart3, Database, BrainCircuit, Truck, FileDown } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

interface CommandItem {
  label: string;
  icon: React.ElementType;
  path: string;
  keywords?: string[];
}

const commandItems: CommandItem[] = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard", keywords: ["home", "overview"] },
  { label: "Inventory", icon: Package, path: "/inventory", keywords: ["products", "stock", "items"] },
  { label: "Billing", icon: ShoppingCart, path: "/billing", keywords: ["sales", "invoices", "pos"] },
  { label: "Suppliers", icon: Truck, path: "/suppliers", keywords: ["vendors", "purchasing"] },
  { label: "Purchases", icon: FileDown, path: "/purchases/new", keywords: ["orders", "buy"] },
  { label: "Reports", icon: BarChart3, path: "/reports", keywords: ["analytics", "statistics", "financial"] },
  { label: "Users", icon: Users, path: "/users", keywords: ["accounts", "employees", "staff"] },
  { label: "Backup", icon: Database, path: "/backup", keywords: ["data safety", "restore"] },
  { label: "AI Assistant", icon: BrainCircuit, path: "/ai", keywords: ["predictions", "llm", "chat"] },
  { label: "Settings", icon: Settings, path: "/settings", keywords: ["configuration", "preferences"] },
];

const CommandPalette: React.FC = () => {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const handleSelect = useCallback((path: string) => {
    navigate(path);
    setOpen(false);
  }, [navigate]);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="p-0 overflow-hidden shadow-lg max-w-lg">
        <Command label="Global Command Menu">
          <CommandInput placeholder="Type a command or search..." />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup heading="Suggestions">
              {commandItems.map((item) => (
                <CommandItem key={item.path} onSelect={() => handleSelect(item.path)}>
                  <item.icon className="mr-2 h-4 w-4" />
                  {item.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </DialogContent>
    </Dialog>
  );
};

export default CommandPalette;