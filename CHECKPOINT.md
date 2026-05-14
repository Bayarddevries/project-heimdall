# Project HEIMDALL — Session Checkpoint
## Stopped: May 13, 2026 — v1.4 Deployed

### Where We Are
Four new features deployed to GitHub Pages. All changes are in `docs/index.html`.

### What Was Done This Session
1. **H-107: Deep linking** — `#CAN-012` opens case directly via URL hash. `hashchange` listener + `history.replaceState`.
2. **H-100: Search by location** — Search box in sidebar filters map markers + case list by location, shape, year, case ID.
3. **H-016: Die-cut folder tabs** — Staggered offsets, notch illusion, active tab pops out. Mobile horizontal layout.
4. **H-030: Polaroid photo effect** — Aged bg, thicker borders, stronger contrast filter, hover straighten+scale, enhanced tape.

### Current State
- **Branch:** main
- **Last commit:** 9f948b5 (v1.4 — 4 features)
- **docs/index.html:** ~2373 lines
- **Data:** 56 cases, narratives synced

### What's Next (Priority Order)
1. **H-055** — Media/photograph collection (P0 data, requires research)
2. **H-010** — Paper grain background (P1 visual)
3. **H-013** — Offset/scanned text rotation (P1 visual)
4. **H-015** — Handwritten marginalia (P1 visual)
5. **H-102** — Timeline mode (P1 feature)
6. **H-050/051/052** — NUFORC/CADORS/MUFON mining (P1 data)

### Open Issues Summary
- 18 open (4 P0, 9 P1, 5 P2), 20 completed, 1 blocked
- Full tracker at `ISSUE_TRACKER.md`

### Key Files
| File | Purpose |
|------|---------|
| `docs/index.html` | Main app — all HTML/CSS/JS inline, ~2373 lines |
| `docs/narratives.js` | Generated case narratives (56 entries) |
| `data/cases-v5-master.json` | Master JSON — 56 cases, 61 fields each |
| `data/cases/*.md` | 56 source markdown case files |
| `docs/data/cases-full.json` | Served copy (GitHub Pages) |
| `ISSUE_TRACKER.md` | 38 issues, 18 open |
| `AGENTS.md` | Agent operating instructions |

### Design System
- Fonts: Special Elite (headers), Source Sans Pro (body), Caveat (handwritten)
- Colors: manila (#d4c5a9, #e8dcc8), red (#c41e3a), gold (#d4a843), brown (#6b5e50), purple (#6b2fa0)
- Ballpoint blue marginalia: #0047AB
- Aesthetic: classified file / manila folder / paper textures / stamps / staples / tape

### Deployment
```bash
cd /root/project-heimdall
git add -A && git commit -m "message" && git push
```
GitHub Pages serves from `docs/` within ~60 seconds.
