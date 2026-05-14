# Project HEIMDALL — Session Checkpoint
## Stopped: May 14, 2026 — v1.7 Deployed

### Where We Are
Edge wear, media collection, and dark mode deployed to GitHub Pages.

### What Was Done This Session
1. **H-011: Edge wear + inner glow** — Paper edge shading on sidebar/detail-panel/top-bar with repeating gradients, inner glow on containers, case-item edge wear lines, filter-bar edge shadow
2. **H-055: Media collection** — 9 new Wikimedia Commons images for 8 cases (CAN-012, CAN-013, CAN-018, CAN-028, CAN-030, CAN-043, CAN-046, CAN-055). All media_urls updated to dict format with type classification. Pipeline re-run.
3. **H-106: Dark mode night ops** — Full red-lit night operations theme with 🌙 Night Ops toggle button. Dark backgrounds (#14100c), muted gold text (#c89060), red accents (#8b2020). Map tile filter (brightness 0.6 + sepia + hue-rotate). localStorage persistence.

### Current State
- **Branch:** main
- **Last commit:** 7918824 (v1.7 — edge wear, media, dark mode)
- **docs/index.html:** ~2920 lines
- **Data:** 56 cases, 20+ media files on disk across 11 case folders

### What's Next (Priority Order)
1. **H-101** — Case relationship graph (P2)
2. **H-103** — Print/export case file (P2)
3. **H-104** — Classified overlay toggle (P2)
4. **H-050/H-051/H-052** — Data mining NUFORC/CADORS/MUFON (P1, requires web research)
5. **H-054** — Fill research gaps (P1)
6. **H-056** — Cross-reference witnesses (P2)
7. **H-061** — Date disambiguation (P2)

### Open Issues Summary
- 8 open (1 P0, 4 P1, 3 P2), 30 completed, 1 blocked
- Full tracker at `ISSUE_TRACKER.md`

### Key Files
| File | Purpose |
|------|---------|
| `docs/index.html` | Main app — all HTML/CSS/JS inline, ~2920 lines |
| `docs/narratives.js` | Generated case narratives (56 entries) |
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
