#!/usr/bin/env python3
"""
Tier 2 — Firecrawl Scraping Pipeline
Scrapes NUFORC, Wikipedia, news, and MUFON for additional case data.
Sequential execution with rate limiting to avoid 429s.
"""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

FIRECRAWL_API_KEY = "fc-4d7a7ed5608f4ad197091d46c9d34ebf"
FIRECRAWL_BASE = "https://api.firecrawl.dev/v1"

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
INPUT = DATA_DIR / "cases-v3-tier1-enriched.json"
API_KEY = FIRECRAWL_API_KEY

def load():
    with open(INPUT, encoding="utf-8") as f:
        return json.load(f)

def firecrawl_scrape(url, formats=None):
    """Scrape a URL via Firecrawl API."""
    if formats is None:
        formats = ["markdown"]
    data = json.dumps({
        "url": url,
        "formats": formats,
        "onlyMainContent": True,
    }).encode()
    
    req = urllib.request.Request(
        f"{FIRECRAWL_BASE}/scrape",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def scrape_nuforc(case, index, total):
    """Search NUFORC for additional details."""
    cid = case["case_id"]
    loc = case.get("location", "").split(",")[0].strip()
    year = case.get("year", "")
    
    # NUFORC search URL
    url = f"https://nuforc.org/?s={urllib.parse.quote(f'{loc} {year}')}"
    
    print(f"  [{index+1}/{total}] NUFORC search for {cid} ({loc}, {year})...")
    try:
        result = firecrawl_scrape(url)
        md = result.get("markdown", "")
        if len(md) > 100:
            case["nuforc_summary"] = md[:2000]
            case["nuforc_enriched"] = True
            print(f"    Found: {len(md)} chars")
        else:
            case["nuforc_enriched"] = False
            print(f"    No results")
    except Exception as e:
        print(f"    Error: {e}")
        case["nuforc_enriched"] = False
    
    time.sleep(2)  # Rate limit
    return case

def scrape_wikipedia(case, index, total):
    """Search Wikipedia for the case."""
    cid = case["case_id"]
    loc = case.get("location", "").split(",")[0].strip()
    name = loc.replace(" ", "_")
    
    # Try Wikipedia article
    url = f"https://en.wikipedia.org/wiki/{name}_UFO_incident"
    # Also try common variations
    urls_to_try = [
        f"https://en.wikipedia.org/wiki/{name}",
        f"https://en.wikipedia.org/wiki/UFO_sighting_in_{name}",
    ]
    
    print(f"  [{index+1}/{total}] Wikipedia search for {cid}...")
    case["wikipedia_enriched"] = False
    
    for try_url in urls_to_try:
        try:
            result = firecrawl_scrape(try_url)
            md = result.get("markdown", "")
            if len(md) > 200 and "ufo" in md.lower() or "unidentified" in md.lower():
                case["wikipedia_url"] = try_url
                case["wikipedia_summary"] = md[:3000]
                case["wikipedia_enriched"] = True
                print(f"    Found: {try_url}")
                break
            else:
                print(f"    Not relevant")
        except Exception as e:
            print(f"    Error: {e}")
        
        time.sleep(1)
    
    return case

def scrape_youtube_media(case, index, total):
    """Search YouTube for video evidence."""
    cid = case["case_id"]
    loc = case.get("location", "").split(",")[0].strip()
    year = case.get("year", "")
    
    # YouTube search for documentary/evidence
    query = f"{loc} {year} UFO sighting evidence"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    print(f"  [{index+1}/{total}] YouTube search for {cid}...")
    try:
        result = firecrawl_scrape(url)
        md = result.get("markdown", "")
        # Extract video IDs from markdown
        videos = []
        for line in md.split("\n"):
            if "youtube.com/watch" in line:
                videos.append(line.strip())
                if len(videos) >= 3:
                    break
        
        if videos:
            case["youtube_links"] = videos[:3]
            case["youtube_enriched"] = True
            print(f"    Found {len(videos)} videos")
        else:
            case["youtube_enriched"] = False
            print(f"    No videos found")
    except Exception as e:
        print(f"    Error: {e}")
        case["youtube_enriched"] = False
    
    time.sleep(2)
    return case

def main():
    print("Loading Tier 1 enriched cases...")
    cases = load()
    print(f"Loaded {len(cases)} cases")
    
    # Focus on Tier A cases first (10 highest priority)
    tier_a = [c for c in cases if c.get("tier") == "A"]
    tier_b = [c for c in cases if c.get("tier") == "B"]
    
    print(f"Tier A: {len(tier_a)} cases (full enrichment)")
    print(f"Tier B: {len(tier_b)} cases (summary only)")
    
    # Enrich Tier A cases fully
    print(f"\n=== Tier A Deep Enrichment ===")
    for i, case in enumerate(tier_a):
        case = scrape_nuforc(case, i, len(tier_a))
        save_progress(cases)
        
        case = scrape_wikipedia(case, i, len(tier_a))
        save_progress(cases)
        
        case = scrape_youtube_media(case, i, len(tier_a))
        save_progress(cases)
        
        print(f"  Completed {case['case_id']}")
        print(f"  {'='*50}")
    
    # Tier B - just NUFORC
    print(f"\n=== Tier B Summary Enrichment ===")
    for i, case in enumerate(tier_b):
        if i >= 5:
            print(f"  Limiting to 5 Tier B cases for this run...")
            break
        case = scrape_nuforc(case, i, 5)
        save_progress(cases)
    
    # Recalculate richness
    def richness(c):
        score = 0
        total = 0
        skip = {"case_id", "date", "year", "year_int", "location", "province", "latitude", "longitude",
                "coordinates", "related_cases", "pattern_tags", "narrative", "source_primary_csv",
                "csv_evidence_summary", "csv_beings_summary"}
        for k, v in c.items():
            if k in skip:
                continue
            total += 1
            if v and str(v).strip() not in ("", "N/A", "Not documented", "Not applicable", "Unknown", "[]", 0, False, "False"):
                score += 1
        return round(score / max(total, 1) * 100)
    
    for c in cases:
        c["richness_score"] = richness(c)
    
    avg_rich = sum(c["richness_score"] for c in cases) / len(cases)
    print(f"\nTier 2 Complete. Avg richness: {avg_rich:.1f}/100")
    
    output_path = DATA_DIR / "cases-v3-tier2-enriched.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Saved to {output_path}")

def save_progress(cases):
    """Save intermediate progress."""
    output_path = DATA_DIR / "cases-v3-tier2-progress.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
