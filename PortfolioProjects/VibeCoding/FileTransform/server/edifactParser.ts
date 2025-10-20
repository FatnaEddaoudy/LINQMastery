import type { ParsedDataRow } from '@shared/schema';

export function parseEDIFACT(content: string, fileName: string): ParsedDataRow[] {
  // EDIFACT format: UNA header defines separators, OR defaults to apostrophe
  // Many malformed files claim one terminator but use another (e.g., space in UNA but newlines in practice)
  
  let segmentTerminator: string;
  
  if (content.startsWith('UNA:')) {
    // UNA defines: component sep, element sep, decimal mark, release char, reserved, segment terminator
    const unaHeader = content.substring(0, 9);
    if (unaHeader.length >= 9) {
      const unaTerminator = unaHeader[8]; // Position 8 is segment terminator
      // Malformed files often specify space/whitespace but use newlines - ignore those
      if (unaTerminator && unaTerminator !== ' ' && unaTerminator !== '\n' && unaTerminator !== '\r') {
        segmentTerminator = unaTerminator;
      } else {
        // UNA specified whitespace - likely malformed, use newline
        segmentTerminator = '\n';
      }
    } else {
      segmentTerminator = "'"; // Incomplete UNA, use default
    }
  } else {
    // No UNA header - use standard EDIFACT apostrophe terminator
    segmentTerminator = "'";
  }
  
  // Split on segment terminator
  const segments = content.split(segmentTerminator).map(s => s.trim()).filter(s => s.length > 0);
  
  const results: ParsedDataRow[] = [];
  
  let currentReference = '';
  let currentDate = '';
  let currentQuantity = '';
  let messageType = '';

  // Detect message type from UNH segment
  for (const segment of segments) {
    if (segment.startsWith('UNH+')) {
      const parts = segment.split('+');
      if (parts.length >= 3) {
        const msgTypePart = parts[2].split(':')[0];
        messageType = msgTypePart || '';
      }
      break;
    }
  }

  const tryEmitRow = () => {
    if (currentReference && currentDate && currentQuantity) {
      results.push({
        reference: currentReference,
        date: currentDate,
        quantity: currentQuantity,
        fileName,
      });
      // Reset quantity and date for next row, keep reference as it may be shared
      currentQuantity = '';
      currentDate = '';
      return true;
    }
    return false;
  };

  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];
    
    // Extract reference from LIN segment (e.g., "LIN+++2358538:IN" or "LIN+1++4260304623843:EN")
    if (segment.startsWith('LIN+')) {
      // Start of new line item - try to emit any pending data first
      tryEmitRow();
      
      // Reset for new line item
      currentReference = '';
      currentDate = '';
      currentQuantity = '';
      
      const parts = segment.split('+');
      if (parts.length >= 4) {
        const refPart = parts[3].split(':')[0];
        if (refPart) {
          currentReference = refPart;
        }
      }
    }
    
    // Alternative: Extract reference from PIA segment (e.g., "PIA+1+2358538")
    if (segment.startsWith('PIA+')) {
      const parts = segment.split('+');
      if (parts.length >= 3) {
        const refPart = parts[2].split(':')[0];
        if (refPart && !currentReference) {
          currentReference = refPart;
        }
      }
    }
    
    // Extract dates based on message type
    // DELFOR: DTM+11 (delivery date)
    // ORDERS: DTM+2 (requested delivery date)
    // DESADV: DTM+11 (despatch date) or DTM+69 (delivery date) 
    // INVOIC: DTM+137 (invoice date) or DTM+35 (delivery date)
    
    let datePatterns: string[] = [];
    switch (messageType) {
      case 'DELFOR':
        datePatterns = ['DTM+11'];
        break;
      case 'ORDERS':
        datePatterns = ['DTM+2'];
        break;
      case 'DESADV':
        datePatterns = ['DTM+11', 'DTM+69'];
        break;
      case 'INVOIC':
        datePatterns = ['DTM+137', 'DTM+35'];
        break;
      default:
        // Unknown message type - try common patterns
        datePatterns = ['DTM+11', 'DTM+2', 'DTM+69', 'DTM+137', 'DTM+35'];
    }
    
    for (const pattern of datePatterns) {
      if (segment.startsWith(pattern)) {
        const parts = segment.split(':');
        if (parts.length >= 2) {
          const dateStr = parts[1];
          // Format: YYYYMMDD -> YYYY-MM-DD
          if (dateStr.length === 8) {
            currentDate = `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`;
          } else if (dateStr.length >= 12) {
            // CCYYMMDDHHMM format - extract just the date
            currentDate = `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`;
          } else {
            currentDate = dateStr;
          }
          // Try to emit if we have all data now
          tryEmitRow();
        }
        break;
      }
    }
    
    // Extract quantity based on message type
    // DELFOR: QTY+113 (delivery quantity)
    // ORDERS: QTY+21 (ordered quantity)
    // DESADV: QTY+12 (despatch quantity)
    // INVOIC: QTY at line level (invoiced quantity - can vary)
    
    let qtyPatterns: string[] = [];
    switch (messageType) {
      case 'DELFOR':
        qtyPatterns = ['QTY+113'];
        break;
      case 'ORDERS':
        qtyPatterns = ['QTY+21'];
        break;
      case 'DESADV':
        qtyPatterns = ['QTY+12'];
        break;
      case 'INVOIC':
        qtyPatterns = ['QTY+47', 'QTY+46']; // Invoiced quantity, allocated quantity
        break;
      default:
        // Unknown message type - try common patterns
        qtyPatterns = ['QTY+113', 'QTY+21', 'QTY+12', 'QTY+47'];
    }
    
    for (const pattern of qtyPatterns) {
      if (segment.startsWith(pattern)) {
        const parts = segment.split(':');
        if (parts.length >= 2) {
          currentQuantity = parts[1];
          // Try to emit if we have all data now
          tryEmitRow();
        }
        break;
      }
    }
    
    // Reset reference when we encounter a new message (UNH segment)
    if (segment.startsWith('UNH+')) {
      tryEmitRow();
      currentReference = '';
      currentDate = '';
      currentQuantity = '';
    }
  }
  
  // Try to emit any remaining data at the end
  tryEmitRow();
  
  return results;
}

export function parseTextFile(content: string, fileName: string): ParsedDataRow[] {
  // For plain text files, try to parse EDIFACT format
  // If it looks like EDIFACT (has UNA, UNB, etc.), use the EDIFACT parser
  if (content.includes('UNA:') || content.includes('UNB+') || content.includes('DELFOR') || content.includes('LIN+')) {
    return parseEDIFACT(content, fileName);
  }
  
  // Otherwise, return empty array (could be extended to support other formats)
  return [];
}
