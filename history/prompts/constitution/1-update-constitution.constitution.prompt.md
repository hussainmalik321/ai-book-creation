---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Dell
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
You are operating strictly within the Spec-Kit Plus workflow.

This project MUST follow the exact phase order:
1. /sp.specify
2. /sp.plan
3. /sp.tasks
4. /sp.implement

Skipping, merging, or improvising phases is NOT allowed.

================================
PROJECT IDENTITY
================================
This is a SPEC-DRIVEN BOOK PRODUCT, not documentation.

Tech Stack:
- Spec-Kit Plus (primary driver)
- Docusaurus (latest)
- Claude Code (for implementation)
- GitHub Pages (deployment)

================================
GLOBAL RULES (APPLY TO ALL PHASES)
================================
- All decisions originate from specs
- No implementation without approved specs
- No UI decisions without explicit spec
- No default Docusaurus UI usage
- Everything must be responsive by design

================================
UI & UX CONSTITUTION
================================
Docusaurus is ONLY an engine.
The UI must be completely custom.

Mandatory:
- Custom layout components
- Custom navigation system
- Custom typography scale
- Custom color system
- Custom reading experience

Forbidden:
- Default Docusaurus theme look
- Default sidebar styles
- Default fonts
- Docs-style appearance

The product must feel like:
- A premium book
- A modern learning platform
- A polished SaaS editorial experience

================================
RESPONSIVENESS LAW
================================
Mobile-first is mandatory.

- Mobile: pure reading focus, zero clutter
- Tablet: enhanced spacing + navigation
- Desktop: immersive book layout

No layout may break at any viewport.

================================
SPEC PHASE CONTRACTS
================================

/sp.specify
- Define WHAT is being built
- Define success criteria
- Define book scope, audience, tone
- Define UI philosophy (not code)
- No technical implementation details

/sp.plan
- Translate specs into architecture
- Define folder structure
- Define component strategy
- Define theming & override strategy
- Define GitHub Pages constraints

/sp.tasks
- Break plan into atomic tasks
- Each task must be independently executable
- No vague or combined tasks
- Tasks must map 1-to-1 with implementation steps

/sp.implement
- Follow tasks EXACTLY
- Use Claude Code conventions
- No deviation from specs or plan
- No extra features unless specified
- Clean, production-ready code only

================================
CONTENT GOVERNANCE
================================
- Book content must be:
  - Structured
  - Authoritative
  - Modern
  - Tool-aware but concept-first
- No filler content
- No ge
```

## Response snapshot

Created a comprehensive constitution for the AI Book Creation project based on the Spec-Kit Plus workflow requirements. The constitution establishes core principles for spec-driven development, custom UI/UX excellence, mobile-first responsiveness, premium content quality, technical stack adherence, and implementation discipline. It also defines content governance, development workflow, UI/UX requirements, and governance rules.

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles and governance rules
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive constitution
- 🔁 Next prompts: Proceed to /sp.specify phase to define the book specifications
- 🧠 Reflection: Constitution establishes clear governance framework for the AI book creation project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification phase with /sp.specify