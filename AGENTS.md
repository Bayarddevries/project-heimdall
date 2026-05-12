# AGENTS.md — Project HEIMDALL Operating Instructions

This file provides instructions for AI agents working on Project HEIMDALL. Load this context when working on the repo.

---

## Project Overview

Project HEIMDALL is an interactive Leaflet.js map + classified-aesthetic archive of 54 Canadian UFO sightings (1662-2025). Deployed to GitHub Pages from the `docs/` folder. Single-page application, no build step, no frameworks.

**Live site:** https://bayarddevries.github.io/project-heimdall/

---

## Critical Architecture Facts

### Data Flow
1. Case narratives live in `data/cases/*.md` (54 files, CAN-001.md to CAN-054.md)
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

---

## What NOT To Do

- **Do not add a build step, framework, or bundler.** The entire site works as static files on GitHub Pages.
- **Do not fetch markdown at runtime via AJAX/fetch.** The narratives.js embed pattern is intentional and proven.
- **Do not modify the `docs/index.html` structure without testing the Leaflet map, sidebar, and detail panel together.**
- **Do not edit `docs/narratives.js` manually.** Always regenerate from `data/cases/*.md`.
- **Do not change the CSS theme** without preserving the classified-aesthetic (paper tones, typewriter fonts, manila folders).
- **Do not deploy from anything other than `docs/` on the `main` branch.**

---

## Common Tasks

### Adding a New Case

1. Create `data/cases/CAN-XXX.md` with frontmatter:
   ```yaml
   ---
   case_id: CAN-XXX
   case_number: "51"
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
- Classified aesthetic: paper textures, stamps, staples, tape effects

---

## Testing After Changes

Agents must verify:
1. Map loads without errors in the browser console
2. ALL 54 markers render on the map
3. Sidebar shows all cases
4. Clicking a marker opens the detail panel with narrative content
5. Clicking a sidebar item opens the same detail panel
6. Timeline slider works
7. Tier/encounter type filters work
8. Zero JavaScript errors in the browser console (`browser_console`)

---

## Key File Paths

| File | Purpose |
|------|---------|
| `docs/index.html` | Main app (all HTML/CSS/JS) |
| `docs/narratives.js` | Embedded case narratives (generated) |
| `data/cases/*.md` | Source markdown case files |
| `data/cases.json` | Metadata JSON (synced with CASES array) |
| `data/cases-all.json` | Full case data with all frontmatter |
| `data/raw_sightings.csv` | Original source CSV |
| `data/research_needs.json` | Research gap tracking |

---

## Deployment

`git add -A && git commit -m "message" && git push` to the `main` branch.

GitHub Pages serves from `docs/` and typically deploys within 60 seconds of the push.

---

## Owner

Created by Bayard deVries. Part of the Bayarddevries GitHub organization. Deployed at bayarddevries.github.io/project-heimdall.
