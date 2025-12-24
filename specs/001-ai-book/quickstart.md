# Quickstart Guide: AI Book Creation Platform

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager
- Git for version control

## Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## Project Structure

```
ai-book/
├── docs/                 # Book content (Markdown files)
│   ├── index.md         # Landing page (book cover)
│   ├── chapter-1.md     # First chapter
│   ├── chapter-2.md     # Second chapter
│   └── ...              # Additional chapters
├── src/                  # Custom components and styling
│   ├── components/      # React components
│   │   ├── BookLayout/  # Main book layout
│   │   ├── Navigation/  # Custom navigation
│   │   └── Typography/  # Custom typography
│   ├── css/             # Custom styles
│   │   ├── design-system.css  # Design tokens
│   │   └── book-styles.css    # Book-specific styles
│   └── theme/           # Docusaurus theme customization
├── docusaurus.config.js # Docusaurus configuration
├── babel.config.js      # Babel configuration
└── static/              # Static assets (images, fonts)
```

## Adding New Chapters

1. Create a new Markdown file in the `docs/` directory
2. Add frontmatter with required fields:
   ```markdown
   ---
   title: Chapter Title
   description: Chapter description
   position: 3  # Sequential position in book
   intent: What this chapter covers
   learningOutcome: What user will learn
   ---
   ```

3. Update the sidebar configuration in `docusaurus.config.js` to include the new chapter

## Custom Components

### Book Layout Component
- Wraps all book content with consistent layout
- Includes custom header, navigation, and footer
- Implements responsive design patterns

### Navigation Component
- Provides book-like navigation (next/previous chapters)
- Shows table of contents
- Maintains reading progress

### Typography Component
- Implements custom typography scale
- Ensures readability across devices
- Supports both reading and UI fonts

## Design System

### Colors
- Primary: Brand color for links and interactive elements
- Secondary: Supporting color for accents
- Background: Page background
- Text: Primary text color
- TextSecondary: Secondary text color

### Typography Scale
- H1: Main headings
- H2: Section headings
- H3: Subsection headings
- Base: Body text
- Small: Captions and secondary text

### Spacing System
- Unit: Base spacing unit (8px)
- Small: 0.5x unit
- Medium: 1.5x unit
- Large: 2x unit

## Deployment

### GitHub Pages
1. Build the site: `npm run build`
2. The `build/` folder contains static files ready for deployment
3. Configure GitHub Pages to serve from the `build/` folder

### Configuration
- Set `baseUrl` in `docusaurus.config.js` for subdirectory deployment
- Ensure all asset paths are relative
- Test locally before deploying

## Development Workflow

1. Create new branch for feature work
2. Add or modify content in `docs/` directory
3. Create custom components in `src/components/` as needed
4. Test locally with `npm start`
5. Build and verify with `npm run build`
6. Commit changes and create pull request