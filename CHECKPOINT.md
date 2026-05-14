# Project HEIMDALL — Session Checkpoint
## Stopped: May 13, 2026 — v1.5 Deployed

### Where We Are
Six new features deployed to GitHub Pages. All changes in `docs/index.html` + new media files.

### What Was Done This Session
1. **H-010: Paper grain** — 3 noise layers (512/256/128px), increased opacity
2. **H-013: Scan rotation** — translate offset on scan-angle classes for crooked photocopy feel
3. **H-014: Staple accents** — 3D staple graphic on fc-h3 headers via ::before/::after
4. **H-015: Handwritten marginalia** — enhanced handnote with ✎ icon, .agent-note class
5. **H-102: Timeline mode** — horizontal timeline with tier-colored dots, hover labels, adaptive year labels
6. **H-055: Media collection** — 3 new public-domain images added (Falcon Lake, Steve Michalak, Sambro Light)

### Current State
- **Branch:** main
- **Last commit:** 35a6031 (v1.5 — visual polish, timeline, media)
- **docs/index.html:** ~2695 lines
- **Data:** 56 cases, 16 media files on disk across 5 cases

### What's Next (Priority Order)
1. **H-040** — Mobile responsive audit (P1)
2. **H-060** — Geolocation verification via Nominatim (P1)
3. **H-055 continued** — More media for remaining Tier A cases (P0)
4. **H-101** — Case relationship graph (P2)
5. **H-103** — Print/export case file (P2)
6. **H-106** — Dark mode night ops (P2)

### Open Issues Summary
- 12 open (3 P0, 5 P1, 4 P2), 26 completed, 1 blocked
- Full tracker at `ISSUE_TRACKER.md`

### Key Files
| File | Purpose |
|------|---------|
| `docs/index.html` | Main app — all HTML/CSS/JS inline, ~2695 lines |
| `docs/narratives.js` | Generated case narratives (56 entries) |
| `data/cases-v5-master.json` | Master JSON — 56 cases, 61 fields each |
| `data/cases/*.md` | 56 source markdown case files |
| `docs/data/cases-full.json` | Served copy (GitHub Pages) |
| `docs/images/` | 16 media files across 5 case folders |

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
