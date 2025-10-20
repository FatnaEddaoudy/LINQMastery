import { Spinner, CheckCircle, ExclamationCircle } from '@/components/Icons';

interface StatusIndicatorProps {
  status: 'idle' | 'processing' | 'success' | 'error';
  message?: string;
}

export function StatusIndicator({ status, message }: StatusIndicatorProps) {
  if (status === 'idle') return null;

  return (
    <div className="flex items-center gap-3 p-4 rounded-lg border bg-card">
      {status === 'processing' && (
        <>
          <Spinner className="w-6 h-6 text-primary" />
          <p className="text-sm font-medium text-foreground">
            {message || 'Processing files...'}
          </p>
        </>
      )}
      {status === 'success' && (
        <>
          <div className="w-6 h-6 rounded-full bg-chart-2 flex items-center justify-center flex-shrink-0">
            <CheckCircle className="w-5 h-5 text-white" />
          </div>
          <p className="text-sm font-medium text-foreground">
            {message || 'Files processed successfully!'}
          </p>
        </>
      )}
      {status === 'error' && (
        <>
          <div className="w-6 h-6 rounded-full bg-destructive flex items-center justify-center flex-shrink-0">
            <ExclamationCircle className="w-5 h-5 text-destructive-foreground" />
          </div>
          <p className="text-sm font-medium text-destructive">
            {message || 'Error processing files'}
          </p>
        </>
      )}
    </div>
  );
}
