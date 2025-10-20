# HR CV Matching Application - Design Guidelines

## Design Approach: Professional Productivity System
**Selected Framework:** Modern HR Platform Design (inspired by Greenhouse, Lever, BambooHR)
**Rationale:** This is a data-intensive productivity tool requiring clarity, efficiency, and professional presentation of complex comparison data.

## Core Design Principles
1. **Data Clarity First:** Information hierarchy over visual flourish
2. **Efficient Workflows:** Minimize clicks, maximize visibility
3. **Professional Trust:** Clean, credible interface for HR decision-making
4. **Scan-ability:** Easy visual parsing of candidate rankings and scores

## Color Palette

**Light Mode:**
- Primary: 220 75% 45% (Professional Blue)
- Background: 0 0% 98% (Soft White)
- Surface: 0 0% 100% (Pure White)
- Text Primary: 220 15% 20% (Deep Charcoal)
- Text Secondary: 220 10% 45% (Medium Gray)
- Success: 145 60% 45% (Match indicator)
- Border: 220 15% 88% (Subtle dividers)

**Dark Mode:**
- Primary: 220 75% 55% (Lighter Blue)
- Background: 220 15% 12% (Dark Slate)
- Surface: 220 12% 16% (Card Background)
- Text Primary: 220 10% 95% (Off White)
- Text Secondary: 220 10% 65% (Light Gray)
- Success: 145 55% 55% (Match indicator)
- Border: 220 12% 22% (Dark dividers)

## Typography
- **Primary Font:** Inter (Google Fonts) - clean, highly legible
- **Headings:** 600-700 weight, tracking tight
- **Body:** 400-500 weight, tracking normal
- **Data/Scores:** 600 weight tabular numbers for alignment
- **Hierarchy:** h1: 2.25rem, h2: 1.875rem, h3: 1.5rem, body: 1rem, small: 0.875rem

## Layout System
**Spacing Primitives:** Tailwind units of 4, 6, 8, 12, 16 (p-4, gap-6, mb-8, py-12, mt-16)
- Consistent padding: p-6 for cards, p-8 for main containers
- Vertical rhythm: mb-8 for section spacing, gap-4 for list items
- Container max-width: max-w-7xl for main content area

## Component Library

**Upload Interface:**
- Large drag-drop zone (min-h-64) with dashed border and hover state
- File type indicators (PDF/Word icons)
- Batch upload progress with individual file status
- Clear "Remove" actions for each uploaded file

**Job Description Input:**
- Clean textarea or rich text editor (h-48 minimum)
- Character count indicator
- Save/draft functionality prominent

**Results Dashboard:**
- Two-view toggle: List View (ranked) / Grid View (cards)
- Sortable table columns: Name, Match Score, Experience, Education
- Color-coded score indicators: 80%+ green, 60-79% yellow, <60% gray
- Quick action buttons: View Details, Download CV, Compare

**Candidate Cards:**
- Profile section: name, photo placeholder, contact info
- Prominent match percentage (large, bold, color-coded)
- Key skills tags (max 6 visible, +N more indicator)
- Experience summary (2-3 lines)
- Primary CTA: "View Full Comparison"

**Side-by-Side Comparison:**
- Split-screen layout (50/50 on desktop, stacked on mobile)
- Job requirements on left, candidate qualifications on right
- Visual indicators: checkmarks for matches, circles for partial, X for missing
- Sticky headers during scroll
- Highlight matching keywords in yellow

**Navigation:**
- Top navbar: Logo left, Upload New / View Results / Settings right
- Breadcrumb trail for deep navigation
- Back buttons contextually placed

**Data Display:**
- Tables with alternating row colors for readability
- Percentage bars inline with scores
- Expandable rows for detailed information
- Pagination for 10/25/50 results per page

**Forms & Inputs:**
- Consistent height (h-11 for inputs)
- Clear labels above fields
- Validation states (red border for errors, green for success)
- Helper text below inputs in text-sm

## Animations
**Minimal, Purposeful Motion:**
- Upload progress: Smooth progress bar fill (transition-all duration-300)
- Card hover: Subtle lift (hover:shadow-lg hover:-translate-y-1)
- Score reveal: Number count-up animation on initial load only
- No parallax, no scroll-triggered animations

## Images
**Profile Placeholders:**
- Circular avatar placeholders (w-12 h-12 for list view, w-20 h-20 for detail view)
- Use initials with colored backgrounds when no photo available
- Professional color palette for placeholder backgrounds

**Icons:**
- Heroicons for UI elements (upload, download, check, X, info)
- File type icons for CV indicators
- Consistent 5-6 sizing (w-5 h-5 for inline, w-6 h-6 for prominent)

**No Hero Image:** This is a utility application - launch directly into functionality

## Accessibility & Interaction
- Minimum touch target: 44x44px for all interactive elements
- Focus states: 2px ring offset in primary color
- ARIA labels for all icon-only buttons
- Keyboard navigation: Tab order follows visual hierarchy
- Screen reader announcements for dynamic score updates
- High contrast mode support for all text/background combinations

## Responsive Breakpoints
- Mobile (<640px): Single column, stacked comparisons, simplified tables
- Tablet (640-1024px): Two-column grids, condensed side-by-side
- Desktop (1024px+): Full multi-column layouts, split-screen comparisons