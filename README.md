# PROJECT HEIMDALL — Canadian UFO Sightings Archive

An interactive, classified-aesthetic Leaflet.js map and archive of 70 documented Canadian UFO sightings spanning 1662 to 2025.

**Live site:** https://bayarddevries.github.io/project-heimdall/

---

## Overview

Project HEIMDALL is an interactive map-based archive of Canadian UFO/aerial phenomenon reports. Users explore sightings on a Leaflet.js map, click markers or sidebar entries to open detailed case files with full historical narratives, witness accounts, physical evidence records, classification data, and source citations.

The visual aesthetic evokes declassified government files: paper grain textures, redacted stamps, typewriter-style fonts (Special Elite), handwritten marginalia (Caveat), Manila folder UI elements, and the visual language of a 1970s intelligence archive.

## Stats

| Metric | Count |
|--------|-------|
||| Total Cases | 70 ||
|| Time Span | 1662-2025 (364 years) ||
||| Tier A (Priority) | 11 ||
||| Tier B (Moderate) | 7 ||
||| Tier C (Routine) | 50 ||
|| CE1 Encounters | 13 ||
|| CE2 Encounters | 7 ||
|| CE3 Encounters | 5 ||
|| CE4 Encounters | 1 ||
||| Case File Narratives | 70/70 (complete) ||

## Features

- **Interactive Leaflet map** — 70 geolocated markers across Canadian territory
- **Timeline slider** — filter cases by year range (1662 to 2025)
- **Sidebar case list** — sortable, filterable by tier (A/B/C) and encounter type (CE1-CE4, CE2, CE3, CE4, DD, NL, RV)
- **Detail panel** — right-side case file viewer with full markdown narrative, classification data, evidence, and source citations
- **Popup cards** — styled as Manila folder cases with staples, paperclips, and classification stamps
- **Tier system** — A (priority, full investigation), B (moderate, enhanced documentation), C (routine, basic documentation)
- **Hynek classification** — CE1 through CE4, NL (nocturnal lights), RV (radar-visual), DD (daylight disc)

## Architecture

```
project-heimdall/
├── docs/                    # GitHub Pages root (deployed from docs/ folder)
│   ├── index.html          # Single-page app: map, sidebar, detail panel, all JS
|   ├── narratives.js       # All 70 case narratives as JS object (57KB)
├── data/
│   ├── raw_sightings.csv   # Original 50-row source CSV
|   ├── cases.json          # Metadata JSON (70 entries, sync with index.html CASES array)
│   ├── cases-all.json      # Full case data with YAML frontmatter metadata
|   ├── cases/              # 70 individual markdown case files (CAN-001.md to CAN-070.md)
│   ├── research_needs.json # Structured research gap tracking per case
│   └── research_tasks.txt  # Research task queue
├── src/
│   └── index.html          # Development source (pre-narrative embed)
├── RESEARCH_WORKFLOW.md    # Data research workflow documentation
├── README.md               # This file
├── AGENTS.md              # Agent operating instructions
├── CHANGELOG.md           # Version history
└── ISSUE_TRACKER.md       # Issue tracking (markdown)
```

## Key Files

| File | Purpose |
|------|---------|
| `docs/index.html` | Frontend application — all HTML/CSS/JS in a single file |
| `docs/narratives.js` | Case narratives embedded for client-side rendering |
| `data/cases.json` | Metadata array synced with embedded `CASES` JS array |
| `data/cases/*.md` | Rich markdown case files (source of narrative content) |
| `data/cases-all.json` | Full case data aggregation with frontmatter |

## Data Sources

- RCMP Form 63 and field reports
- NUFORC (National UFO Reporting Center) archives
- CADORS (Civil Aviation Daily Occurrence Reporting System)
- Project Magnet (Canadian government UFO research program)
- MUFON (Mutual UFO Network)
- DND (Department of National Defence) declassified files
- Jesuit Relations (historical records)
- Local press archives and witness accounts

## Build & Deploy

No build step. GitHub Pages serves `docs/` from the `main` branch.

To update:
1. Edit `docs/index.html` and/or `data/cases/*.md`
2. If changes to the CASES array: sync `data/cases.json`
3. If new/updated .md files: regenerate `docs/narratives.js`:
   ```
   # Script to embed all markdown narratives into narratives.js
   python3 -c "
   import os, json, re; cases_dir='data/cases'; narratives={}
   for f in sorted(os.listdir(cases_dir)):
       if not f.endswith('.md'): continue
       c=open(os.path.join(cases_dir,f)).read()
       m=re.match(r'^---\s*\n.*?\n---\s*\n(.*)$',c,re.DOTALL)
       body=m.group(1).strip() if m else c.strip()
       cid=re.search(r'^case_id:\s*(.+)$',m.group(0) if m else '',re.MULTILINE)
       cid=cid.group(1).strip() if cid else f.replace('.md','')
       narratives[cid]=body
   open('docs/narratives.js','w').write(f'var NARRATIVES = {json.dumps(narratives, ensure_ascii=False)};')
   "
   ```
4. `git add -A && git commit -m "message" && git push`

## Contact Classifications

- **CE1** — Close Encounter of the First Kind: visual sighting at close range
- **CE2** — Close Encounter of the Second Kind: physical evidence (trace marks, radiation, soil effects)
- **CE3** — Close Encounter of the Third Kind: entity/being reports
- **CE4** — Close Encounter of the Fourth Kind: abduction/contact experiences
- **NL** — Nocturnal Lights: lights observed during night hours
- **RV** — Radar-Visual: confirmed by both radar and visual observation
- **DD** — Daylight Disc: solid objects observed during daylight

## Tier System

| Tier | Description | Marker Color |
|------|-------------|--------------|
| A | Priority — Full investigation with primary sources, multiple witness types, physical evidence | Red (#c41e3a) |
| B | Moderate — Enhanced documentation, official records, enhanced credibility | Gold (#d4a843) |
| C | Routine — Basic documentation, single-witness, lower credibility | Brown (#6b5e50) |

*CE3 and CE4 cases are overridden to purple (#6b2fa0) regardless of tier.*

## Notable Cases

- **CAN-011** — Montreal Fiery Serpents (1662): Earliest documented UFO sighting in Canadian history
- **CAN-012** — Falcon Lake (1967): Stefan Michalak's burn case, grid-pattern injuries, radioactive soil
- **CAN-012** — Shag Harbour (1967): 11+ witnesses, yellow foam, sonar hits, object entered water
- **CAN-017** — Duncan, BC (1970): Nurse Doreen Kendall's CE3 encounter, 2 tall men in dark suits
- **CAN-032** — Carp, ON (1991): "The Guardian" VHS tapes, scorched field, Diane Labenek
- **CAN-051-054** — 2023 Flap Cases: Cross-border cases with Canadian relevance (Yukon, Lake Huron, Prudhoe Bay)
