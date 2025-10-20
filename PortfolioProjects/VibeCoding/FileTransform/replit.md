# EDIFACT File Processor

## Overview

This is a web-based EDIFACT file processing application that allows users to upload EDIFACT, PDF, TXT, and Word files to extract structured data (reference numbers, dates, and quantities) and export the results to Excel or CSV format. The application provides a clean, Material Design-inspired interface for file upload, data preview, and export operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: React with TypeScript and Vite
- **UI Library**: Shadcn/ui components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom design system (New York variant)
- **State Management**: React hooks with TanStack Query for server state
- **Routing**: Wouter for lightweight client-side routing
- **File Handling**: react-dropzone for drag-and-drop upload interface

**Design System**:
- Material Design-inspired approach optimized for data-focused applications
- Custom color palette with deep blue primary color (216 100% 45%) for professional appearance
- Support for both light and dark modes
- Typography using Inter font family for UI and JetBrains Mono for data display
- Emphasis on clarity, efficient workflow, and minimal friction

**Key Frontend Components**:
- `FileUploadZone`: Drag-and-drop file upload interface supporting multiple file types
- `DataPreviewTable`: Displays extracted data in tabular format
- `FileCard`: Individual file management with preview and download options
- `ProcessingModeToggle`: Switch between combined or separate file export modes
- `StatusIndicator`: Visual feedback for processing states

### Backend Architecture

**Runtime**: Node.js with Express.js
- **Language**: TypeScript with ES modules
- **Build Tool**: esbuild for production bundling
- **Development**: tsx for TypeScript execution in development
- **File Upload**: Multer middleware with in-memory storage (10MB limit)

**API Design**:
- RESTful endpoint structure
- Single `/api/upload` POST endpoint for file processing
- Request/response validation using Zod schemas
- Error handling with proper HTTP status codes

**File Processing Pipeline**:
1. Accept multiple files via multipart/form-data
2. Detect file type based on extension and content
3. Parse EDIFACT segments using custom parser
4. Extract reference numbers (from LIN segments), dates (from DTM segments), and quantities (from QTY segments)
5. Return structured data with error reporting for unparseable files

**EDIFACT Parser Logic**:
- Segments delimited by apostrophes (')
- Line items identified by LIN+ prefix
- Date extraction from DTM segments
- Quantity extraction from QTY segments
- Flexible parsing to handle variations in EDIFACT format

**Export Functionality**:
- Excel export using xlsx library
- CSV export using papaparse library
- Support for combined (single file) or separate (per upload) export modes

### External Dependencies

**Frontend Libraries**:
- **@tanstack/react-query** (v5.60.5): Server state management and caching
- **react-dropzone**: File upload UI with drag-and-drop
- **wouter**: Lightweight routing solution
- **@radix-ui/***: Headless UI component primitives for accessibility
- **class-variance-authority**: Type-safe component variants
- **tailwindcss**: Utility-first CSS framework

**Backend Libraries**:
- **express**: Web server framework
- **multer**: Multipart form data handling for file uploads
- **xlsx**: Excel file generation
- **papaparse**: CSV parsing and generation
- **zod**: Runtime type validation and schema definition
- **drizzle-orm**: SQL query builder (configured but storage currently in-memory)
- **@neondatabase/serverless**: Serverless Postgres driver (configured for future use)

**Development Tools**:
- **vite**: Frontend build tool and dev server
- **typescript**: Type safety across the stack
- **esbuild**: Fast JavaScript bundler for production builds
- **tsx**: TypeScript execution engine for development

**Database Configuration** (Prepared but not actively used):
- PostgreSQL via Neon serverless driver
- Drizzle ORM for type-safe database queries
- Schema defined in `shared/schema.ts`
- Migrations configured in `drizzle.config.ts`
- Current implementation uses in-memory storage (`MemStorage` class)

**Session Management** (Configured):
- connect-pg-simple for PostgreSQL session storage (when database is enabled)

**Design Resources**:
- Google Fonts CDN: Inter and JetBrains Mono font families
- Material Design principles adapted for data-focused workflows