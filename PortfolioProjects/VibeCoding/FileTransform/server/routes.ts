import type { Express } from "express";
import { createServer, type Server } from "http";
import multer from "multer";
import { parseEDIFACT, parseTextFile } from "./edifactParser";
import { parsePDF, parseWord } from "./documentParser";
import * as XLSX from 'xlsx';
import Papa from 'papaparse';
import type { ParsedDataRow } from "@shared/schema";

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
});

export async function registerRoutes(app: Express): Promise<Server> {
  // Upload and process files
  app.post('/api/upload', upload.array('files', 10), async (req, res) => {
    try {
      const files = req.files as Express.Multer.File[];
      
      if (!files || files.length === 0) {
        return res.status(400).json({ error: 'No files uploaded' });
      }

      const results = await Promise.all(files.map(async (file) => {
        const content = file.buffer.toString('utf-8');
        let parsedData: ParsedDataRow[] = [];
        const errors: string[] = [];

        try {
          // Determine file type and parse accordingly
          const extension = file.originalname.split('.').pop()?.toLowerCase();
          const filenameLower = file.originalname.toLowerCase();
          
          if (extension === 'fgd' || filenameLower.includes('.fgd') || 
              content.includes('DELFOR') || content.includes('ORDERS') || 
              content.includes('INVOIC') || content.includes('DESADV') || 
              content.includes('UNB+')) {
            // EDIFACT file (DELFOR, ORDERS, INVOIC, DESADV)
            parsedData = parseEDIFACT(content, file.originalname);
            if (parsedData.length === 0) {
              errors.push('No data could be extracted from this EDIFACT file. Please check the file format.');
            }
          } else if (extension === 'txt') {
            // Text file - try EDIFACT parser
            parsedData = parseTextFile(content, file.originalname);
            if (parsedData.length === 0) {
              errors.push('No EDIFACT data found in this text file.');
            }
          } else if (extension === 'pdf') {
            // PDF file
            parsedData = await parsePDF(file.buffer, file.originalname);
            if (parsedData.length === 0) {
              errors.push('No data could be extracted from this PDF file. Please ensure it contains reference, date, and quantity information.');
            }
          } else if (extension === 'doc' || extension === 'docx') {
            // Word document
            parsedData = await parseWord(file.buffer, file.originalname);
            if (parsedData.length === 0) {
              errors.push('No data could be extracted from this Word document. Please ensure it contains reference, date, and quantity information.');
            }
          } else {
            // Try to parse as EDIFACT anyway
            parsedData = parseTextFile(content, file.originalname);
            if (parsedData.length === 0) {
              errors.push('Unsupported file type. Please use EDIFACT (.FGD) or TXT files.');
            }
          }
        } catch (error) {
          errors.push(`Error parsing file: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }

        return {
          fileName: file.originalname,
          fileSize: file.size,
          parsedData,
          errors: errors.length > 0 ? errors : undefined,
        };
      }));

      res.json(results);
    } catch (error) {
      console.error('Upload error:', error);
      res.status(500).json({ error: 'Failed to process files' });
    }
  });

  // Download processed data as Excel or CSV
  app.post('/api/download', async (req, res) => {
    try {
      const { mode, format, files } = req.body;

      if (!files || files.length === 0) {
        return res.status(400).json({ error: 'No data to download' });
      }

      // Combine all data
      let allData: ParsedDataRow[] = [];
      
      if (mode === 'combined') {
        // Combine all files into one dataset
        files.forEach((file: { fileName: string, data: ParsedDataRow[] }) => {
          allData = allData.concat(file.data);
        });
      } else {
        // For separate mode, just use the first file (frontend handles individual downloads)
        allData = files[0].data;
      }

      if (format === 'excel') {
        // Create Excel file with only Reference, Date, and Quantity columns
        const worksheet = XLSX.utils.json_to_sheet(
          allData.map(row => ({
            Reference: row.reference,
            Date: row.date,
            Quantity: row.quantity,
          }))
        );

        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Data');

        const buffer = XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });

        res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader('Content-Disposition', 'attachment; filename=processed_data.xlsx');
        res.send(buffer);
      } else if (format === 'csv') {
        // Create CSV file with only Reference, Date, and Quantity columns
        const csvData = allData.map(row => ({
          Reference: row.reference,
          Date: row.date,
          Quantity: row.quantity,
        }));

        const csv = Papa.unparse(csvData);

        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', 'attachment; filename=processed_data.csv');
        res.send(csv);
      } else {
        res.status(400).json({ error: 'Invalid format' });
      }
    } catch (error) {
      console.error('Download error:', error);
      res.status(500).json({ error: 'Failed to generate download' });
    }
  });

  const httpServer = createServer(app);

  return httpServer;
}
