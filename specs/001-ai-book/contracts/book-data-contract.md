# Data Contracts: AI Book Creation Platform

## Book Data Contract

**Purpose**: Defines the structure for book data used in the static site

**Schema**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "author": "string",
  "coverImage": "string",
  "chapters": [
    {
      "id": "string",
      "title": "string",
      "slug": "string",
      "content": "string",
      "intent": "string",
      "learningOutcome": "string",
      "position": "number",
      "prevChapterId": "string | null",
      "nextChapterId": "string | null"
    }
  ],
  "navigation": {
    "structure": [
      {
        "id": "string",
        "title": "string",
        "type": "string",
        "target": "string",
        "children": "[...children]",
        "position": "number"
      }
    ]
  }
}
```

**Validation**:
- All required fields must be present
- Chapter positions must be sequential
- Navigation targets must reference valid chapters
- Content must be valid Markdown/MDX

## Navigation Contract

**Purpose**: Defines the structure for navigation data used in the site

**Schema**:
```json
{
  "currentChapter": {
    "id": "string",
    "title": "string",
    "position": "number"
  },
  "prevChapter": {
    "id": "string",
    "title": "string",
    "position": "number"
  },
  "nextChapter": {
    "id": "string",
    "title": "string",
    "position": "number"
  },
  "tableOfContents": [
    {
      "id": "string",
      "title": "string",
      "position": "number",
      "isCurrent": "boolean"
    }
  ]
}
```

**Validation**:
- Current chapter must be valid
- Previous/next chapters must exist or be null
- Table of contents must be ordered by position
- Current chapter must be marked in TOC

## Design System Contract

**Purpose**: Defines the design tokens used throughout the site

**Schema**:
```json
{
  "colors": {
    "primary": "string",
    "secondary": "string",
    "background": "string",
    "text": "string",
    "textSecondary": "string"
  },
  "typography": {
    "fontFamily": "string",
    "fontFamilyUi": "string",
    "sizes": {
      "small": "string",
      "base": "string",
      "large": "string",
      "xl": "string",
      "h1": "string",
      "h2": "string",
      "h3": "string"
    }
  },
  "spacing": {
    "unit": "string",
    "small": "string",
    "medium": "string",
    "large": "string"
  }
}
```

**Validation**:
- All color values must be valid CSS color formats
- Font families must be valid CSS font families
- Spacing values must be valid CSS units