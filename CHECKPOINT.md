# Project HEIMDALL — Session Checkpoint
## Stopped: May 15, 2026 — v1.8 Deployed

### Where We Are
Relationship graph, date disambiguation, sound effects, witness cross-reference, and narratives.js minification deployed to GitHub Pages.

### What Was Done This Session
1. **H-101: Case relationship graph** — 4th "RELATIONSHIPS" tab with visual node graph + sortable table. Shows cases connected by shared pattern tags or explicit cross-references. Fixed quote escaping in onclick handlers.
2. **H-061: Date disambiguation** — Standardized all 56 dates to ISO format (YYYY-MM-DD) with precision field (year/month/day). Human-readable display via `formatDate()`.
3. **H-105: Sound effects** — Procedural Web Audio API: paper rustle, stamp thud, staple click, UI click. 🔊/🔇 toggle.
4. **H-056: Witness pattern cross-reference** — "Witness Pattern Matches" in Relationships tab. Categorizes by RCMP/Military/Police/Pilot/Civilian Group.
5. **H-201: Narratives.js minification** — Pipeline generates `narratives.min.js`. HTML loads minified version.
6. **H-202: YAML parser verification** — Verified regex frontmatter stripping works on all 56 files.

### Current State
- **Branch:** main
- **Last commit:** 7f966a6 (v1.8 — relationships, dates, sound, witness cross-ref)
- **docs/index.html:** ~3457 lines
- **Data:** 56 cases, 20+ media files on disk across 11 case folders

### What's Next (Priority Order)
1. **H-055** — Continue media collection for remaining 45 cases (P0)
2. **H-054** — Fill research gaps (P1, requires web research)
3. **H-050/H-051/H-052** — Data mining NUFORC/CADORS/MUFON (P1, likely network-blocked)
4. **H-200** — narratives.js sync automation (P1, CI/CD)

### Open Issues Summary
- 5 open (1 P0, 3 P1, 1 P2), 36 completed, 1 blocked
- Full tracker at `ISSUE_TRACKER.md`

### Key Files
| File | Purpose |
|------|---------|
| `docs/index.html` | Main app — all HTML/CSS/JS inline, ~3457 lines |
| `docs/narratives.js` | Generated case narratives (56 entries) |
| `docs/narratives.min.js` | Minified version (loaded by HTML) |
| `data/cases-v5-master.json` | Master JSON — 56 cases, 66 fields each |
| `data/cases/*.md` | 56 source markdown case files |
| `docs/data/cases-full.json` | Served copy (GitHub Pages) |
| `docs/images/` | 20+ media files across 11 case folders |

### Design System
- Fonts: Special Elite (headers), Source Sans Pro (body), Caveat (handwritten)
- Colors: manila (#d4c5a9, #e8dcc8), red (#c41e3a), gold (#d4a843), brown (#6b5e50), purple (#6b2fa0)
- Night mode: dark (#14100c, #1a1410), muted gold (#c89060, #d4a050), red accents (#8b2020, #4a1010)
- Ballpoint blue marginalia: #0047AB
- Aesthetic: classified file / manila folder / paper textures / stamps / staples / tape

### Deployment
```bash
cd /root/project-heimdall
git add -A && git commit -m "message" && git push
```
GitHub Pages serves from `docs/` within ~60 seconds.
