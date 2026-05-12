#!/usr/bin/env python3
"""
Project HEIMDALL — Firecrawl data enrichment pipeline v2
Uses direct Wikipedia URLs (bypasses search API), scrapes case pages, YouTube refs.
"""

import json
import re
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

API_KEY = "fc-4d7a7ed5608f4ad197091d46c9d34ebf"
DATA_FILE = "/root/project-heimdall/data/cases-v2.json"
LOG_FILE = "/root/project-heimdall/scripts/enrichment_log.json"

# ─── Load data ───
with open(DATA_FILE, 'r') as f:
    cases = json.load(f)

log = {"started": datetime.now().isoformat(), "cases": {}}

# ─── Known Wikipedia pages for Canadian UFO cases ───
# Maps location strings → Wikipedia article slug
WIKI_PAGES = {
    "Montreal, QC": None,  # No dedicated Wikipedia for 1662 case
    "Ottawa, ON": None,  # No Wikipedia for 1915 ghost plane
    "Goose Bay, NL": None,  # No Wikipedia for 1947
    "Rivers, MB": None,
    "Gander, NL": "1950_Grand_Falls_UFO_incident",  # Nearby incident
    "Clan Lake, NWT": "Clan_Lake_UFO_sighting",
    "Yellowknife, NWT": "Yellowknife_UFO_incident",
    "Agassiz, BC": None,
    "Falcon Lake, MB": "1967_Falcon_Lake_incident",
    "Shag Harbour, NS": "Shag_Harbour_UFO_incident",
    "Montreal-Nord, QC": "1974_Montreal_UFO_incident",
    "St. Paul, AB": "Landing_at_St._Paul",
    "Surrey, BC": None,
    "Duncan, BC": None,  # Might have page
    "Langenburg, SK": "Langenburg_UFO_sighting",
    "Montérégie, QC": None,
    "Montréal, QC": "1977_Montreal_UFO_incident",  # Mont-Joli
    "Mont-Joli, QC": "Stephenville_UFO_encounters",
    "Valcourt, QC": None,
    "Granby, QC": None,  # May not have own article
    "Carp, ON": "Carp_UFO_incident",
    "Sherwood Park, AB": None,
    "l'Annonciation, QC": None,  # Quebec UFO video
    "Port Colborne, ON": "Port_Colborne_UFO_incident",
    "Vaudreuil-Dorion, QC": None,
    "Calgary, AB": None,
    "Bathurst, NB": None,
    "Edmonton, AB": None,
    "Winnipeg, MB": None,
    "Toronto, ON": None,
    "Halifax, NS": None,
    "Iqaluit, NU": None,
    "Whitehorse, YT": None,
    "Vancouver, BC": "2016_Vancouver_UFO_sighting",
    "Ashmount, AB": None,
    "Regina, SK": None,
    "Winnipeg, MB": None,
    "Sheridan Lake, BC": None,
}

def get_wiki_url(case: dict) -> str:
    """Get Wikipedia URL for a case, checking by location and year."""
    loc = case.get("location", "").strip()
    year = case.get("year", "")
    
    # First try exact location match
    if loc in WIKI_PAGES and WIKI_PAGES[loc]:
        url = f"https://en.wikipedia.org/wiki/{WIKI_PAGES[loc]}"
        return url
    
    # Try partial matches
    for case_loc, slug in WIKI_PAGES.items():
        if slug and any(part in loc.lower() for part in case_loc.lower().split(", ")):
            return f"https://en.wikipedia.org/wiki/{slug}"
    
    return ""

# ─── Firecrawl scraper (v2) ───
def scrape(url: str, formats=None) -> dict:
    """Scrape a URL via Firecrawl v2 API."""
    if formats is None:
        formats = ["markdown"]
    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v2/scrape",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "url": url,
                "formats": formats,
                "onlyMainContent": True,
                "skipTlsVerification": False,
                "timeout": 60000
            },
            timeout=120
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                return data.get("data", {})
    except Exception as e:
        return {}
    return {}

# ─── Scrape Wikipedia page ───
def scrape_wikipedia(case: dict) -> dict:
    """Scrape Wikipedia for a case and extract enrichment data."""
    slug = get_wiki_url(case)
    if not slug:
        return {"wikipedia_url": None, "wikipedia_found": False}
    
    url = f"https://en.wikipedia.org/wiki/{slug}"
    print(f"  Wikipedia: {slug}")
    data = scrape(url, "markdown")
    if not data:
        return {"wikipedia_url": url, "wikipedia_found": False, "scrape_error": True}
    
    md = data.get("markdown", "")
    if not md:
        return {"wikipedia_url": url, "wikipedia_found": False, "empty_content": True}
    
    # Extract structured data
    extract = parse_wikipedia_md(md, case)
    
    # Find external reference URLs
    refs = re.findall(r'\[(?:[^\]]+)\]\((https?://[^)]+)\)', md)
    external_refs = [r for r in set(refs) if 'wikipedia.org' not in r and 'wikimedia' not in r]
    
    return {
        "wikipedia_url": url,
        "wikipedia_found": True,
        "wikidata_article_len": len(md),
        "extract": extract,
        "external_references": external_refs[:15]
    }

def parse_wikipedia_md(md: str, case: dict) -> dict:
    """Extract structured data from Wikipedia markdown."""
    extract = {}
    
    # Date patterns
    date_patterns = [
        r'(?:on|occurred on|date[:\s]+)([A-Z][a-z]+ \d{1,2},?\s+\d{4})',
        r'([A-Z][a-z]+ \d{1,2},?\s+\d{4})',
    ]
    for pat in date_patterns:
        m = re.search(pat, md)
        if m:
            extract['date_detail'] = m.group(1)
            break
    
    # Witness names
    for pat in [
        r'(?:witness(?:es)?|reporter)\s+(?:named\s+)?(?:([\w\s\.]+?))\s+(?:reported|saw|observed|claimed)',
        r'([\w\s]+?)\s+(?:reported|saw|observed|claimed|testified)',
    ]:
        m = re.search(pat, md, re.IGNORECASE)
        if m:
            extract['witness_name'] = m.group(1).strip()
            break
    
    # Size/dimension mentions
    sizes = re.findall(r'(\d+(?:[./]\d+)?)\s*(?:feet|ft|meters|m|km|inches|in)\b', md, re.IGNORECASE)
    if sizes:
        extract['dimensions_mentioned'] = sizes[:5]
    
    # Classification
    for cls in ['CE1', 'CE2', 'CE3', 'CE4', 'CE-1', 'CE-2', 'CE-3', 'CE-4']:
        if cls in md:
            extract['classification_confirmed'] = cls
            break
    
    # Official investigation
    official = []
    for org in ['RCMP', 'RCAF', 'DND', 'CADORS', 'NORAD', 'NATO', 'Transport Canada']:
        if org in md:
            official.append(org)
    if official:
        extract['official_involvement'] = official
    
    # Media types mentioned
    media = []
    if re.search(r'(?:photo|photograph|image|picture)', md, re.IGNORECASE):
        media.append('photographs mentioned')
    if re.search(r'(?:video|footage|film)', md, re.IGNORECASE):
        media.append('video/footage mentioned')
    if re.search(r'(?:tape|recording|audio)', md, re.IGNORECASE):
        media.append('audio/tape mentioned')
    if re.search(r'(?:radar)', md, re.IGNORECASE):
        media.append('radar data mentioned')
    if media:
        extract['media_types'] = media
    
    # Article metrics
    extract['article_word_count'] = len(md.split())
    extract['article_length'] = len(md)
    
    return extract

# ─── Scrape YouTube reference ───
def scrape_youtube(video_url: str) -> dict:
    """Extract metadata from a YouTube video page."""
    print(f"  YouTube: {video_url}")
    data = scrape(video_url)
    if not data:
        return {}
    
    md = data.get("markdown", "")
    if not md:
        return {}
    
    metadata = {}
    title_match = re.search(r'# \[(.+?)\]', md)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    views_match = re.search(r'\*\*Views\*\*:\s*([\d,]+)', md)
    if views_match:
        metadata['views'] = views_match.group(1).replace(',', '')
    
    likes_match = re.search(r'\*\*Likes\*\*:\s*([\d,]+)', md)
    if likes_match:
        metadata['likes'] = likes_match.group(1).replace(',', '')
    
    desc = re.search(r'## Description\n```\n(.*?)```', md, re.DOTALL)
    if desc:
        metadata['description'] = desc.group(1)[:500]
    
    return metadata

# ─── Process one case ───
def process_case(case: dict) -> dict:
    """Full enrichment for one case."""
    cid = case['case_id']
    loc = case.get('location', '')
    year = case.get('year', '?')
    print(f"\n  PROCESSING: {cid} — {year} {loc}")
    
    result = {"case_id": cid, "wikipedia": {}, "youtube": []}
    
    # 1. Wikipedia
    result["wikipedia"] = scrape_wikipedia(case)
    
    # 2. YouTube references
    media_urls = case.get("media_urls", [])
    for media in media_urls:
        if isinstance(media, dict):
            url = media.get("url", "")
        else:
            url = media
        
        if "youtube.com" in url or "youtu.be" in url:
            yt_data = scrape_youtube(url)
            if yt_data:
                result["youtube"].append({"url": url, **yt_data})
    
    time.sleep(0.5)  # Small delay between cases
    return result

# ─── Main ───
def main():
    BATCH_SIZE = 5
    ALL_CASES = cases  # Full run of 50
    
    print(f"\n{'='*60}")
    print(f"PROJECT HEIMDALL — Data Enrichment Pipeline v2")  
    print(f"Cases: {len(ALL_CASES)} | Batch size: {BATCH_SIZE}")
    print(f"{'='*60}")
    
    for i in range(0, len(ALL_CASES), BATCH_SIZE):
        batch = ALL_CASES[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(ALL_CASES) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n>>> BATCH {batch_num}/{total_batches} (cases {i+1}-{min(i+BATCH_SIZE, len(ALL_CASES))})")
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(process_case, c): c for c in batch}
            for future in as_completed(futures):
                case = futures[future]
                try:
                    result = future.result()
                    cid = result['case_id']
                    log['cases'][cid] = result
                    
                    # Update case with enrichment
                    case_obj = next(c for c in cases if c['case_id'] == cid)
                    if result['wikipedia'].get('wikipedia_found'):
                        case_obj['wikipedia_url'] = result['wikipedia'].get('wikipedia_url', '')
                        ext = result['wikipedia'].get('extract', {})
                        if ext.get('date_detail') and not case_obj.get('date_detail'):
                            case_obj['date_detail'] = ext['date_detail']
                        if ext.get('classification_confirmed'):
                            case_obj['classification_source'] = 'Wikipedia confirms ' + ext['classification_confirmed']
                    else:
                        case_obj['wikipedia_url'] = ''
                    
                except Exception as e:
                    print(f"  ERROR processing {case['case_id']}: {e}")
                    log['cases'][case['case_id']] = {"error": str(e)}
        
        time.sleep(1.5)  # Rate limit between batches
    
    # Save enriched data
    enriched_file = "/root/project-heimdall/data/cases-v2-enriched.json"
    with open(enriched_file, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    
    # Save detailed log
    log["completed"] = datetime.now().isoformat()
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"Enriched data: {enriched_file}")
    print(f"Detailed log: {LOG_FILE}")
    
    # Summary stats
    wiki_found = sum(1 for v in log['cases'].values() if v.get('wikipedia', {}).get('wikipedia_found'))
    yt_found = sum(1 for v in log['cases'].values() if len(v.get('youtube', [])) > 0)
    errors = sum(1 for v in log['cases'].values() if 'error' in v)
    
    print(f"\nResults:")
    print(f"  Wikipedia pages found: {wiki_found}")
    print(f"  YouTube metadata extracted: {yt_found}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
