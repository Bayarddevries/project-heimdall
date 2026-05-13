"""
Build the v5 Tier 1 enriched JSON from the v5 CSV (56 cases).
Directly maps CSV fields into the v3 schema format expected by merge_v5.py.
"""
import csv, json, re
from pathlib import Path

CSV_PATH = Path("/root/project-heimdall/data/canadian_ufo_sightings_v5.csv")
OUTPUT = Path("/root/project-heimdall/data/cases-v3-tier1-enriched.json")

PROVINCE_MAP = {
    "AB": "Alberta", "BC": "British Columbia", "QC": "Quebec", "ON": "Ontario",
    "MB": "Manitoba", "SK": "Saskatchewan", "NS": "Nova Scotia", "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador", "PE": "Prince Edward Island",
    "NT": "Northwest Territories", "NU": "Nunavut", "YT": "Yukon",
}

# Contact type → Hynek label
CONTACT_LABELS = {
    "NL": "Nocturnal Lights / Night Lights",
    "RV": "Radar Visual",
    "DD": "Daylight Disc / Daylight Discs",
    "CE1": "Close Encounter 1st Kind",
    "CE2": "Close Encounter 2nd Kind",
    "CE3": "Close Encounter 3rd Kind",
    "CE4": "Close Encounter 4th Kind",
    "N/A": "Cultural / N/A",
}

CONTACT_DESC = {
    "NL": "Observed but no direct interaction or physical evidence.",
    "RV": "Radar-visual confirmation by military or ATC.",
    "DD": "Daylight observation with detailed visual or photographic evidence.",
    "CE1": "Close approach, sighting within 500 feet.",
    "CE2": "Physical evidence found at the scene.",
    "CE3": "Entities/beings observed or encountered.",
    "CE4": "Abduction experience reported.",
    "N/A": "Cultural or infrastructure case — a UFO-related installation or event.",
}

def extract_year(date_str):
    """Extract year from various date formats."""
    if not date_str:
        return 0
    year_match = re.search(r'\b(1[0-9]{3}|20[0-9]{2})\b', date_str)
    return int(year_match.group()) if year_match else 0

def extract_province(location):
    """Extract province abbreviation from location string."""
    prov_match = re.search(r',\s*([A-Z]{2})\b', location)
    return prov_match.group(1) if prov_match else ""

def extract_coords(coords_str):
    """Parse 'lat, lng' into list."""
    if not coords_str or "," not in coords_str:
        return [0.0, 0.0]
    parts = coords_str.split(",")
    try:
        return [float(parts[0].strip()), float(parts[1].strip())]
    except ValueError:
        return [0.0, 0.0]

cases = []
with open(CSV_PATH) as f:
    rows = list(csv.DictReader(f))

for i, row in enumerate(rows):
    cid = f"CAN-{i+1:03d}"
    loc = row["Location"]
    date_str = row["Date"]
    year = extract_year(date_str)
    prov_abbr = extract_province(loc)
    prov_full = PROVINCE_MAP.get(prov_abbr, "")
    coords = extract_coords(row["Coordinates"])
    contact = row["Contact (Hynek)"]
    if contact == "N/A":
        contact = "N/A"
    
    witnesses_str = row.get("Beings/Witnesses", "")
    evidence_str = row.get("Evidence/Physical Impact", "")
    source_str = row.get("Primary Source", "")
    
    shape = row.get("Shape", "Unknown")
    
    # Parse witness count from string
    wm = re.search(r'(\d+)\+?\s*(?:Witnesses?|residents?)', witnesses_str, re.IGNORECASE)
    wc = int(wm.group(1)) if wm else 0
    
    narrative = f"UFO sighting reported at {loc}. {date_str}. {witnesses_str}. {evidence_str}."
    
    case = {
        "case_id": cid,
        "date": date_str,
        "year": str(year),
        "year_int": year,
        "decade": f"{year // 10 * 10}s" if year > 0 else "Unknown",
        "location": loc,
        "province_id": prov_abbr,
        "province": prov_full,
        "latitude": coords[0],
        "longitude": coords[1],
        "coordinates": [coords[0], coords[1]],
        "shape": shape,
        "shape_detail": shape,
        "contact_type": contact,
        "hynek_classification": contact,
        "hynek_label": CONTACT_LABELS.get(contact, "Unknown"),
        "hynek_description": CONTACT_DESC.get(contact, ""),
        "being_type": "",
        "being_count": 0,
        "witness_count": wc,
        "being_type_detail": "",
        "witness_credibility": "MEDIUM - Documented",
        "physical_evidence": [evidence_str] if evidence_str else [],
        "media_urls": [],
        "source_primary": source_str,
        "narrative": narrative,
        "csv_evidence_summary": evidence_str,
        "csv_beings_summary": witnesses_str,
        "source_primary_csv": source_str,
        "internal_tier": "C",  # Will be recalculated by merge script
    }
    cases.append(case)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(cases, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(cases)} cases to {OUTPUT}")
print(f"Case IDs: {[c['case_id'] for c in cases]}")
