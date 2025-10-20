import { useCallback, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import { CloudArrowUp, DocumentText, XMark } from '@/components/Icons';
import { Badge } from '@/components/ui/badge';

interface FileUploadZoneProps {
  onFilesSelected: (files: File[]) => void;
  selectedFiles: File[];
  onRemoveFile: (index: number) => void;
  isProcessing: boolean;
}

export function FileUploadZone({ onFilesSelected, selectedFiles, onRemoveFile, isProcessing }: FileUploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  
  const handleFileChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      onFilesSelected(Array.from(files));
      // Reset input value to allow selecting the same file again
      event.target.value = '';
    }
  }, [onFilesSelected]);
  
  const { getRootProps, isDragActive } = useDropzone({
    onDrop: onFilesSelected,
    disabled: isProcessing,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'application/octet-stream': ['.FGD', '.fgd'],
    },
    multiple: true,
    noClick: true,
    noKeyboard: false,
  });
  
  const handleClick = () => {
    if (!isProcessing && inputRef.current) {
      inputRef.current.click();
    }
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        onClick={handleClick}
        data-testid="dropzone-upload"
        className={`
          border-2 border-dashed rounded-lg transition-all duration-200
          ${selectedFiles.length > 0 ? 'h-40' : 'h-64'}
          ${isDragActive ? 'border-primary bg-primary/5 scale-[1.02]' : 'border-border'}
          ${isProcessing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover-elevate'}
          flex flex-col items-center justify-center gap-4 p-8
        `}
      >
        <input
          ref={inputRef}
          type="file"
          onChange={handleFileChange}
          data-testid="input-file"
          aria-label="File upload input"
          className="hidden"
          multiple
          accept=".txt,.pdf,.doc,.docx,.FGD,.fgd"
          disabled={isProcessing}
        />
        <CloudArrowUp className="w-12 h-12 text-muted-foreground" />
        <div className="text-center">
          <p className="text-base font-medium text-foreground">
            {isDragActive ? 'Drop files here' : 'Drag files here or click to browse'}
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            Supports EDIFACT, PDF, TXT, Word (.doc, .docx)
          </p>
        </div>
      </div>

      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-foreground">Selected Files ({selectedFiles.length})</p>
          <div className="flex flex-wrap gap-2">
            {selectedFiles.map((file, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="px-3 py-2 pr-2 gap-2 max-w-xs"
                data-testid={`badge-file-${index}`}
              >
                <DocumentText className="w-4 h-4 flex-shrink-0" />
                <span className="font-mono text-xs truncate flex-1">{file.name}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onRemoveFile(index);
                  }}
                  disabled={isProcessing}
                  className="hover-elevate active-elevate-2 rounded-sm p-0.5"
                  data-testid={`button-remove-file-${index}`}
                >
                  <XMark className="w-3.5 h-3.5" />
                </button>
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
