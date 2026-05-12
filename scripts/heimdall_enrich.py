#!/usr/bin/env python3
"""
Project HEIMDALL — Data Enrichment Pipeline v3
Sequential Firecrawl scraping with retry + known Wikipedia URLs.
Writes enriched data to data/cases-v3.json
"""

import json
import time
import re
import sys
import os

API_KEY = "fc-4d7a7ed5608f4ad197091d46c9d34ebf"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cases-v2.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cases-v3.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "enrich_cache.json")

# ── Known Wikipedia pages (direct URLs, no search) ──
WIKI_PAGES = {
    "CAN-012": "https://en.wikipedia.org/wiki/1967_Falcon_Lake_incident",
    "CAN-013": "https://en.wikipedia.org/wiki/1967_Shag_Harbour_UFO_incident",
    "CAN-023": "https://en.wikipedia.org/wiki/Charlie_Redstar",
    "CAN-038": "https://en.wikipedia.org/wiki/Fox_Lake_UFO_incident",
    "CAN-015": "https://en.wikipedia.org/wiki/St._Paul,_Alberta#UFO",
    "CAN-028": "https://en.wikipedia.org/wiki/Nahanni_Valley#Legend",
    "CAN-018": "https://en.wikipedia.org/wiki/1970_Duncan_UFO_incident",
    "CAN-016": "https://en.wikipedia.org/wiki/RCAF_Station_Rivers",  # partial
    "CAN-047": "https://en.wikipedia.org/wiki/CADORS",  # aviation reporting system
    "CAN-044": "https://en.wikipedia.org/wiki/Aviation_safety#Canada",
    "CAN-048": "https://en.wikipedia.org/wiki/Hafford",
}

# ── Load base cases ──
with open(DATA_PATH) as f:
    cases = json.load(f)

# ── Load cache if exists ──
cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE) as f:
        cache = json.load(f)
    print(f"Loaded cache with {len(cache)} entries")


def firecrawl_scrape(url, max_retries=3):
    """Scrape a URL with Firecrawl v2, retry on failure."""
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "skipTlsVerification": True,
    }).encode()

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                "https://api.firecrawl.dev/v2/scrape",
                data=body,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                result = json.loads(resp.read().decode())
                md = result.get("data", {}).get("markdown", "")
                if md and len(md) > 100:
                    return md
                return None
        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"    Attempt {attempt + 1} failed: {e}. Waiting {wait}s...")
            time.sleep(wait)
    return None


def extract_from_wiki(md, case):
    """Extract structured fields from Wikipedia markdown."""
    if not md:
        return {}

    updates = {}

    # Extract first-hand account / quotes
    quotes = []
    for line in md.split("\n"):
        if line.strip().startswith(">"):
            quote = line.strip().lstrip("> ")
            quotes.append(quote)
    if quotes:
        updates["first_hand_quotes"] = quotes[:5]

    # Extract any mention of dimensions/size
    dim_patterns = [
        r"(\d+\s*(?:feet|ft|meters|m|kilometers|km|miles|mi))",
        r"(\d+\s*x\s*\d+)",
    ]
    dimensions = []
    for pat in dim_patterns:
        for m in re.finditer(pat, md, re.IGNORECASE):
            dimensions.append(m.group(1))
    if dimensions and not case.get("dimensions"):
        updates["wiki_dimensions"] = list(set(dimensions))[:5]

    # Extract mention of witnesses count
    witness_patterns = [
        r"(\d+)\s*witness",
        r"(\d+)\s*people?\s*saw",
        r"(\d+)\s*peopl",
    ]
    for pat in witness_patterns:
        m = re.search(pat, md, re.IGNORECASE)
        if m:
            updates["wiki_witness_count"] = int(m.group(1))
            break

    # Extract narrative — grab the first few paragraphs that aren't headers
    paragraphs = []
    in_content = False
    for line in md.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# ") or stripped.startswith("=="):
            in_content = True
            continue
        if stripped and in_content and not stripped.startswith("[") and not stripped.startswith("{{") and not stripped.startswith("|") and not stripped.startswith("- "):
            paragraphs.append(stripped)
    if paragraphs:
        updates["wiki_narrative_summary"] = "\n\n".join(paragraphs[:8])

    # Extract media mentions (images)
    image_mentions = []
    for line in md.split("\n"):
        img_match = re.search(r"\!\[(.*?)\]\((.*?)\)", line)
        if img_match:
            image_mentions.append({
                "caption": img_match.group(1),
                "url": img_match.group(2),
            })
    if image_mentions:
        updates["wiki_images"] = image_mentions[:10]

    # Extract references/external links
    refs = []
    in_refs = False
    for line in md.split("\n"):
        if "References" in line or "External links" in line or "==References==" in line:
            in_refs = True
            continue
        if in_refs and line.startswith("^[") or line.startswith("* "):
            refs.append(line.strip())
        if in_refs and line.startswith("==") and "References" not in line:
            break
    if refs:
        updates["wiki_references"] = refs[:10]

    return updates


def firecrawl_search(query, max_results=3):
    """Use Firecrawl search to find relevant pages."""
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "query": query,
        "limit": max_results,
    }).encode()

    try:
        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/search",
            data=body,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            result = json.loads(resp.read().decode())
            return result.get("data", [])
    except Exception as e:
        print(f"    Search error: {e}")
        return []


# ── Main loop ──
print(f"Enriching {len(cases)} cases...")
print("=" * 60)

for i, case in enumerate(cases):
    cid = case["case_id"]
    loc = case["location"]
    year = case["year"]

    # Skip if already cached
    if cid in cache and cache[cid].get("status") == "done":
        print(f"[{i+1:02d}] {cid} {loc} ({year}) — CACHED, skipping")
        # Apply cached data
        for key, val in cache[cid].get("data", {}).items():
            case[key] = val
        continue

    print(f"\n[{i+1:02d}] {cid} {loc} ({year})")
    print("=" * 50)

    updates = {}

    # Strategy 1: Direct Wikipedia URL
    wiki_url = WIKI_PAGES.get(cid)
    if wiki_url:
        print(f"  → Scraping Wikipedia: {wiki_url}")
        md = firecrawl_scrape(wiki_url)
        if md:
            wiki_data = extract_from_wiki(md, case)
            updates.update(wiki_data)
            updates["wikipedia_url"] = wiki_url
            # Save raw markdown to cache
            cache[f"{cid}_wiki_raw"] = md[:5000]  # truncate
            print(f"  ✓ Got {len(md)} chars from Wikipedia")

    # Strategy 2: NUFORC search
    # Try to find NUFORC reports
    if not cache.get(f"{cid}_nuforc"):
        print(f"  → Searching NUFORC...")
        nuforc_query = f"site:nuforc.org {loc} {year} UFO"
        results = firecrawl_search(nuforc_query, max_results=2)
        if results:
            nuforc_urls = [r.get("url", "") for r in results if r.get("url")]
            updates["nuforc_links"] = nuforc_urls
            cache[f"{cid}_nuforc"] = nuforc_urls
            print(f"  ✓ Found {len(nuforc_urls)} NUFORC links")

    # Strategy 3: CADORS search for aviation-related cases
    if case.get("hynek_classification") in ["RV", "DD"] or "CADORS" in case.get("source_primary", ""):
        if not cache.get(f"{cid}_cadors"):
            print(f"  → Searching CADORS...")
            cadors_query = f"site:tc.gc.ca CADORS {loc} {year}"
            results = firecrawl_search(cadors_query, max_results=2)
            if results:
                cadors_urls = [r.get("url", "") for r in results if r.get("url")]
                updates["cadors_report_url"] = cadors_urls
                cache[f"{cid}_cadors"] = cadors_urls
                print(f"  ✓ Found {len(cadors_urls)} CADORS links")

    # Strategy 4: General web search for media
    if not cache.get(f"{cid}_media") and len(case.get("media_urls", [])) < 2:
        print(f"  → Searching for media...")
        media_query = f"UFO {loc} {year} site:youtube.com OR site:imgur.com OR photo"
        results = firecrawl_search(media_query, max_results=3)
        if results:
            media_urls = [r.get("url", "") for r in results if r.get("url")]
            if media_urls:
                existing = case.get("media_urls", [])
                existing.extend(media_urls)
                updates["media_urls"] = existing[:5]
                cache[f"{cid}_media"] = media_urls
                print(f"  ✓ Found {len(media_urls)} media links")

    # Save cached progress
    cache[cid] = {"status": "done", "data": updates}

    # Apply to case
    for key, val in updates.items():
        case[key] = val

    # Save cache after each case
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    # Polite delay
    time.sleep(3)

# ── Write output ──
with open(OUTPUT_PATH, "w") as f:
    json.dump(cases, f, indent=2)

print("\n" + "=" * 60)
print("DONE!")
print(f"Output: {OUTPUT_PATH}")
print(f"Cache: {CACHE_FILE}")

# Print summary
new_fields = 0
for case in cases:
    for key in case:
        if key.startswith("wiki") or key.startswith("nuforc") or key.startswith("cadors"):
            if case.get(key):
                new_fields += 1
print(f"New fields populated: {new_fields}")
