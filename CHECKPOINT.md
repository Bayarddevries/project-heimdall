# Project HEIMDALL — Session Checkpoint
## Stopped: May 11, 2026 — Evening Session

### Where We Are
Built the **Falcon Lake dossier prototype** (`docs/falcon-lake-prototype.html`) — a standalone 5-tab interactive case file with the full classified aesthetic. This is the visual template for ALL 54 cases going forward.

### The Pivot
We pivoted from incremental map tweaks to a complete redesign of the case presentation. Instead of single Leaflet popups, each case will open as an interactive multi-page dossier (folder with tabs).

### What's Built
- `docs/falcon-lake-prototype.html` — Complete prototype, all CSS/JS inline
  - 5 tabs: Incident, Witnesses, Evidence, Official Record, Aftermath
  - Full classified file aesthetic (manila grain, coffee rings, staples, tape, polaroids, marginalia)
  - Content for Falcon Lake (CAN-011) populated from CSV + historical records
  - Tab navigation, hover effects, stamp watermarks

### What's Next (Priority Order)
1. **Integrate dossier into main index.html** — Replace current popup system with the tabbed folder UI. Side panel on marker click.
2. **Expand all 54 cases to the rich schema** — CSV only has 8 fields. We need 25+ fields per case (witness counts, evidence types, physical trace, official response, media). Start with Tier A cases first.
3. **Data research pipeline** — Mine NUFORC, government archives, press, ufology sources for detailed enrichment.
4. **Media** — Find real photos (polaroid frames), embed YouTube videos.
5. **Coordinate fixes** — Falcon Lake lat/lng, jitter overlapping markers.
6. **Adjacent cases** — CAN-051/052/054 (2023 US flap) as related/cross-referenced.

### Live Prototype URL
`http://localhost:8123/falcon-lake-prototype.html` (needs server restart: `cd /root/project-heimdall/docs && python3 -m http.server 8123`)

### Live Site
`https://bayarddevries.github.io/project-heimdall/` — current version (pre-dossier redesign)

### Design Decisions Locked In
- Classified file aesthetic from `classified-file-ui` skill (manila, grain, staples, tape, etc.)
- 5-tab dossier per case (not 6 — condensed from original proposal)
- Google Fonts: Special Elite, Source Sans 3, Caveat (only external dependency)
- Inline everything — no external CSS/JS files (single HTML deliverable)
- Post-it notes for agent annotations
- Polaroid frames with tape corners for images
- Handwritten marginalia in ballpoint blue (#0047AB)

### Source CSV
`/mnt/c/Users/bayar/Downloads/CANADIAN UFO SIGHTINGS.csv` (50 rows, 8 columns)

### Repo
`/root/project-heimdall/` on `main` branch
Deploy from `docs/` via GitHub Pages
