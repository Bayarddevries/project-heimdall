# CHANGELOG — Project HEIMDALL

## [2026-05-15] v2.1 — Layers Dropdown Fix

- **Fix: Layers dropdown toggle (H-207)** — Overlay toggle was broken: page loaded with lines/markers already displayed and the toggle controls didn't work. Switched from hidden `<label>`/`<input>` pairs to `<div role="button">` elements with `tabindex="0"` for proper accessibility tree interaction. Changed layers from `.addTo(map)` (immediately visible) to `L.layerGroup()` (hidden until toggled). Custom "🗺 LAYERS" header dropdown replaces old Leaflet layer control buttons at bottom-left.
- **Tier distribution**: 11 A + 7 B + 52 C (70 total)

## [2026-05-15] v2.0 — Map Overlays + Tier Upgrades

- **Feat: Toggle-able map overlays** — Three Leaflet layer groups added via `initOverlays()`:
  - ☢️ Nuclear Facilities (13 points: plants, mines, labs) — red circle markers
  - ⚔️ Military Bases (25 points: CFBs, DND, radar) — blue circle markers
  - 📡 NORAD Radar (4 radar lines + 23 stations) — green dashed lines + circle markers
- JSON files at docs/data/layers/ — loaded async via fetch, error-tolerant
- Layer control positioned bottom-left, popups show name/type/province
- **Feat: Tier upgrades (C→B)** — 4 cases upgraded:
  - CAN-059 North York Flashing Lights (10 witnesses, police video)
  - CAN-061 Terrace Hotspot (25 reports, highest per-capita)
  - CAN-066 Harbour Mille Follow-Up (RCMP, linked to CAN-045)
  - CAN-070 Yellowknife Modern (DND tracking, modern 2022)
- Tier distribution: 11 A + 7 B + 52 C (70 total)

## [2026-05-14] v1.10 — Media Enrichment Phase 3

- **Feat: Media collection phase 3 (Night Ops)** — Added 21 media files across 16 cases. Total cases with media: 37/56 (up from 21).
- New location photos for CAN-015 (4x St. Paul UFO pad), CAN-017 (Prince George), CAN-021 (Granby), CAN-022 (Langenburg), CAN-023 (Carman 1908 historical), CAN-024 (Montreal), CAN-031 (Kelowna), CAN-033 (Shelburne), CAN-034 (Montreal), CAN-035 (Diefenbunker), CAN-042 (Mont Saint-Hilaire), CAN-047 (Hamilton), CAN-048 (Vancouver), CAN-049 (Oshawa), CAN-050 (Calgary), CAN-053 (Sudbury)
- Added Project Blue Book reports (US Gov, public domain) for CAN-008 (Ramore/Clan Lake) and CAN-017 (Prince George)
- **Fix: Pipeline media_urls preservation** — Created `scripts/restore_media.py` to restore media_urls after pipeline runs. Updated AGENTS.md with documentation.
- **19 cases remain** without media (mostly remote locations / small towns without Wikipedia presence)

## [2026-05-15] v1.9 — Media Collection, CI/CD

- **Feat: Media collection phase 2 (H-055)** — Added images for 8 new cases (CAN-001, CAN-003, CAN-006, CAN-010, CAN-014, CAN-016, CAN-020, CAN-032). Total: 18 cases with media, 32 image files. Removed 264MB PDF that exceeded GitHub's file size limit.
- **Feat: CI/CD automation (H-200)** — GitHub Actions workflow `.github/workflows/regenerate.yml` auto-runs pipeline on push when case data changes. Commits regenerated narratives.js back to repo.
- **Fix: H-205** — Detail panel crash fix: witnesses field numeric type caused TypeError in buildRelationshipsTab; cast to String before toLowerCase() restores click functionality.

## [2026-05-15] v1.8 — Relationships, Dates, Sound, Witness Cross-Ref

- **Feat: Case relationship graph (H-101)** — 4th "RELATIONSHIPS" tab with visual node graph + sortable table. Shows cases connected by shared pattern tags or explicit cross-references. Fixed quote escaping in onclick handlers.
- **Feat: Date disambiguation (H-061)** — Standardized all 56 dates to ISO format (YYYY-MM-DD) with precision field (year/month/day). Human-readable display: "May 20, 1967" vs "1967" vs "October 2008".
- **Feat: Sound effects (H-105)** — Procedural Web Audio API sounds: paper rustle (case open), stamp thud (close), staple click (tab switch), UI click (filters). 🔊/🔇 toggle in top bar.
- **Feat: Witness pattern cross-reference (H-056)** — "Witness Pattern Matches" section in Relationships tab. Categorizes by RCMP/Military/Police/Pilot/Civilian Group, finds other cases with matching witness types.
- **Feat: Narratives.js minification (H-201)** — Pipeline now generates `narratives.min.js` (compact, no indentation). HTML loads minified version.
- **Fix: YAML parser verification (H-202)** — Verified regex-based frontmatter stripping works on all 56 files. No YAML parser actually used in pipeline.

## [2026-05-14] v1.7 — Edge Wear, Media, Dark Mode

- **Feat: Edge wear + inner glow (H-011)** — Paper edge shading on sidebar/detail-panel/top-bar with repeating gradients, inner glow on containers, case-item edge wear lines, filter-bar edge shadow
- **Feat: Media collection continued (H-055)** — 9 new Wikimedia Commons images for 8 cases: Falcon Lake landscape, Shag Harbour village + park, Duncan BC city hall, Portage la Prairie, L'Ancienne-Lorette church, Niagara Falls, Valcartier location map, Vulcan County AB. All media_urls updated to dict format with type classification
- **Feat: Dark mode night ops (H-106)** — Full red-lit "night operations" theme with 🌙 Night Ops toggle button. Dark backgrounds (#14100c), muted gold text (#c89060), red accents (#8b2020). Map tile filter (brightness 0.6 + sepia + hue-rotate). localStorage persistence. Mobile responsive

## [2026-05-14] v1.6 — Mobile Fixes, Geolocation Verification

- **Fix: Mobile touch targets (H-040)** — `.view-toggle` and `.timeline-close` buttons raised from 32px to 44px min-height/min-width for WCAG compliance; `.timeline-view` z-index raised to 1110 (above timeline-bar at 1100); `.timeline-header h3` font-size increased from 9px to 11px for readability
- **Fix: Geolocation verification (H-060)** — Full Nominatim API audit of all 56 cases: 38 OK (<20km), 5 CHECK (<50km, acceptable), 9 NO_RESULT (remote/water bodies), 3 corrected:
  - CAN-028 Portage la Prairie: (49.5,-98.7)→(49.9724,-98.2892) — 60km error
  - CAN-042 St-Hilaire: (45.5,-73.1)→(45.5624,-73.1919) — corrected to Mont Saint-Hilaire
  - CAN-037 l'Annonciation: (46.4,-74.8)→(46.4108,-74.782) — refined to actual road location
- **Data: CSV corrections** — Updated `canadian_ufo_sightings_v5.csv` with corrected coordinates for 3 cases

## [2026-05-13] v1.5 — Visual Polish, Timeline, Media

- **Feat: Paper grain background (H-010)** — Enhanced grain overlay with 3 noise layers (512/256/128px), increased base opacity to 0.055
- **Feat: Scan rotation (H-013)** — Added translate offset to scan-angle classes for realistic "crooked photocopy" feel on dossier content
- **Feat: Staple accents (H-014)** — 3D staple graphic on all `.fc-h3` section headers via `::before`/`::after` pseudo-elements
- **Feat: Handwritten marginalia (H-015)** — Enhanced `.handnote` with pencil icon (✎), added `.agent-note` class with dashed left border
- **Feat: Timeline mode (H-102)** — Horizontal timeline view with tier-colored dots, vertical stagger, hover labels, click-to-open, adaptive year labels
- **Feat: Media collection (H-055)** — Added 3 new public-domain images: Falcon Lake reconstruction, Steve Michalak with saucer drawing, Sambro Light RCMP report

## [2026-05-13] v1.4 — Deep Linking, Search, Die-Cut Tabs, Polaroid Effect

- **Feat: Deep linking (H-107)** — URL hash `#CAN-012` opens that case directly on page load. `hashchange` listener for real-time updates. `history.replaceState` keeps URL in sync when clicking cases.
- **Feat: Search by location (H-100)** — Search box in sidebar filters map markers and case list by location, shape, year, or case ID. Clear button (✕) resets. Mobile: 44px touch targets.
- **Feat: Die-cut folder tabs (H-016)** — Staggered tab offsets (0px/5px/10px), circular notch illusion via `::after` pseudo-element, active tab pops out with `translateX(-4px)` and shadow. Mobile: horizontal layout resets.
- **Feat: Polaroid photo effect (H-030)** — Aged `#f5f0e8` background, thicker 12px borders, stronger `contrast(1.4) brightness(0.8) saturate(0.6) sepia(0.2)` filter, hover straightens+scales 1.04x, subtle paper texture via `::before` gradient, enhanced tape corners (40×14px, more yellowed).

## [2026-05-13] v1.3 — Batch 1 Visual Polish

Deployed hand-drawn UI elements and interaction refinements:

- **Feat: Hand-drawn checkboxes (H-021)** — New `.hand-checkbox` class with Caveat-font red ✗ mark. Filter buttons now use hand-drawn boxes instead of unicode checkbox glyphs.
- **Feat: Paperclip toggle (H-022)** — New `.paperclip-toggle` component with sliding clip mechanism for toggle UI.
- **Feat: Stamp press states** — `.stamp-badge:active` and `.detail-stamp:active` for tactile press feedback.
- **Feat: Post-it refinements** — Added `::before` fold highlight gradient and `:active` press state to `.postit-btn`, `.p-btn`, `.search-link-btn`.
- **Refactor: Filter button typography** — Changed from Special Elite 11px to Caveat 14px for handwritten feel.
- **Refactor: Filter checkbox style** — `.filter-btn::before` renders hand-drawn box, `.filter-btn.active::after` renders red ✗ mark.
- **Rebase: Remote sync** — Rebased over 4 remote debug commits (39da324, 5c0e9c2, d8fd61c, 62690ed, ae61d86).

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
