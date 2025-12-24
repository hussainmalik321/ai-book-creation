# Data Model: AI Book Creation Platform

## Book Entity

**Fields**:
- id: string (unique identifier)
- title: string (book title)
- description: string (book description)
- coverImage: string (path to cover image)
- author: string (author name)
- metadata: object (additional book metadata)
- chapters: Chapter[] (array of chapters in book sequence)
- navigation: NavigationTree (structure for navigation)

**Relationships**:
- Contains many Chapter entities
- Connected to NavigationTree for navigation structure

**Validation Rules**:
- Title is required
- Must have at least one chapter
- Navigation structure must be valid

## Chapter Entity

**Fields**:
- id: string (unique identifier)
- title: string (chapter title)
- slug: string (URL-friendly identifier)
- content: string (chapter content in Markdown/MDX)
- intent: string (learning intent for the chapter)
- learningOutcome: string (what user should learn)
- position: number (order in book sequence)
- prevChapterId: string (optional, previous chapter)
- nextChapterId: string (optional, next chapter)
- metadata: object (additional chapter metadata)

**Relationships**:
- Belongs to one Book entity
- Connected to previous/next chapters for navigation

**Validation Rules**:
- Title and slug are required
- Position must be unique within book
- Content must exist
- Intent and learningOutcome are required

## NavigationTree Entity

**Fields**:
- id: string (unique identifier)
- bookId: string (reference to parent book)
- structure: NavigationNode[] (hierarchical navigation structure)
- toc: TableOfContents (flat table of contents)

**Relationships**:
- Connected to one Book entity
- Contains many NavigationNode entities

## NavigationNode Entity

**Fields**:
- id: string (unique identifier)
- title: string (navigation item title)
- type: string (chapter, section, external, etc.)
- target: string (target URL or chapter ID)
- children: NavigationNode[] (optional, child navigation items)
- position: number (order in navigation)
- metadata: object (additional navigation metadata)

**Relationships**:
- Belongs to one NavigationTree
- Connected to other NavigationNode entities hierarchically

## TableOfContents Entity

**Fields**:
- id: string (unique identifier)
- bookId: string (reference to parent book)
- chapters: ChapterReference[] (ordered list of chapters)
- sections: SectionReference[] (optional, subsections)

**Relationships**:
- Connected to one Book entity
- Connected to many Chapter entities

## Design Tokens Entity

**Fields**:
- id: string (unique identifier)
- type: string (color, typography, spacing, etc.)
- name: string (token name)
- value: string (token value)
- theme: string (light, dark, or both)
- category: string (primary, secondary, etc.)

**Relationships**:
- Part of global design system

## Validation Rules Summary

1. Book must have valid title and at least one chapter
2. Chapter must have unique slug within book
3. Chapter position must be sequential within book
4. Navigation structure must match chapter structure
5. All required metadata fields must be present
6. Navigation nodes must have valid targets
7. Design tokens must have valid values and themes