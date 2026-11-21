import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ErrorBoundaryState {
  hasError: boolean;
}

export class ErrorBoundary extends React.Component<React.PropsWithChildren, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: unknown, info: React.ErrorInfo) {
    console.error('Unhandled UI error:', error, info.componentStack);
  }

  // key bump forces React to remount the failed subtree on retry
  private resetKey = 0;

  handleRetry = () => {
    this.resetKey += 1;
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center h-full min-h-[50vh] gap-4 text-center px-6">
          <div className="flex items-center justify-center h-12 w-12 rounded-full bg-destructive/10 text-destructive">
            <AlertTriangle className="h-6 w-6" />
          </div>
          <div>
            <p className="font-medium">Something went wrong loading this page.</p>
            <p className="text-sm text-muted-foreground mt-1">
              Your data is safe. Try again, or switch to another section.
            </p>
          </div>
          <Button onClick={this.handleRetry}>Try again</Button>
        </div>
      );
    }
    return <React.Fragment key={this.resetKey}>{this.props.children}</React.Fragment>;
  }
}

export default ErrorBoundary;
