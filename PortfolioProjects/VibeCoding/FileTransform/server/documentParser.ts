import mammoth from 'mammoth';
import type { ParsedDataRow } from '@shared/schema';

// pdf-parse doesn't have ES module exports, use dynamic import
const getPdfParse = async () => {
  const module = await import('pdf-parse');
  return (module as any).default || module;
};

interface ExtractedData {
  reference?: string;
  date?: string;
  quantity?: string;
}

/**
 * Extract structured data from plain text using regex patterns
 */
function extractDataFromText(text: string): ExtractedData[] {
  const results: ExtractedData[] = [];
  
  // Common patterns for reference numbers (alphanumeric, could be product codes, order numbers, etc.)
  const refPatterns = [
    /(?:ref(?:erence)?|item|product|sku|order)[\s:#]*([A-Z0-9]{5,15})/gi,
    /\b([A-Z]{2,5}[-]?\d{5,10})\b/g, // Pattern like ABC-12345 or ABC12345
    /\b(\d{7,10})\b/g, // Plain 7-10 digit numbers
  ];
  
  // Date patterns (various formats)
  const datePatterns = [
    /(\d{4}[-\/]\d{2}[-\/]\d{2})/g, // YYYY-MM-DD or YYYY/MM/DD
    /(\d{2}[-\/]\d{2}[-\/]\d{4})/g, // DD-MM-YYYY or MM-DD-YYYY
    /(\d{8})/g, // YYYYMMDD
  ];
  
  // Quantity patterns
  const qtyPatterns = [
    /(?:qty|quantity|amount|count|units?)[\s:#]*(\d+)/gi,
    /\b(\d{1,6})\s*(?:pcs?|pieces?|units?|ea|each)/gi,
  ];
  
  // Extract potential references
  const references: string[] = [];
  for (const pattern of refPatterns) {
    const matches = Array.from(text.matchAll(pattern));
    for (const match of matches) {
      if (match[1]) {
        references.push(match[1]);
      }
    }
  }
  
  // Extract potential dates
  const dates: string[] = [];
  for (const pattern of datePatterns) {
    const matches = Array.from(text.matchAll(pattern));
    for (const match of matches) {
      if (match[1]) {
        // Normalize date format to YYYY-MM-DD
        let dateStr = match[1];
        if (dateStr.length === 8 && /^\d{8}$/.test(dateStr)) {
          // YYYYMMDD format
          dateStr = `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`;
        }
        dates.push(dateStr);
      }
    }
  }
  
  // Extract potential quantities
  const quantities: string[] = [];
  for (const pattern of qtyPatterns) {
    const matches = Array.from(text.matchAll(pattern));
    for (const match of matches) {
      if (match[1]) {
        quantities.push(match[1]);
      }
    }
  }
  
  // Try to match references with dates and quantities
  // Simple approach: if we have same number of each, pair them up
  const maxLength = Math.max(references.length, dates.length, quantities.length);
  
  for (let i = 0; i < maxLength; i++) {
    const data: ExtractedData = {
      reference: references[i] || references[0],
      date: dates[i] || dates[0],
      quantity: quantities[i] || quantities[0],
    };
    
    // Only add if we have at least reference and one other field
    if (data.reference && (data.date || data.quantity)) {
      results.push(data);
    }
  }
  
  return results;
}

/**
 * Parse PDF file to extract reference, date, and quantity data
 */
export async function parsePDF(buffer: Buffer, fileName: string): Promise<ParsedDataRow[]> {
  try {
    const pdfParse = await getPdfParse();
    const pdf = await pdfParse(buffer);
    const text = pdf.text;
    
    const extracted = extractDataFromText(text);
    
    return extracted.map(item => ({
      reference: item.reference || '',
      date: item.date || '',
      quantity: item.quantity || '',
      fileName,
    })).filter(row => row.reference && row.date && row.quantity);
  } catch (error) {
    console.error('PDF parsing error:', error);
    return [];
  }
}

/**
 * Parse Word document (.docx) to extract reference, date, and quantity data
 */
export async function parseWord(buffer: Buffer, fileName: string): Promise<ParsedDataRow[]> {
  try {
    const result = await mammoth.extractRawText({ buffer });
    const text = result.value;
    
    const extracted = extractDataFromText(text);
    
    return extracted.map(item => ({
      reference: item.reference || '',
      date: item.date || '',
      quantity: item.quantity || '',
      fileName,
    })).filter(row => row.reference && row.date && row.quantity);
  } catch (error) {
    console.error('Word parsing error:', error);
    return [];
  }
}
