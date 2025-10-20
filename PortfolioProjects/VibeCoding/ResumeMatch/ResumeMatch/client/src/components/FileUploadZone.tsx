import { useCallback, useState, useEffect } from "react";
import { Upload, File, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
}

interface FileUploadZoneProps {
  files?: File[];
  onFilesChange?: (files: File[]) => void;
}

export function FileUploadZone({ files: externalFiles = [], onFilesChange }: FileUploadZoneProps) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    const uploadedFiles = externalFiles.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file,
    }));
    setFiles(uploadedFiles);
  }, [externalFiles]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      (file) => file.type === "application/pdf" || 
                file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
                file.type === "application/msword"
    );

    const uploadedFiles = droppedFiles.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file,
    }));

    const newFiles = [...files, ...uploadedFiles];
    setFiles(newFiles);
    onFilesChange?.(newFiles.map(f => f.file));
  }, [files, onFilesChange]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const uploadedFiles = selectedFiles.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file,
    }));

    const newFiles = [...files, ...uploadedFiles];
    setFiles(newFiles);
    onFilesChange?.(newFiles.map(f => f.file));
  };

  const removeFile = (id: string) => {
    const newFiles = files.filter((f) => f.id !== id);
    setFiles(newFiles);
    onFilesChange?.(newFiles.map(f => f.file));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-md p-12 text-center transition-colors ${
          isDragging ? "border-primary bg-primary/5" : "border-border hover-elevate"
        }`}
      >
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
            <Upload className="w-8 h-8 text-muted-foreground" />
          </div>
          <div>
            <p className="text-lg font-medium text-foreground" data-testid="text-upload-title">
              Drop CVs here or click to upload
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Supports PDF and Word documents (multiple files)
            </p>
          </div>
          <Button
            variant="outline"
            onClick={() => document.getElementById("file-input")?.click()}
            data-testid="button-browse-files"
          >
            Browse Files
          </Button>
          <input
            id="file-input"
            type="file"
            multiple
            accept=".pdf,.doc,.docx"
            onChange={handleFileInput}
            className="hidden"
            data-testid="input-file"
          />
        </div>
      </div>

      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-foreground">
            Uploaded Files ({files.length})
          </p>
          {files.map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between p-3 border rounded-md hover-elevate"
              data-testid={`file-item-${file.id}`}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded bg-muted flex items-center justify-center">
                  <File className="w-5 h-5 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">{file.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {formatFileSize(file.size)}
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => removeFile(file.id)}
                data-testid={`button-remove-${file.id}`}
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
