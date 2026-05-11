# PROJECT HEIMDALL — Research Workflow

## How We Collaborate

1. **AI Research Pass:** Agent researches each case via web, fills in the case file with findings
2. **Manual Research Pass:** Bayard does independent research (books, archives, contacts, media)
3. **Telegram Sync:** Bayard and agent chat on Telegram about findings, interesting angles, gaps
4. **Integration:** Agent merges Bayard's findings into case files, commits to repo
5. **Site Update:** GitHub Pages auto-deploys updated data

## Case File Structure

Each case file lives in `data/cases/CAN-XXX.md` with:
- Basic data from CSV
- Expanded fields (narrative, witness statements, weather, etc.)
- Media references (linked to files in `media/` directory)
- Research notes from AI and Bayard
- Status checklist

## Status Tracking

- `RESEARCH PENDING` — No research done yet
- `AI PASS IN PROGRESS` — Agent researching now
- `AI PASS COMPLETE` — Agent finished first pass
- `IN DISCUSSION` — Bayard and agent chatting on Telegram
- `MANUAL PASS IN PROGRESS` — Bayard doing independent research
- `MANUAL PASS COMPLETE` — Bayard's findings collected
- `NARRATIVE READY` — Full dossier drafted
- `MEDIA COLLECTED` — Photos/documents gathered
- `CASE COMPLETE` — File ready for site display

## Naming Convention

- Case IDs: CAN-001 through CAN-XXX
- Media files: `media/photos/CAN-XXX_description.jpg`
- Case files: `data/cases/CAN-XXX.md`

## Adding New Cases

1. Add row to `data/raw_sightings.csv`
2. Run update script to regen case files
3. Git commit and push

## Research Sources Priority

1. NUFORC database
2. CADORS (aviation safety reports)
3. RCMP/DND declassified files
4. Newspaper archives
5. MUFON case files
6. Ufology books (e.g., Chris Rutkowski)
7. YouTube/documentary analysis
8. Witness interviews (when available)
9. Skeptical analysis sources
