# Project HEIMDALL — Session Checkpoint
## Stopped: May 15, 2026 — v1.9.1 Bugfixes Deployed

### Where We Are
Bug fixes for onclick quoting deployed. 18 cases with media (32 files), CI/CD active.

### What Was Done This Session
1. **Fix: openDetail onclick quoting (H-203)** — Corrected string concatenation in detail panel open button
2. **Fix: window.open onclick quoting (H-204)** — Corrected string concatenation in external search link button

3. **H-055: Media collection phase 2** — Added images for 8 new cases: CAN-001 (Montreal 1910), CAN-003 (CFB Goose Bay), CAN-006 (Project Blue Book PDF), CAN-010 (Fort Frances), CAN-014 (Blue Book 1967), CAN-016 (CIA Reading Room ref), CAN-020 (RCMP patch), CAN-032 (Quebec city). Synced media_urls for all 18 cases with files on disk. Removed 264MB PDF that exceeded GitHub's 100MB limit.
4. **H-200: CI/CD automation** — Created `.github/workflows/regenerate.yml` GitHub Actions workflow that auto-runs the pipeline on push when case data changes.
5. **Media_urls sync** — Fixed media_urls in cases-full.json to match actual files on disk for all cases.

### Current State
- **Branch:** main
- **Last commit:** b33c275 (v1.9 — media collection + CI/CD)
- **docs/index.html:** ~3457 lines
- **Data:** 56 cases, 32 media files across 18 case folders
- **CI/CD:** GitHub Actions workflow active

### What's Next (Priority Order)
6. **H-054** — Fill research gaps (P1, requires web research)
7. **H-050/H-051/H-052** — Data mining NUFORC/CADORS/MUFON (P1, likely network-blocked)
8. **H-055 continued** — More media for remaining 38 cases without images

### Open Issues Summary
- 3 open (3 P1), 38 completed, 1 blocked
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
| `docs/images/` | 32 media files across 18 case folders |
| `.github/workflows/regenerate.yml` | CI/CD pipeline automation |

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
