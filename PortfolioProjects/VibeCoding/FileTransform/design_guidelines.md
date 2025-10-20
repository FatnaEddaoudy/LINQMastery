# Design Guidelines: EDIFACT File Processing Application

## Design Approach

**Selected Framework**: Material Design System (data-focused variant)
**Rationale**: Utility-focused application requiring clear hierarchy, robust data display, and efficient file processing workflow. Material Design provides excellent patterns for upload interfaces, data tables, and status indicators.

**Core Principles**:
- Clarity over decoration
- Efficient workflow with minimal friction
- Clear visual feedback for processing states
- Professional, trustworthy appearance

---

## Color Palette

### Light Mode
- **Primary**: 216 100% 45% (Deep Blue - professional, trustworthy)
- **Primary Hover**: 216 100% 38%
- **Surface**: 0 0% 100% (Pure white)
- **Surface Secondary**: 220 14% 96% (Light gray for upload zones)
- **Border**: 220 13% 91%
- **Text Primary**: 222 47% 11%
- **Text Secondary**: 215 16% 47%
- **Success**: 142 76% 36% (Green for completed processing)
- **Error**: 0 84% 60% (Red for parsing errors)
- **Warning**: 38 92% 50% (Amber for format warnings)

### Dark Mode
- **Primary**: 216 100% 60%
- **Primary Hover**: 216 100% 68%
- **Surface**: 222 47% 11% (Dark navy)
- **Surface Secondary**: 217 33% 17% (Lighter dark for upload zones)
- **Border**: 217 19% 27%
- **Text Primary**: 210 20% 98%
- **Text Secondary**: 217 10% 65%
- **Success**: 142 71% 45%
- **Error**: 0 72% 51%
- **Warning**: 38 100% 60%

---

## Typography

**Font Family**: 
- Primary: 'Inter', -apple-system, sans-serif (via Google Fonts CDN)
- Monospace: 'JetBrains Mono', 'Courier New', monospace (for file names and data display)

**Type Scale**:
- Headings: font-semibold, leading-tight
- Body: font-normal, leading-relaxed
- Data Tables: font-medium, leading-snug, text-sm
- File Names: font-mono, text-sm
- Labels: font-medium, text-sm, uppercase, tracking-wide

---

## Layout System

**Spacing Primitives**: Tailwind units 4, 6, 8, 12, 16
- Component padding: p-6 or p-8
- Section spacing: space-y-8 or space-y-12
- Card gaps: gap-6
- Form elements: space-y-4

**Container Strategy**:
- Max width: max-w-7xl mx-auto
- Main content: px-6 py-8
- Cards and panels: rounded-lg with subtle shadows

---

## Component Library

### A. Upload Zone
- **Large drop zone**: Dashed border (border-2 border-dashed), h-48 to h-64
- **Active state**: Primary blue border, subtle background tint
- **Icon**: Upload cloud icon (Heroicons) at 48px size
- **Supporting text**: "Drag files here or click to browse" with accepted formats list below
- **File chips**: After upload, show files as removable chips with file type icons

### B. Processing Toggle
- **Radio button group**: Horizontal layout
  - Option 1: "Combine into single file" (recommended badge)
  - Option 2: "Separate file for each upload"
- Styled with clear selection states, primary blue for selected

### C. Data Preview Table
- **Headers**: Sticky, bg-surface-secondary, font-medium, text-sm
- **Columns**: Reference (monospace), Date (formatted), Quantity (right-aligned, monospace)
- **Rows**: Alternating subtle background (zebra striping), border-b
- **Max height**: max-h-96 overflow-auto for long datasets
- **Empty state**: Centered icon + text when no data parsed

### D. Action Buttons
- **Primary**: Full blue background, white text, px-6 py-3, rounded-lg
- **Secondary**: Outline variant with primary blue border, px-6 py-3
- **Icon buttons**: p-2, rounded-md, hover:bg-surface-secondary

### E. Status Indicators
- **Processing spinner**: Primary blue, 24px size (Heroicons outline/spin)
- **Success checkmark**: Green circle background, white check icon
- **Error alert**: Red background, destructive text, with retry option
- **Progress bar**: Linear, primary blue fill, height h-1.5, rounded-full

### F. File Cards (for separate file mode)
- **Card design**: border, rounded-lg, p-4, bg-surface
- **Header**: File name (monospace, truncate), file size, delete icon
- **Preview section**: Mini table showing first 5 rows
- **Download button**: Full width, secondary style

### G. Navigation/Header
- **Simple top bar**: Logo/title left, settings/help right
- **Height**: h-16, border-b
- **Sticky**: sticky top-0 z-10

---

## Interaction Patterns

### Upload Flow
1. Empty state → Drag zone prominent
2. File hover → Border animation, background highlight
3. Files selected → Chips appear below zone, zone shrinks
4. Processing → Spinner overlay, disable interactions
5. Complete → Success animation, preview table appears

### Data Display
- **Instant preview**: Show parsed data immediately after processing
- **Expandable rows**: Click to see full EDIFACT segment data
- **Sort/filter**: Column headers clickable for basic sorting

### Download Actions
- **Single file mode**: One prominent "Download Excel" button
- **Multiple files mode**: Individual download buttons per card
- **Format toggle**: CSV/Excel switch near download button

---

## Visual Hierarchy

**Priority Levels**:
1. Upload zone (when empty) or Preview table (when populated)
2. Processing mode toggle (persistent visibility)
3. Download actions (appears after successful processing)
4. File management (remove, clear all)
5. Settings and help (header utility items)

---

## Animation Guidelines

**Minimal, Purposeful Animations**:
- Upload drop zone: Gentle scale on drag-over (scale-102)
- Processing spinner: Rotate animation only
- Success state: Single checkmark fade-in
- File chips: Slide-in from bottom (duration-200)
- NO parallax, NO scroll-driven effects, NO decorative animations

---

## Responsive Behavior

**Breakpoints**:
- Mobile (< 768px): Single column, upload zone h-40, stacked buttons
- Tablet (768px - 1024px): Full features, comfortable spacing
- Desktop (> 1024px): Optimal experience, side-by-side layouts where appropriate

**Mobile Adaptations**:
- Horizontal scrolling for data table
- Stacked action buttons (full width)
- Simplified file cards (condensed preview)

---

## Icons

**Library**: Heroicons (outline style) via CDN
- Upload: cloud-arrow-up
- Success: check-circle
- Error: exclamation-circle  
- Download: arrow-down-tray
- File types: document-text, document (generic)
- Delete: trash, x-mark