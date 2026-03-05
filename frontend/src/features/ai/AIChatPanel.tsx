import React, { useState, useEffect } from "react";
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { 
  BarChart, 
  MessageSquare, 
  Send, 
  Bot, 
  User as UserIcon,
  Zap
} from "lucide-react";
import aiService from "@/services/ai.service";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface Message {
  id: number;
  sender: "user" | "ai";
  text: string;
  isPrediction?: boolean;
}

const AIChatPanel: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<any[]>([]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { id: messages.length + 1, sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await aiService.queryAI(input);
      const aiMessage: Message = { id: messages.length + 2, sender: "ai", text: response.response };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error: any) {
      toast.error("AI query failed: " + (error.response?.data?.detail || error.message));
      const errorMessage: Message = { id: messages.length + 2, sender: "ai", text: "I'm sorry, I encountered an error. Please try again later." };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleGetPredictions = async () => {
    setLoading(true);
    try {
      const data = await aiService.getSalesPrediction(30); // Predict next 30 days
      setPredictions(data);
      const predictionMessage: Message = { 
        id: messages.length + 1, 
        sender: "ai", 
        text: "Here are the sales predictions for the next 30 days:",
        isPrediction: true,
      };
      setMessages((prev) => [...prev, predictionMessage]);
    } catch (error: any) {
      toast.error("Sales prediction failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Scroll to bottom of chat
    const chatContainer = document.getElementById("chat-container");
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages, predictions]);

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Assistant</h1>
          <p className="text-muted-foreground">Your intelligent business co-pilot (Premium Feature).</p>
        </div>
        <Button onClick={handleGetPredictions} disabled={loading} variant="outline">
          <BarChart className="mr-2 h-4 w-4" />
          Get Sales Predictions
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5" />
              Chat with AI
            </CardTitle>
            <CardDescription>Ask questions about your business data (e.g., "What were sales last month?").</CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea id="chat-container" className="h-[400px] pr-4">
              <div className="space-y-4">
                {messages.map((msg) => (
                  <div key={msg.id} className={cn(
                    "flex items-start gap-3",
                    msg.sender === "user" ? "justify-end" : "justify-start"
                  )}>
                    {msg.sender === "ai" && (
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="bg-blue-500 text-white"><Bot className="h-5 w-5" /></AvatarFallback>
                      </Avatar>
                    )}
                    <div className={cn(
                      "rounded-lg p-3 max-w-[70%]",
                      msg.sender === "user" ? "bg-blue-500 text-white" : "bg-muted text-foreground"
                    )}>
                      {msg.text}
                      {msg.isPrediction && predictions.length > 0 && (
                        <div className="mt-2 bg-background p-3 rounded-md border text-sm">
                          <h4 className="font-semibold mb-1">Sales Predictions (Next 30 Days)</h4>
                          <ul className="list-disc pl-5">
                            {predictions.slice(0, 5).map((p, idx) => ( // Show first 5 predictions
                              <li key={idx}>
                                {p.date}: ${p.predicted_revenue.toFixed(2)}
                              </li>
                            ))}
                            {predictions.length > 5 && (
                              <li>...and {predictions.length - 5} more days.</li>
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                    {msg.sender === "user" && (
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="bg-gray-500 text-white"><UserIcon className="h-5 w-5" /></AvatarFallback>
                      </Avatar>
                    )}
                  </div>
                ))}
              </div>
            </ScrollArea>
            <div className="mt-4 flex gap-2">
              <Input
                placeholder="Ask me anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === "Enter") handleSendMessage();
                }}
                disabled={loading}
              />
              <Button onClick={handleSendMessage} disabled={loading}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-yellow-500" />
              AI Insights
            </CardTitle>
            <CardDescription>Automated insights and proactive recommendations.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg">
              <h4 className="font-semibold text-blue-800 dark:text-blue-200">Sales Prediction Overview</h4>
              {predictions.length > 0 ? (
                <div className="mt-2 text-sm text-blue-700 dark:text-blue-300">
                  <p>Next 30 days total predicted revenue: <span className="font-bold">${predictions.reduce((sum, p) => sum + p.predicted_revenue, 0).toFixed(2)}</span></p>
                  <p>Highest predicted day: {predictions[0].date} with ${predictions[0].predicted_revenue.toFixed(2)}</p>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Click "Get Sales Predictions" to generate forecasts.</p>
              )}
            </div>
            {/* Additional insights could go here */}
            <div className="text-sm text-muted-foreground">
              More automated insights (e.g., low-profit items, inventory optimization) coming soon!
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AIChatPanel;
