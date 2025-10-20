import { useState } from 'react';
import { FileUploadZone } from '@/components/FileUploadZone';
import { ProcessingModeToggle } from '@/components/ProcessingModeToggle';
import { DataPreviewTable } from '@/components/DataPreviewTable';
import { FileCard } from '@/components/FileCard';
import { StatusIndicator } from '@/components/StatusIndicator';
import { Button } from '@/components/ui/button';
import { ArrowDownTray } from '@/components/Icons';
import type { ProcessingMode, ParsedDataRow, FileUploadResponse } from '@shared/schema';
import { useMutation } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';

export default function Home() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [mode, setMode] = useState<ProcessingMode>('combined');
  const [processedFiles, setProcessedFiles] = useState<FileUploadResponse[]>([]);
  const [status, setStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');
  const [statusMessage, setStatusMessage] = useState('');

  const uploadMutation = useMutation({
    mutationFn: async (files: File[]) => {
      const formData = new FormData();
      files.forEach((file) => formData.append('files', file));
      
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      return response.json() as Promise<FileUploadResponse[]>;
    },
    onSuccess: (data) => {
      setProcessedFiles(data);
      
      // Check if any files have errors
      const filesWithErrors = data.filter(f => f.errors && f.errors.length > 0);
      const filesWithData = data.filter(f => f.parsedData.length > 0);
      
      if (filesWithData.length > 0) {
        setStatus('success');
        setStatusMessage(`Successfully processed ${filesWithData.length} ${filesWithData.length === 1 ? 'file' : 'files'}${filesWithErrors.length > 0 ? ` (${filesWithErrors.length} with warnings)` : ''}`);
      } else if (filesWithErrors.length > 0) {
        setStatus('error');
        setStatusMessage('No data could be extracted from uploaded files. Check file format.');
      }
      
      setSelectedFiles([]);
    },
    onError: (error) => {
      setStatus('error');
      setStatusMessage(error instanceof Error ? error.message : 'Failed to process files');
    },
  });

  const downloadMutation = useMutation({
    mutationFn: async ({ format, fileData }: { format: 'excel' | 'csv', fileData: { fileName: string, data: ParsedDataRow[] }[] }) => {
      const response = await apiRequest('POST', '/api/download', {
        mode,
        format,
        files: fileData,
      });

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `processed_data.${format === 'excel' ? 'xlsx' : 'csv'}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    },
  });

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles((prev) => [...prev, ...files]);
    setStatus('idle');
  };

  const handleRemoveFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleProcess = async () => {
    if (selectedFiles.length === 0) return;
    setStatus('processing');
    setStatusMessage('Processing files...');
    uploadMutation.mutate(selectedFiles);
  };

  const handleDownloadCombined = (format: 'excel' | 'csv') => {
    const allData = processedFiles.flatMap(file => 
      mode === 'combined' 
        ? file.parsedData 
        : file.parsedData.map(row => ({ ...row, fileName: file.fileName }))
    );
    downloadMutation.mutate({ 
      format, 
      fileData: [{ fileName: 'combined', data: allData }] 
    });
  };

  const handleDownloadSeparate = (fileName: string, format: 'excel' | 'csv') => {
    const file = processedFiles.find(f => f.fileName === fileName);
    if (file) {
      downloadMutation.mutate({ 
        format, 
        fileData: [{ fileName: file.fileName, data: file.parsedData }] 
      });
    }
  };

  const handleDeleteFile = (fileName: string) => {
    setProcessedFiles(prev => prev.filter(f => f.fileName !== fileName));
    if (processedFiles.length === 1) {
      setStatus('idle');
    }
  };

  const allParsedData = processedFiles.flatMap(file => 
    mode === 'combined' 
      ? file.parsedData 
      : file.parsedData.map(row => ({ ...row, fileName: file.fileName }))
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-20 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <h1 className="text-2xl font-semibold text-foreground">EDIFACT File Processor</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Convert EDIFACT (DELFOR, ORDERS, INVOIC, DESADV) and text files to Excel or CSV format
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="space-y-8">
          <FileUploadZone
            onFilesSelected={handleFilesSelected}
            selectedFiles={selectedFiles}
            onRemoveFile={handleRemoveFile}
            isProcessing={uploadMutation.isPending}
          />

          <ProcessingModeToggle
            mode={mode}
            onModeChange={setMode}
            disabled={uploadMutation.isPending}
          />

          {selectedFiles.length > 0 && processedFiles.length === 0 && (
            <Button
              onClick={handleProcess}
              disabled={uploadMutation.isPending}
              className="w-full sm:w-auto"
              data-testid="button-process"
            >
              {uploadMutation.isPending ? 'Processing...' : `Process ${selectedFiles.length} ${selectedFiles.length === 1 ? 'File' : 'Files'}`}
            </Button>
          )}

          <StatusIndicator status={status} message={statusMessage} />

          {processedFiles.length > 0 && mode === 'combined' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-foreground">Preview Data</h2>
                <div className="flex gap-2">
                  <Button
                    onClick={() => handleDownloadCombined('excel')}
                    variant="default"
                    disabled={downloadMutation.isPending}
                    data-testid="button-download-excel-combined"
                  >
                    <ArrowDownTray className="w-4 h-4 mr-2" />
                    Download Excel
                  </Button>
                  <Button
                    onClick={() => handleDownloadCombined('csv')}
                    variant="secondary"
                    disabled={downloadMutation.isPending}
                    data-testid="button-download-csv-combined"
                  >
                    <ArrowDownTray className="w-4 h-4 mr-2" />
                    Download CSV
                  </Button>
                </div>
              </div>
              <DataPreviewTable data={allParsedData} />
            </div>
          )}

          {processedFiles.length > 0 && mode === 'separate' && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold text-foreground">Processed Files</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {processedFiles.map((file) => (
                  <FileCard
                    key={file.fileName}
                    fileName={file.fileName}
                    fileSize={file.fileSize}
                    data={file.parsedData}
                    errors={file.errors}
                    onDownload={(format) => handleDownloadSeparate(file.fileName, format)}
                    onDelete={() => handleDeleteFile(file.fileName)}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
