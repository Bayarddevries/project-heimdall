# ISSUE TRACKER — Project HEIMDALL

A markdown-based issue tracker for Project HEIMDALL. Migrate to GitHub Issues when ready.

---

## Format

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-001 | Short title | P0-P2 | Open/Done/Blocked | One-sentence description |

---

## Open Issues

### UI / Visual Overhaul

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-010 | Paper grain background | P1 | Open | Add paper fiber/grain texture to main container and dossier panels |
| H-011 | Edge wear + inner glow | P2 | Open | Add 0.5-1px irregular borders + tan inner glow to paper containers |
| H-012 | Coffee stains + foxing | P2 | Open | Add low-opacity (5-8%) coffee ring stains and age spots to corners/background |
| H-013 | Offset/scanned text rotation | P1 | Open | Apply slight rotation (0.3-0.5deg) to text blocks/images for "human-error" photocopy feel |
| H-014 | Staple/paperclip accents | P1 | Open | Replace standard headers with staple images pinning content blocks |
| H-015 | Handwritten marginalia | P1 | Open | Add Caveat font in ballpoint blue (#0047AB) for agent notes, dates, flags in margins |
| H-016 | Die-cut folder tabs | P0 | Open | Implement third-cut folder tab navigation (Left/Center/Right stagger) for section switching |
| H-030 | Polaroid photo effect | P0 | Open | Images get thick uneven white borders, high contrast, "fifth-gen photocopy" look |
| H-031 | Scotch tape corner mounts | P1 | Open | Transparent tape strips in corners of "taped" images/documents |
| H-040 | Responsive mobile layout | P1 | Open | Mobile: stacked layout with hamburger nav for folder tabs, touch-friendly targets |

### Data

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-050 | NUFORC data cross-reference | P1 | Open | Mine NUFORC for additional Canadian reports to expand dataset beyond 56 |
| H-051 | CADORS data mining | P1 | Open | Query CADORS for aviation-related UFO reports with radar confirmation |
| H-052 | MUFON case files | P1 | Open | Extract MUFON cases with Canadian relevance |
| H-053 | RCMP Form 63 deep scan | P0 | Blocked | Full scan of RCMP Form 63 for all case physical evidence details |
| H-054 | Fill research_needs.json gaps | P1 | Open | Execute tasks in research_tasks.txt to fill missing fields |
| H-055 | Media/photograph collection | P0 | Open | Gather and embed newspaper clippings, photos, sketches, VHS stills for cases |
| H-056 | Cross-reference witness names | P2 | Open | Match witnesses across multiple cases for pattern analysis |
| H-060 | Geolocation verification | P1 | Open | Verify lat/lng for all 56 cases with modern mapping tools |
| H-061 | Date disambiguation | P2 | Open | Standardize dates to ISO format where possible |

### Features

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-100 | Map search by location | P1 | Open | Add search box to filter/map to cities, provinces |
| H-101 | Case relationship graph | P2 | Open | Visual graph showing related cases (same witnesses, proximity, similar descriptions) |
| H-102 | Timeline mode | P1 | Open | Horizontal timeline view alongside map for chronological browsing |
| H-103 | Print/export case file | P2 | Open | Generate printable classified-style PDF for individual cases |
| H-104 | "Classified" overlay toggle | P2 | Open | Toggle between classified (redacted) and declassified views |
| H-105 | Sound effects | P3 | Open | Subtle paper rustle, stamp thud, staple click sounds on interaction |
| H-106 | Dark mode (night ops) | P2 | Open | Red-lit "night operations" variant of the classified aesthetic |
| H-107 | Share/link to specific case | P1 | Open | URL hash-based deep linking (#CAN-012 opens that case directly) |

### Bug / Maintenance

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-200 | narratives.js sync automation | P1 | Open | Automate narrative regeneration on commit (CI/CD hook) |
| H-201 | Reduce narratives.js file size | P2 | Open | Consider minification or gzipped delivery for 267KB file |
| H-202 | Fix cases-all.json generation | P1 | Open | YAML parser error on em-dashes; use regex extraction or fix frontmatter |

---

## Completed

| ID | Title | Priority | Completed | Description |
|----|-------|----------|-----------|-------------|
| H-001 | Initial map deployment | P0 | 2025-05-11 | 50 cases loaded on Leaflet map with basic popups |
| H-002 | Case narrative system | P0 | 2025-05-11 | Embedded 54 markdown case files with marked.js rendering |
| H-003 | Tier system (A/B/C) | P0 | 2025-05-11 | Color-coded markers and filter system |
| H-004 | Encounter type classification | P0 | 2025-05-11 | Hynek system (CE1-CE4, NL, RV, DD) implemented |
| H-005 | Timeline slider | P0 | 2025-05-11 | Filter cases by year range |
| H-006 | Detail panel | P0 | 2025-05-11 | Right-side panel with narrative, metadata, evidence |
| H-007 | Sidebar sync | P0 | 2025-05-11 | Sidebar clicks sync with map zoom and detail panel |
| H-008 | 2023 flap integration | P1 | 2025-05-11 | Added CAN-051 to CAN-054 from cross-border cases |
| H-009 | Research infrastructure | P0 | 2025-05-11 | research_needs.json, research_tasks.txt, data schema |
| H-017 | Dymo label UI elements | P2 | 2026-05-13 | Dymo label maker style for case numbers, dates, classification headers |
| H-018 | Brass prong / punch binding | P2 | 2026-05-13 | Two-hole punch + brass fastener graphics on inner document pages |
| H-019 | Post-it note buttons | P1 | 2026-05-13 | Post-it note style buttons with fold highlight and press states |
| H-020 | CONFIDENTIAL rubber stamp | P1 | 2026-05-13 | Red stamp graphic with hover + active press states |
| H-021 | Hand-drawn checkboxes | P2 | 2026-05-13 | X marks in hand-drawn squares for filter toggles |
| H-022 | Paperclip toggle switches | P2 | 2026-05-13 | Metal paperclip slides between positions as toggle UI element |

---

## Stats

| Metric | Count |
|--------|-------|
| Total Issues | 38 |
| Open | 22 |
| Completed | 16 |
| Blocked | 1 |
| P0 Critical | 5 |
| P1 High | 10 |
| P2 Medium | 7 |
