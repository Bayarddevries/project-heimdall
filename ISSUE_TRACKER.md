# ISSUE TRACKER — Project HEIMDALL

A markdown-based issue tracker for Project HEIMDALL. Migrate to GitHub Issues when ready.

---

## Format

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-001 | Short title | P0-P2 | Open/Done/Blocked | One-sentence description |

---

## Open Issues

### Data

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-050 | NUFORC data cross-reference | P1 | Open | Mine NUFORC for additional Canadian reports to expand dataset beyond 56 |
| H-051 | CADORS data mining | P1 | Open | Query CADORS for aviation-related UFO reports with radar confirmation |
| H-052 | MUFON case files | P1 | Open | Extract MUFON cases with Canadian relevance |
| H-053 | RCMP Form 63 deep scan | P0 | Blocked | Full scan of RCMP Form 63 for all case physical evidence details |
| H-054 | Fill research_needs.json gaps | P1 | Open | Execute tasks in research_tasks.txt to fill missing fields |

### Bug / Maintenance

| ID | Title | Priority | Status | Description |
|----|-------|----------|--------|-------------|
| H-200 | narratives.js sync automation | P1 | Open | Automate narrative regeneration on commit (CI/CD hook) |

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
| H-010 | Paper grain background | P1 | 2026-05-13 | Enhanced grain overlay — 3 noise layers, increased opacity |
| H-011 | Edge wear + inner glow | P2 | 2026-05-14 | Paper edge shading, inner glow on containers, case-item edge wear |
| H-012 | Coffee stains + foxing | P2 | 2026-05-13 | 5 coffee stain elements + foxing overlay on background |
| H-013 | Offset/scanned text rotation | P1 | 2026-05-13 | Scan-angle classes with translate offset for photocopy feel |
| H-014 | Staple/paperclip accents | P1 | 2026-05-13 | 3D staple graphic on fc-h3 section headers |
| H-015 | Handwritten marginalia | P1 | 2026-05-13 | Enhanced handnote with pencil icon, .agent-note class |
| H-016 | Die-cut folder tabs | P0 | 2026-05-13 | Staggered tab navigation with notch illusion and active pop-out |
| H-017 | Dymo label UI elements | P2 | 2026-05-13 | Dymo label maker style for case numbers, dates, classification headers |
| H-018 | Brass prong / punch binding | P2 | 2026-05-13 | Two-hole punch + brass fastener graphics on inner document pages |
| H-019 | Post-it note buttons | P1 | 2026-05-13 | Post-it note style buttons with fold highlight and press states |
| H-020 | CONFIDENTIAL rubber stamp | P1 | 2026-05-13 | Red stamp graphic with hover + active press states |
| H-021 | Hand-drawn checkboxes | P2 | 2026-05-13 | X marks in hand-drawn squares for filter toggles |
| H-022 | Paperclip toggle switches | P2 | 2026-05-13 | Metal paperclip slides between positions as toggle UI element |
| H-030 | Polaroid photo effect | P0 | 2026-05-13 | Aged bg, thicker borders, stronger filter, hover enhance, tape corners |
| H-031 | Scotch tape corner mounts | P1 | 2026-05-13 | Merged into H-030 polaroid effect — tape enhanced there |
| H-040 | Responsive mobile layout | P1 | 2026-05-14 | Mobile touch targets fixed to 44px, timeline z-index, header readability |
| H-055 | Media/photograph collection | P0 | 2026-05-14 | 12+ public-domain images from Wikimedia Commons for 11 cases |
| H-056 | Cross-reference witness names | P2 | 2026-05-15 | Witness pattern matches by type (RCMP/Military/Police/Pilot/Civilian) |
| H-060 | Geolocation verification | P1 | 2026-05-14 | Full Nominatim audit of 56 cases; 3 coordinates corrected |
| H-061 | Date disambiguation | P2 | 2026-05-15 | Standardized all dates to ISO format with precision-aware display |
| H-100 | Map search by location | P1 | 2026-05-13 | Search box filters sidebar + map markers by location, shape, year, ID |
| H-101 | Case relationship graph | P2 | 2026-05-15 | Visual graph + table showing related cases by shared pattern tags |
| H-102 | Timeline mode | P1 | 2026-05-13 | Horizontal timeline view with tier-colored dots, hover labels, adaptive years |
| H-103 | Print/export case file | P2 | 2026-05-14 | Print-optimized CSS + print button in detail panel |
| H-104 | Classified overlay toggle | P2 | 2026-05-14 | Toggle between classified (redacted) and declassified views |
| H-105 | Sound effects | P3 | 2026-05-15 | Procedural Web Audio: paper rustle, stamp thud, staple click, UI click |
| H-106 | Dark mode (night ops) | P2 | 2026-05-14 | Red-lit night operations theme with toggle button, localStorage persistence |
| H-107 | Share/link to specific case | P1 | 2026-05-13 | URL hash-based deep linking (#CAN-012 opens that case directly) |
| H-201 | Reduce narratives.js file size | P2 | 2026-05-15 | Minified narratives.js generation in pipeline (narratives.min.js) |
| H-202 | Fix cases-all.json generation | P1 | 2026-05-15 | Verified regex frontmatter stripping works on all 56 files (no YAML parser needed) |

---

## Stats

| Metric | Count |
|--------|-------|
| Total Issues | 42 |
| Open | 5 |
| Completed | 36 |
| Blocked | 1 |
| P0 Critical | 1 |
| P1 High | 3 |
| P2 Medium | 1 |
