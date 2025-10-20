import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowDownTray, Trash, DocumentText, ExclamationCircle } from '@/components/Icons';
import type { ParsedDataRow } from '@shared/schema';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

interface FileCardProps {
  fileName: string;
  fileSize: number;
  data: ParsedDataRow[];
  errors?: string[];
  onDownload: (format: 'excel' | 'csv') => void;
  onDelete: () => void;
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

export function FileCard({ fileName, fileSize, data, errors, onDownload, onDelete }: FileCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-3">
        <div className="flex items-center gap-2 min-w-0 flex-1">
          <DocumentText className="w-5 h-5 text-muted-foreground flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <p className="font-mono text-sm truncate" data-testid={`text-filename-${fileName}`}>
              {fileName}
            </p>
            <p className="text-xs text-muted-foreground">{formatFileSize(fileSize)}</p>
          </div>
        </div>
        <Button
          size="icon"
          variant="ghost"
          onClick={onDelete}
          data-testid={`button-delete-${fileName}`}
        >
          <Trash className="w-4 h-4" />
        </Button>
      </CardHeader>
      <CardContent className="pb-3 space-y-3">
        {errors && errors.length > 0 && (
          <div className="flex items-start gap-2 p-3 rounded-md bg-destructive/10 border border-destructive/20">
            <ExclamationCircle className="w-4 h-4 text-destructive flex-shrink-0 mt-0.5" />
            <div className="text-xs text-destructive space-y-1">
              {errors.map((error, idx) => (
                <p key={idx}>{error}</p>
              ))}
            </div>
          </div>
        )}
        {data.length > 0 ? (
          <div className="border rounded-md overflow-hidden">
            <div className="max-h-48 overflow-auto">
              <Table>
                <TableHeader className="bg-muted">
                  <TableRow>
                    <TableHead className="text-xs font-semibold">Reference</TableHead>
                    <TableHead className="text-xs font-semibold">Date</TableHead>
                    <TableHead className="text-xs font-semibold text-right">Quantity</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.slice(0, 5).map((row, index) => (
                    <TableRow key={index}>
                      <TableCell className="font-mono text-xs py-2">{row.reference}</TableCell>
                      <TableCell className="text-xs py-2">{row.date}</TableCell>
                      <TableCell className="font-mono text-xs py-2 text-right">{row.quantity}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            {data.length > 5 && (
              <div className="px-3 py-2 bg-muted/50 text-xs text-muted-foreground text-center border-t">
                +{data.length - 5} more rows
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-6 text-sm text-muted-foreground">
            No data extracted from this file
          </div>
        )}
      </CardContent>
      <CardFooter className="gap-2 pt-0">
        <Button
          onClick={() => onDownload('excel')}
          variant="default"
          className="flex-1"
          disabled={data.length === 0}
          data-testid={`button-download-excel-${fileName}`}
        >
          <ArrowDownTray className="w-4 h-4 mr-2" />
          Excel
        </Button>
        <Button
          onClick={() => onDownload('csv')}
          variant="secondary"
          className="flex-1"
          disabled={data.length === 0}
          data-testid={`button-download-csv-${fileName}`}
        >
          <ArrowDownTray className="w-4 h-4 mr-2" />
          CSV
        </Button>
      </CardFooter>
    </Card>
  );
}
