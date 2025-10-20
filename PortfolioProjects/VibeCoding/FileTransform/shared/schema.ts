import { z } from "zod";

// Parsed data row from EDIFACT or other files
export const parsedDataRow = z.object({
  reference: z.string(),
  date: z.string(),
  quantity: z.string(),
  fileName: z.string().optional(),
});

export type ParsedDataRow = z.infer<typeof parsedDataRow>;

// File upload response
export const fileUploadResponse = z.object({
  fileName: z.string(),
  fileSize: z.number(),
  parsedData: z.array(parsedDataRow),
  errors: z.array(z.string()).optional(),
});

export type FileUploadResponse = z.infer<typeof fileUploadResponse>;

// Processing mode
export const processingMode = z.enum(['combined', 'separate']);
export type ProcessingMode = z.infer<typeof processingMode>;

// Export request
export const exportRequest = z.object({
  mode: processingMode,
  format: z.enum(['excel', 'csv']),
  files: z.array(z.object({
    fileName: z.string(),
    data: z.array(parsedDataRow),
  })),
});

export type ExportRequest = z.infer<typeof exportRequest>;
