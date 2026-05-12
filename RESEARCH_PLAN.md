# Project HEIMDALL — Research & Enrichment Plan

## Context

We have 50 Canadian UFO sightings from 1662–2025, initially parsed from CSV into a v3 schema with ~70 fields per case. Current coverage analysis shows:

- **100% filled:** 45 fields (core identity, location, shape, contact type, narrative, tags, relationships)
- **50–98% filled:** 10 fields (dimensions, movement, duration, being summary, province)
- **0–38% filled:** 23 fields — these are the enrichment target

## Priority Gaps (the fields users care about)

| Gap | Coverage | Why It Matters |
|-----|----------|----------------|
| Size/dimensions estimate | 0% | "How big was it?" — first question users ask |
| Speed & altitude | 0% | Performance data distinguishes craft from natural phenomena |
| Being/appearance details | 0–8% | The "alien" question — humanoid? entity? description? |
| Media URLs (photos/video) | 10% | Visual evidence is the hook that keeps users engaged |
| CADORS report links | 0% | Government-verified pilot reports = high credibility |
| NUFORC cross-references | 0% | Corroborating witness accounts |
| Weather conditions | 0% | Rules out misidentification (cloud formations, meteors) |
| First-hand quotes | ~5% | "Here's what the witness actually said" — narrative gold |

## Three-Tier Enrichment Strategy

### Tier 1 — Low-Hanging Fruit (automated, no API)
**Effort:** 2–4 hours. **Impact:** Fills 5–8 fields per case for ~80% of cases.

1. **Historical Weather Lookup** — For each dated sighting (post-1900), query Environment Canada historical weather or use a weather API to get conditions at that location/date. This rules out misidentification and adds realism.

2. **Pattern Analysis & Cross-Case Clustering** — Group cases by:
   - Same witness seeing multiple events (e.g., Stefan Michalak appears in other reports)
   - Cases within 100km of each other within 30 days
   - Same shape appearing in same region across decades
   - Build a "related cases" graph that the UI can surface

3. **Being Data Extraction** — For the 4 CE3 cases (Duncan BC, Granby QC, l'Annonciation QC, St-Zotique QC) and the CE4 case (Port Colborne), extract and structure any being/entity data from the existing narratives. Currently these fields are empty even though the narrative text describes entities.

4. **Media Inventory from Google Drive** — We have a Google Drive "ufo media" folder. Map images/files to specific case IDs by filename pattern matching.

5. **CADORS ID Extraction** — For cases that mention CADORS in their source (Vancouver 2014, Gulf of St. Lawrence 2021, N. Alberta 2025), extract the specific CADORS report numbers and construct the URL.

### Tier 2 — Web Scraping (Firecrawl API)
**Effort:** 1–2 API runs, ~200 requests total. **Impact:** Brings media URLs, NUFORC links, additional narratives to 80%+ coverage.

For each of the 50 cases, scrape:

1. **NUFORC Database** — Search `nuforc.org` for sightings matching location + date range. Extract witness count, shape, and link to the report.

2. **Wikipedia / Notable Cases** — For the ~12 cases that have Wikipedia entries (Falcon Lake, Shag Harbour, Shag Harbour, Nahanni Valley, etc.), scrape the article for additional witness quotes, dimensions, and aftermath details.

3. **Newspaper Archives** — For well-documented cases (Charlie Redstar Carman MB, Westmount QC, Shag Harbour NS, Falcon Lake MB), search local newspaper archives for contemporary coverage and witness interviews.

4. **MUFON Case Files** — Cross-reference cases against MUFON's database. Many Canadian cases have MUFON filings we can link.

5. **YouTube / Video Evidence** — Search for video documentation of each case. Many Canadian UFO cases have YouTube documentaries or footage. Link these to `media_urls`.

6. **CADORS Public Reports** — Search aviation authority databases for the pilot-reported cases.

### Tier 3 — Deep Research (manual review, high-value cases)
**Effort:** 2–3 hours focused on Tier A cases. **Impact:** Complete first-hand accounts, full narratives, being entity descriptions, official report summaries.

Focus on the 10 Tier A cases only — these are the heavy hitters users will spend the most time with:

1. **Falcon Lake (CAN-011)** — Stefan Michalak's chest burns, radioactive soil, RCMP Form 63
2. **Shag Harbour (CAN-012)** — Canada's Roswell, RCN search, yellow foam, sonar hits
3. **Duncan BC (CAN-018)** — Nurse Doreen Kendall, two tall men in dark suits, psychological profile
4. **Langenburg SK (CAN-022)** — Edwin Fuhr, 5 rings of flattened grass, RCMP report
5. **St. Paul AB Landing Pad (CAN-015)** — The UFO landing pad, centennial, municipal records
6. **Montreal Police (CAN-032)** — 40+ people, Place Bonaventure, 3-hour sighting
7. **Carp ON (CAN-033)** — "The Guardian" VHS tapes, scorched field
8. **Fox Lake YT (CAN-038)** — 31 witnesses, massive craft
9. **Vancouver Near-Miss (CAN-044)** — Commercial pilot, YVR airport, CADORS
10. **Charlie Redstar (CAN-023)** — 1000s of sightings, months-long phenomenon

For each of these, build:
- Extended narrative (2–3x current length)
- Full witness list with quotes
- Official report summary
- Media gallery (photos, videos, newspaper clippings)
- Timeline of events (if multi-day/multi-phase)
- Aftermath (what happened to the witnesses, cultural impact)

## Research Pipeline Architecture (for when Firecrawl is unblocked)

```
scripts/
├── enrich_weather.py          # Historical weather lookup per case
├── enrich_beings.py           # Extract being/entity data from narratives
├── enrich_media.py            # Map Google Drive media → case IDs
├── enrich_cadors.py           # Extract CADORS report URLs
├── enrich_scrape.py           # Firecrawl pipeline (NUFORC, Wiki, news)
├── enrich_cluster.py          # Cross-case relationship graph
└── output/
    ├── cases-v3-weather.json  # Weather-enriched v3
    ├── cases-v3-media.json    # Media-enriched v3
    └── cases-v4-master.json   # Final merged output
```

## Recommended Order of Implementation

1. **Start with Tier 1** — No external API needed. Parse narrative text for being data, extract CADORS IDs, map existing media, compute historical weather data (can use a free weather API or offline database).

2. **Then Tier 2** — Run the Firecrawl scraping pipeline. This is serial (rate-limited), so expect it to take 30–60 minutes for all 50 cases.

3. **Finish with Tier 3** — Deep-research the 10 Tier A cases. These get the most page views and set the quality bar for the whole archive.

## What This Means for the Map UI

Once enriched, each case file tab will have:
- **INCIDENT:** Core facts + dimensions + weather + narrative + media gallery
- **WITNESS:** Full witness list + credibility scores + first-hand quotes + being descriptions
- **EVIDENCE:** Physical trace data + EM interference + radar confirmation + media
- **OFFICIAL:** CADORS/RCMP/National sources + official report summary + military involvement
- **AFTERMATH:** Cultural impact + witness fate + follow-up reports + related cases graph

## Immediate Next Steps

Pick one:
- **A)** Run Tier 1 locally right now (weather, beings extraction, media mapping, CADORS) — no API needed
- **B)** Start the Firecrawl scraping pipeline for Tier 2 — needs terminal approval
- **C)** Build out one Tier A case fully as a template (Falcon Lake is the best candidate) — this shows us what the end state should look like

Which path do you want to start with?
