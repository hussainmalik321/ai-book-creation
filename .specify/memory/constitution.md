<!--
Sync Impact Report:
Version change: N/A → 1.0.0
List of modified principles: N/A (initial constitution)
Added sections: All principles and sections (new constitution)
Removed sections: None
Templates requiring updates: ✅ updated / ⚠ pending
Follow-up TODOs: None
-->
# AI Book Creation Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All decisions originate from specs; No implementation without approved specs; No UI decisions without explicit spec; Strict adherence to the 4-phase workflow: /sp.specify → /sp.plan → /sp.tasks → /sp.implement; Skipping, merging, or improvising phases is NOT allowed.

### II. Custom UI/UX Excellence
Docusaurus is ONLY an engine; The UI must be completely custom; Mandatory: Custom layout components, Custom navigation system, Custom typography scale, Custom color system, Custom reading experience; Forbidden: Default Docusaurus theme look, Default sidebar styles, Default fonts, Docs-style appearance; The product must feel like: A premium book, A modern learning platform, A polished SaaS editorial experience.

### III. Mobile-First Responsiveness
Mobile-first is mandatory; Mobile: pure reading focus, zero clutter; Tablet: enhanced spacing + navigation; Desktop: immersive book layout; No layout may break at any viewport; Everything must be responsive by design.

### IV. Premium Content Quality
Book content must be: Structured, Authoritative, Modern, Tool-aware but concept-first; No filler content; No generic documentation; Content must follow book philosophy, not documentation approach; Structured narrative flow required.

### V. Technical Stack Adherence
Tech Stack: Spec-Kit Plus (primary driver), Docusaurus (latest), Claude Code (for implementation), GitHub Pages (deployment); Strict adherence to specified technology stack; No unauthorized technology additions without explicit spec approval.

### VI. Implementation Discipline
Follow tasks EXACTLY during implementation; Use Claude Code conventions; No deviation from specs or plan; No extra features unless specified; Clean, production-ready code only; No implementation without corresponding task definition.

## Content Governance
- All content must be structured as a book, not documentation
- Content must have clear audience, scope, and tone defined in spec
- No default Docusaurus content or styling allowed
- Content must be authoritative and concept-first with tool awareness
- All content must be responsive and accessible across all devices

## Development Workflow
- Strict adherence to 4-phase workflow: /sp.specify → /sp.plan → /sp.tasks → /sp.implement
- All phases must be completed in order - no skipping or improvising
- Each phase must be approved before proceeding to the next
- All decisions must be traceable back to the specification
- Implementation must follow tasks exactly without deviation

## UI/UX Requirements
- Complete departure from default Docusaurus theme
- Custom design system implementation required
- Mobile-first responsive design approach
- Premium book-like reading experience
- Modern, clean, distraction-free interface
- Custom navigation and typography systems

## Governance
Constitution supersedes all other practices; All development must comply with stated principles; Amendments require formal documentation and approval; All PRs/reviews must verify constitution compliance; Implementation must strictly follow the 4-phase workflow; Deviations require explicit spec approval.

**Version**: 1.0.0 | **Ratified**: 2025-12-24 | **Last Amended**: 2025-12-24
