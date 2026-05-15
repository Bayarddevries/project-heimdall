# AGENTS.md — Project HEIMDALL Operating Instructions

This file provides instructions for AI agents working on Project HEIMDALL. Load this context when working on the repo.

---

## Project Overview

Project HEIMDALL is an interactive Leaflet.js map + classified-aesthetic archive of 70 Canadian UFO sightings (1662-2025). Deployed to GitHub Pages from the `docs/` folder. Single-page application, no build step, no frameworks.

**Live site:** https://bayarddevries.github.io/project-heimdall/
**Repo:** github.com/Bayarddevries/project-heimdall
**Current version:** V5 — 70 cases, v2.0 deployed

---

## Critical Architecture Facts

### Data Flow
1. Case narratives live in `data/cases/*.md` (70 files, CAN-001.md to CAN-070.md)
2. Each .md file has YAML frontmatter + markdown body
3. `docs/narratives.js` is a pre-generated JS object: `var NARRATIVES = {"CAN-001": "...", ...}`
4. `docs/index.html` has a hardcoded `CASES` array for map metadata
5. On click: `openDetail(caseId)` → reads from `NARRATIVES[caseId]` → parses with `marked.js` → injects into detail panel
6. `data/cases.json` = metadata array synced from `docs/index.html`'s `CASES` array

### YAML Parsing
The Python `yaml` library FAILS on certain case files due to unquoted em-dashes (—) in multi-line sequences. Use regex stripping for frontmatter extraction:
```python
m = re.match(r'^---\s*\n.*?\n---\s*\n(.*)$', content, re.DOTALL)
body = m.group(1).strip() if m else content.strip()
```

### Narrative Regeneration
When `data/cases/*.md` files are updated, regenerate `docs/narratives.js` with the script in README.md. **Never edit narratives.js by hand — it is always generated.**

### Three-Tier Data Pipeline
1. `scripts/rebuild_v5.py` — CSV + RESEARCH_DATA → `data/cases-v5-master.json`
2. `scripts/regenerate_markdown.py` — master JSON → 56 `data/cases/*.md` files
3. `scripts/generate_frontend.py` — markdown + master JSON → `docs/narratives.js` + `docs/data/cases-full.json` + `data/cases.json`

**Always run in order**: rebuild_v5.py → regenerate_markdown.py → generate_frontend.py → git push.

### Dual-COPY BUG (CRITICAL)
There are TWO copies of `cases-full.json`:
- `data/cases-full.json` (source/root copy)
- `docs/data/cases-full.json` (the one GitHub Pages ACTUALLY serves)

After ANY change to `cases-full.json`, immediately run:
```
cp data/cases-full.json docs/data/cases-full.json
```
Or run the full pipeline which handles both copies.

## MEDIA RESTORATION (CRITICAL)
The 3-tier pipeline (`generate_frontend.py`) DESTROYS all `media_urls` in `cases-full.json` because markdown case files don't contain that field. After any pipeline run, always restore with:
```
python3 scripts/restore_media.py
```
The backup is stored in `scripts/media_backup.json`. Run `python3 scripts/restore_media.py save` to update the backup after adding new media.

---

## What NOT To Do

- **Do not add a build step, framework, or bundler.** The entire site works as static files on GitHub Pages.
- **Do not fetch markdown at runtime via AJAX/fetch.** The narratives.js embed pattern is intentional and proven.
- **Do not modify the `docs/index.html` structure without testing the Leaflet map, sidebar, and detail panel together.**
- **Do not edit `docs/narratives.js` manually.** Always regenerate from `data/cases/*.md`.
- **Do not change the CSS theme** without preserving the classified-aesthetic (paper tones, typewriter fonts, manila folders).
- **Do not deploy from anything other than `docs/` on the `main` branch.**
- **Do not delete or rename case files** without updating the CASES array in index.html and regenerating narratives.js.
- **Do NOT verify media rendering via `file://` protocol.** The browser's `fetch()` API is blocked on `file://` URLs (CORS). Use live GitHub Pages URL or a local HTTP server.

---

## Common Tasks

### Adding a New Case

1. Create `data/cases/CAN-XXX.md` with frontmatter:
   ```yaml
   ---
   case_id: CAN-XXX
   case_number: "57"
   case_name: Event Name
   date: "1995"
   location: Place, Province
   lat: XX.X
   lng: -XX.X
   hynek: CE1/CE2/CE3/CE4/NL/RV/DD
   tier: A/B/C
   shape: Shape
   duration: Duration
   witnesses: N
   ---
   ```
   Followed by the markdown narrative body.

2. Add entry to `CASES` array in `docs/index.html` (use existing entries as template)
3. Regenerate `docs/narratives.js` using the script in README.md
4. Update `data/cases.json` to match the CASES array
5. Commit and push

### Updating an Existing Case

1. Edit the `data/cases/CAN-XXX.md` file
2. Regenerate `docs/narratives.js`
3. If metadata changed, update the CASES array in `docs/index.html`
4. Update `data/cases.json` to match
5. Commit and push

### Changing UI/CSS

- All CSS lives inside `<style>` in `docs/index.html`
- Test map rendering after any CSS change
- Preserve color palette: manila (#d4c5a9, #e8dcc8), red (#c41e3a), gold (#d4a843), brown (#6b5e50), purple (#6b2fa0)

### Adding New CSS Classes
- Use the existing font families: 'Special Elite' for headings, 'Source Sans Pro' for body text, 'Caveat' for handwritten notes
- Classified aesthetic: paper textures, stamps, staples, tape effects, coffee stains, polaroid frames

---

## Testing After Changes

Agents must verify:
1. Map loads without errors in the browser console
2. ALL 70 markers render on the map
3. Sidebar shows all cases
4. Clicking a marker opens the detail panel with narrative content
5. Clicking a sidebar item opens the same detail panel
6. Timeline slider works
7. Tier/encounter type filters work
8. Zero JavaScript errors in the browser console (`browser_console`)
9. Mobile viewport (375x812): bottom sheet displays full content with accessible close button

---

## Key File Paths

| File | Purpose |
|------|---------|
|| `docs/index.html` | Main app (all HTML/CSS/JS, ~3500 lines) |
|| `docs/narratives.js` | Embedded case narratives (generated, ~57KB) |
|| `data/cases/*.md` | Source markdown case files (70 files) |
|| `data/cases.json` | Metadata JSON (synced with CASES array) |
|| `data/cases-v5-master.json` | Full case data — master JSON (70 cases, 61 fields) |
|| `data/cases-full.json` | Full case data — root copy (sync to docs/) |
|| `docs/data/cases-full.json` | Full case data — served copy (GitHub Pages) |
|| `data/canadian_ufo_sightings_v5.csv` | Extended source CSV (70 rows) — ground truth |
|| `scripts/rebuild_v5.py` | CSV → master JSON pipeline |
|| `scripts/regenerate_markdown.py` | Master JSON → markdown files |
|| `scripts/generate_frontend.py` | Markdown → frontend assets |
|| `.github/workflows/regenerate.yml` | CI/CD — auto-runs pipeline on push |
|| `docs/data/layers/*.json` | 3 overlay GeoJSON files (nuclear, military, NORAD radar) |

---

## Deployment

`git add -A && git commit -m "message" && git push` to the `main` branch.

GitHub Pages serves from `docs/` and typically deploys within 60 seconds of the push.

---

## v1.4 Features (Deployed 2026-05-13)

| ID | Feature | Details |
|----|---------|---------|
| H-107 | Deep linking | `#CAN-012` opens case. `openCaseById()`, `hashchange` listener, `history.replaceState` |
| H-100 | Search | `.search-wrap`, `.search-input`, `.search-clear`. Filters by location/shape/year/ID |
| H-016 | Die-cut tabs | `.folder-tab::after` notch, staggered `margin-left`, active `translateX(-4px)` |
| H-030 | Polaroid | `.polaroid` aged bg, thicker borders, hover straighten+scale, `.tape` 40×14px |

## v1.5 Features (Deployed 2026-05-13)

| ID | Feature | Details |
|----|---------|---------|
| H-010 | Paper grain | 3 noise layers (512/256/128px), increased base opacity to 0.055 |
| H-013 | Scan rotation | CSS vars `--scan-rot`/`--scan-trans`, translate offset on `.scan-angle-1` through `.scan-angle-5` |
| H-014 | Staple accents | 3D staple graphic on `.fc-h3::before` with metallic gradient, prong shadows |
| H-015 | Handwritten marginalia | `.handnote` with ✎ icon, `.agent-note` with dashed left border |
| H-102 | Timeline mode | `.timeline-view` fixed bottom, tier-colored dots, hover labels, `.view-toggle` button |
| H-055 | Media collection | 3 new public-domain images: Falcon Lake reconstruction, Steve Michalak saucer drawing, Sambro Light RCMP report |

## v1.6 Features (Deployed 2026-05-14)

| ID | Feature | Details |
|----|---------|---------|
| H-040 | Mobile touch targets | `.view-toggle` and `.timeline-close` raised to 44px min-dimension; `.timeline-view` z-index 1110; `.timeline-header h3` 11px |
| H-060 | Geolocation verification | Full Nominatim API audit of 56 cases; 3 coordinates corrected (CAN-028, CAN-037, CAN-042) |

## v1.7 Features (Deployed 2026-05-14)

| ID | Feature | Details |
|----|---------|---------|
|| H-011 | Edge wear + inner glow | Paper edge shading with repeating gradients, inner glow on sidebar/detail-panel/top-bar, case-item edge wear lines, filter-bar edge shadow |
|| H-055 | Media collection | 9 new Wikimedia Commons images for 8 cases. media_urls in dict format with type/image/reference classification |
|| H-106 | Dark mode (night ops) | `.night-ops` class on `<body>`, 🌙 Night Ops toggle, dark backgrounds (#14100c), gold text (#c89060), red accents (#8b2020), map tile filter, localStorage persistence |

## v1.9 Features (Deployed 2026-05-15)

| ID | Feature | Details |
|----|---------|---------|
| H-055 | Media collection phase 2 | 32 public-domain images across 18 case folders. Wikimedia Commons + Wikipedia sources. media_urls synced for all cases with files |
|| H-200 | CI/CD automation | `.github/workflows/regenerate.yml` — GitHub Actions auto-runs pipeline on push when case data changes |
|| H-205 | Fix witnesses TypeError in relationships tab | P0 | witnesses field numeric causes TypeError in buildRelationshipsTab; wrapped with String() cast before toLowerCase() — restores detail panel click functionality |



## v1.8 Features (Deployed 2026-05-15)

| ID | Feature | Details |
|----|---------|---------|
| H-101 | Case relationship graph | 4th "RELATIONSHIPS" tab with visual node graph + sortable table. Shows cases connected by shared pattern tags or explicit cross-references. `.rel-graph`, `.rel-node`, `.rel-central`, `.rel-linked`, `.rel-line`, `.rel-tags`, `.rel-tag`, `.rel-tier`, `.rel-table` |
| H-061 | Date disambiguation | All 56 dates standardized to ISO format (YYYY-MM-DD) with `date_precision` field (year/month/day). `formatDate()` function for human-readable display |
| H-105 | Sound effects | Procedural Web Audio API: `playPaperRustle()`, `playStampThud()`, `playStapleClick()`, `playClick()`. `toggleSound()` with 🔊/🔇 button |
| H-056 | Witness pattern cross-reference | "Witness Pattern Matches" in Relationships tab. Categorizes by RCMP/Military/Police/Pilot/Civilian Group |
| H-201 | Narratives.js minification | Pipeline generates `narratives.min.js`. HTML loads minified version |
| H-202 | YAML parser fix | Verified regex frontmatter stripping works on all 56 files |

---

## Batch 1 Visual Polish (Deployed 2026-05-13)

The following CSS classes were added/refined in `docs/index.html`:

| ID | Feature | CSS Classes |
|----|---------|-------------|
| H-021 | Hand-drawn checkboxes | `.hand-checkbox`, `.hand-checkbox .box`, `.hand-checkbox.checked .box::after` |
| H-022 | Paperclip toggle | `.paperclip-toggle`, `.track`, `.clip`, `.on` |
| H-020 | Stamp press states | `.stamp-badge:active`, `.detail-stamp:active` |
| H-019 | Post-it refinements | `.postit-btn::before`, `.postit-btn:active`, `.p-btn::before`, `.p-btn:active` |
| — | Filter button font | `.filter-btn` changed from Special Elite 11px → Caveat 14px |
| — | Filter checkboxes | `.filter-btn::before` hand-drawn box, `.filter-btn.active::after` red ✗ mark |

---

## Owner

## v2.0 Features (Deployed 2026-05-15)

| ID | Feature | Details |
|----|---------|---------|
| H-XXX | Map overlays | 3 toggle-able Leaflet layers: nuclear plants (red), military bases (blue), NORAD radar (green). Loaded via `initOverlays()` in `docs/index.html`. GeoJSON files in `docs/data/layers/`. Layer control at bottom-left. |
| H-XXX | Tier upgrades | 4 cases C→B: CAN-059 North York, CAN-061 Terrace, CAN-066 Harbour Mille, CAN-070 Yellowknife. Now 11A + 7B + 52C. |

## Map Overlay Layer Architecture

Three GeoJSON overlay files in `docs/data/layers/` loaded asynchronously by `initOverlays()` in `docs/index.html`:

| Layer | File | Features | Style | Color |
|-------|------|----------|-------|-------|
| ☢️ Nuclear Facilities | `nuclear_plants.json` | 13 points (plants, mines, labs) | circleMarker r=10 | Red (#c41e3a) |
| ⚔️ Military Bases | `military_bases.json` | 25 points (CFBs, DND, signals) | circleMarker r=8 | Blue (#2d4a6a) |
| 📡 NORAD Radar | `norad_radar.json` | 4 radar lines + 23 stations | circleMarker r=7 + dashed polylines | Green (#2d6a4f) |

All layers: loaded via fetch() with error tolerance, popup on click shows name/type/province. Layer control positioned bottom-left. Compatible with Night Ops (dark mode).

Created by Bayard deVries. Part of the Bayarddevries GitHub organization. Deployed at bayarddevries.github.io/project-heimdall.
