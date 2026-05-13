# CHANGELOG — Project HEIMDALL

## [2026-05-13] v1.2 — Mobile Fixes, Tab Refactor, Media Gallery

- **Refactor: Detail panel 5 tabs → 3 tabs** (INCIDENT / EVIDENCE & SOURCES / ANALYSIS)
  - Cleaner information architecture; EVIDENCE tab auto-redacts when no data exists
  - New `buildTabsThree()` separates data building from rendering
  - `hasNoEvidenceAndSourcesData()` heuristic for evidence tab redaction
- **Fix: Mobile detail panel empty** — add `flex-direction: column` + `z-index` for stacking context
- **Feat: Mobile zoom buttons** — 44px touch targets for mobile map controls
- **Enrichment: CAN-055 Vulcan County** — add full case details
- **Fix: Guard null/undefined fields** — protect UI from missing location, shape, contact data
- **Media gallery: 13 images** — added from Drive, linked to case evidence tabs
- **Clean dead links** — removed broken reference links from case data
- **Remove stale backup** — delete `docs/index.html.bak-20260512-2201`

## [2026-05-13] v1.1.1 — Date Header Fix

- Fix case date headers in detail panel rendering

## [2026-05-11] v1.1 — Narrative Integration & Docs

- Embedded all 54 case markdown narratives into `docs/narratives.js` (267KB)
- Added `marked.js` CDN dependency for client-side markdown rendering
- Rewrote `openDetail()` to dynamically parse and inject case narratives
- Sidebar clicks now sync with detail panel (click case in list = zoom map + open panel)
- Created `docs/CHANGELOG.md`
- Created `docs/ISSUE_TRACKER.md`
- Created `AGENTS.md` (agent operating instructions for future work)

## [2025-05-11] v1.0 — Initial Public Release

- 54 cases covering 1662-2025 Canadian UFO/AAP sightings
- Interactive Leaflet.js map with 54 geolocated markers
- Timeline slider (filter by year range)
- Sidebar with tier (A/B/C) and encounter type filters
- Detail panel with metadata grid, evidence blocks, and source citations
- Classified-aesthetic styling: paper tones, typewriter fonts, Manila folder UI
- Tier system with color-coded markers
- Hynek classification system (CE1-CE4, NL, RV, DD)
- 4 research tracks defined (NUFORC, CADORS, MUFON, RCMP)
- `data/cases/` directory with 54 rich markdown case files
- `data/research_needs.json` for gap tracking
- GitHub Pages deployment from `docs/` folder
- Initial documentation: README, RESEARCH_WORKFLOW

## [Pre-release] Data Gathering

- Compiled original 50-row `raw_sightings.csv` from source material
- Researched and wrote 54 case file narratives from:
  - NUFORC archives
  - CADORS reports
  - RCMP Form 63 and field reports
  - Project Magnet files
  - MUFON records
  - DND declassified files
  - Jesuit Relations (historical records)
  - Local press archives and witness accounts
- Added 4 additional cases (CAN-051 to CAN-054) from 2023 cross-border flap with Canadian overlap
- Structured data with Hynek classifications, tier ratings, witness counts, shapes, durations
- Created `research_needs.json` with structured research gap tracking per case
