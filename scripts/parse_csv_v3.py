#!/usr/bin/env python3
"""
Project HEIMDALL — CSV → v3 Schema Parser
Reads CANADIAN UFO SIGHTINGS.csv and maps to expanded v3 schema.
Produces data/cases-v3.csv-enriched.json as output.
"""

import csv
import json
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
CSV_PATH = DATA_DIR / "raw_sightings.csv"
V2_PATH = DATA_DIR / "cases-v2.json"
V3_OUTPUT = DATA_DIR / "cases-v3.csv-enriched.json"

# ─── Hynek Classification Mapping ───────────────────────────────────
CONTACT_MAP = {
    "NL": "NL",
    "RV": "RV",
    "CE1": "CE1",
    "CE2": "CE2",
    "CE3": "CE3",
    "CE4": "CE4",
    "DD": "DD",
    "N/A": "N/A",
}

HYNEK_LABELS = {
    "NL": "Nocturnal Light",
    "RV": "Radar-Visual",
    "CE1": "Close Encounter of the First Kind",
    "CE2": "Close Encounter of the Second Kind",
    "CE3": "Close Encounter of the Third Kind",
    "CE4": "Close Encounter of the Fourth Kind",
    "DD": "Daylight Disc",
    "N/A": "Not Classified",
}

# ─── Tier Assignment Heuristics ──────────────────────────────────────
# A = Physical evidence + high-credibility witnesses + official records
# B = Multiple witnesses + documented but less physical evidence
# C = Single witness or limited documentation
def assign_tier(row):
    evidence = row.get("Evidence/Physical Impact", "").lower()
    contact = row.get("Contact (Hynek)", "").upper()
    witnesses = row.get("Beings/Witnesses", "").lower()
    source = row.get("Primary Source", "").lower()

    a_signals = 0
    b_signals = 0

    # Physical evidence markers
    if any(x in evidence for x in ["burn", "radiat", "soil", "mark", "trace", "crash", "foam", "sonar", "scorch", "ground"]):
        a_signals += 2
    if any(x in evidence for x in ["photo", "video", "cctv", "radar", "record"]):
        a_signals += 1

    # Witness credibility
    if any(x in witnesses for x in ["pilot", "military", "police", "officer", "rcmp", "rcaf", "parliament", "nurse"]):
        a_signals += 1
    elif any(x in witnesses for x in ["multiple", "1,000", "mass", "thousands", "dozens", "residents", "community"]):
        b_signals += 1

    # Official source
    if any(x in source for x in ["rcmp", "dnd", "usaf", "cadors", "mufon", "navy", "cgb", "hansard", "project magnet", "coast guard"]):
        a_signals += 1
    elif any(x in source for x in ["press", "gazette", "report"]):
        b_signals += 1

    # Contact type boosts
    if contact in ("CE2", "CE3", "CE4", "RV"):
        a_signals += 1
    elif contact in ("CE1", "DD"):
        b_signals += 1

    # Multi-witness events
    w_text = row.get("Beings/Witnesses", "")
    if any(x in w_text.lower() for x in ["11+", "1000s", "40+", "31", "thousands", "multiple"]):
        b_signals += 1

    if a_signals >= 3:
        return "A"
    elif a_signals >= 1 or b_signals >= 2:
        return "B"
    return "C"

# ─── Pattern Tag Generator ───────────────────────────────────────────
def generate_pattern_tags(row):
    tags = []
    evidence = row.get("Evidence/Physical Impact", "").lower()
    witnesses = row.get("Beings/Witnesses", "").lower()
    contact = row.get("Contact (Hynek)", "").upper()
    shape = row.get("Shape", "").lower()
    source = row.get("Primary Source", "").lower()
    location = row.get("Location", "").lower()

    # Evidence-based
    if any(x in evidence for x in ["burn", "radiat", "soil", "mark"]):
        tags.append("physical-trace")
    if any(x in evidence for x in ["photo", "35mm", "image"]):
        tags.append("photographic-evidence")
    if any(x in evidence for x in ["video", "youtube", "cctv", "vhs"]):
        tags.append("video-evidence")
    if any(x in evidence for x in ["radar", "sonar"]):
        tags.append("radar-confirmation")
    if "interfe" in evidence or "electromag" in evidence.lower():
        tags.append("electromagnetic-effects")

    # Witness-based
    if any(x in witnesses for x in ["pilot", "military", "police", "officer", "rcaf", "rcmp", "nurse", "parliament"]):
        tags.append("credible-witness")
    if any(x in witnesses for x in ["multiple", "1,000", "mass", "thousands", "dozens", "residents", "31", "40+"]):
        tags.append("mass-sighting")
    if "first nations" in witnesses:
        tags.append("indigenous-account")

    # Contact-based
    if contact in ("CE2", "CE3", "CE4"):
        tags.append(f"contact-{contact.lower()}")
    if contact == "RV":
        tags.append("radar-visual")
    if contact == "DD":
        tags.append("daylight-disc")

    # Shape-based
    if "disc" in shape or "saucer" in shape:
        tags.append("disc-shaped")
    if "triangle" in shape or "v-" in shape:
        tags.append("triangular")
    if "sphere" in shape or "orb" in shape or "ball" in shape:
        tags.append("spherical")
    if "light" in shape or "glow" in shape:
        tags.append("luminous")

    # Location-based
    if "urban" in location or any(city in location for city in ["montreal", "toronto", "vancouver", "ottawa", "calgary", "edmonton"]):
        tags.append("urban")
    if any(x in location for x in ["lake", "water", "harbour", "river", "gulf"]):
        tags.append("near-water")
    if "remote" in location or "nt" in location or "nu" in location or "yt" in location:
        tags.append("remote-location")

    # Cultural
    if "legend" in source.lower() or "lore" in source.lower():
        tags.append("folkloric")
    if "mufon" in source.lower():
        tags.append("mufon-case")
    if "cadors" in source.lower():
        tags.append("cadors-file")

    return sorted(set(tags))

# ─── Witness Credibility ─────────────────────────────────────────────
def compute_witness_credibility(row):
    witnesses = row.get("Beings/Witnesses", "").lower()
    contact = row.get("Contact (Hynek)", "").upper()

    high_signals = 0
    if any(x in witnesses for x in ["pilot", "military", "police", "officer", "rcaf", "rcmp", "parliament", "nurse"]):
        high_signals += 1
    if any(x in witnesses for x in ["multiple", "1,000", "mass", "thousands", "dozens", "residents", "community"]):
        high_signals += 1
    if contact in ("CE2", "CE3", "RV"):
        high_signals += 1

    if high_signals >= 2:
        return "High"
    elif high_signals == 1:
        return "Medium"
    return "Low"

# ─── Parse Date ──────────────────────────────────────────────────────
def parse_date(date_str):
    """Extract year and clean date string."""
    date_str = date_str.strip().strip('"')
    # Try to find a year
    year_match = re.search(r'(\d{4})', date_str)
    if year_match:
        year = int(year_match.group(1))
        return date_str, year
    return date_str, None

# ─── Parse Coordinates ───────────────────────────────────────────────
def parse_coordinates(coord_str):
    """Parse '45.5, -73.5' into floats."""
    coord_str = coord_str.strip().strip('"')
    parts = coord_str.split(",")
    if len(parts) == 2:
        try:
            lat = float(parts[0].strip())
            lng = float(parts[1].strip())
            return lat, lng
        except ValueError:
            pass
    return None, None

# ─── Parse Witness Count ─────────────────────────────────────────────
def parse_witness_count(text):
    """Extract approximate witness count from text."""
    text = text.lower()
    if "11+" in text:
        return 11
    if "1,000s" in text or "thousands" in text:
        return 1000
    if "40+" in text:
        return 40
    if "31" in text and "witness" in text:
        return 31
    if "dozens" in text:
        return 24
    if "multiple" in text:
        return 5
    num_match = re.search(r'(\d+)', text)
    if num_match:
        return int(num_match.group(1))
    return 1

# ─── Province from Location ──────────────────────────────────────────
def extract_province(location):
    prov_map = {
        "QC": "Quebec", "ON": "Ontario", "BC": "British Columbia",
        "MB": "Manitoba", "SK": "Saskatchewan", "AB": "Alberta",
        "NS": "Nova Scotia", "NB": "New Brunswick", "NL": "Newfoundland",
        "NT": "Northwest Territories", "YT": "Yukon", "NWT": "Northwest Territories",
        "NU": "Nunavut", "PEI": "Prince Edward Island",
    }
    for abbr, full in prov_map.items():
        if abbr in location.upper():
            return full
    return "Unknown"

# ─── Main Parser ─────────────────────────────────────────────────────
def main():
    # Load v2 for reference (narratives, etc.)
    v2_cases = {}
    if V2_PATH.exists():
        with open(V2_PATH) as f:
            for case in json.load(f):
                v2_cases[case.get("location", "")] = case

    csv_cases = []
    case_num = 0

    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            case_num += 1
            case_id = f"CAN-{case_num:03d}"

            # Parse core fields
            date_str, year = parse_date(row.get("Date", ""))
            lat, lng = parse_coordinates(row.get("Coordinates", ""))
            location = row.get("Location", "").strip().strip('"')
            shape = row.get("Shape", "").strip()
            contact = row.get("Contact (Hynek)", "").strip()
            beings = row.get("Beings/Witnesses", "").strip()
            evidence = row.get("Evidence/Physical Impact", "").strip()
            source = row.get("Primary Source", "").strip().strip('"')

            # Derive fields
            province = extract_province(location)
            tier = assign_tier(row)
            pattern_tags = generate_pattern_tags(row)
            witness_count = parse_witness_count(beings)
            credibility = compute_witness_credibility(row)
            contact_label = HYNEK_LABELS.get(contact, "Not Classified")

            # Find v2 narrative if available
            v2 = v2_cases.get(location, {})
            narrative = v2.get("narrative", "")
            source_secondary = v2.get("source_secondary", [])
            analyst_notes = v2.get("analyst_notes", "")

            case = {
                # ── Core Identity ──
                "case_id": case_id,
                "date": date_str,
                "year": year,
                "year_int": year,
                "location": location,
                "province": province,
                "latitude": lat,
                "longitude": lng,
                "coordinates": [lat, lng] if lat and lng else [],

                # ── Object Characteristics ──
                "shape": shape,
                "shape_detail": v2.get("shape_details", shape),
                "dimensions": v2.get("dimensions", ""),
                "size_certificate": v2.get("size_certainty", "LOW"),
                "size_estimate": "",
                "color": v2.get("color", ""),
                "light_color": v2.get("light_color", ""),
                "sound": v2.get("sound", "Not documented"),
                "movement_pattern": v2.get("movement_pattern", ""),
                "duration": v2.get("duration", ""),
                "speed": v2.get("speed", "Unknown"),
                "altitude": v2.get("altitude", "Unknown"),
                "trail_or_vapor": v2.get("trail_or_vapor", ""),
                "luminescence": "",
                "number_in_sky": v2.get("number_in_sky", 0),

                # ── Contact Classification ──
                "contact_type": contact,
                "hynek_classification": contact,
                "hynek_label": contact_label,
                "hynek_description": v2.get("hynek_description", ""),
                "being_type": v2.get("being_type", "N/A"),
                "being_count": v2.get("being_count", 0),
                "being_type_detail": v2.get("being_description", "No entities observed"),
                "being_height": v2.get("being_height", ""),
                "being_appearance": v2.get("being_appearance", ""),
                "being_clothing": v2.get("being_clothing", ""),
                "being_behavior": v2.get("being_behavior", ""),

                # ── Witnesses ──
                "witness_count": witness_count,
                "witness_credibility": credibility,
                "witness_names": v2.get("witness_names", []),
                "witnesses": v2.get("witness_details", beings),
                "witness_occupation": "",

                # ── Physical Evidence ──
                "physical_evidence": evidence,
                "environmental_trace": v2.get("environmental_trace", "None documented"),
                "electromagnetics": v2.get("electromagnetics", "Not applicable"),
                "medical_effects": v2.get("medical_effects", "None reported"),
                "radiation_detected": v2.get("radiation_detected", False),
                "radar_confirmation": contact == "RV",
                "media_urls": v2.get("media_urls", []),

                # ── Official Records ──
                "source_primary": source,
                "source_secondary": source_secondary,
                "cadors_report_url": v2.get("cadors_report_url", ""),
                "nuforc_links": v2.get("nuforc_links", ""),
                "rcmp_file_reference": "RCMP" in source.upper() or "RCMP" in evidence.upper(),
                "military_involvement": any(x in evidence.lower() + source.lower() for x in ["military", "rcaf", "navy", "usaf", "radar", "dnd"]),

                # ── Aftermath ──
                "aftermath_reported": v2.get("current_status", "") not in ("", "N/A"),
                "cultural_impact": v2.get("cultural_impact", "N/A"),
                "skepticism_analysis": v2.get("skepticism_analysis", "N/A"),
                "current_status": v2.get("current_status", "N/A"),
                "current_status_detail": v2.get("current_status_detail", ""),
                "analyst_notes": analyst_notes,

                # ── Relationships ──
                "pattern_tags": pattern_tags,
                "related_cases": [],
                "internal_tier": tier,
                "decade_cluster": f"{(year // 10) * 10}s" if year else "",
                "province_adjacent": [],

                # ── Narrative ──
                "narrative": narrative,

                # ── CSV Source Fields (preserve) ──
                "csv_evidence_summary": evidence,
                "csv_beings_summary": beings,
                "source_primary_csv": source,

                # ── Computed ──
                "richness_score": 0,  # filled after
                "adjacent": v2.get("adjacent", False),
                "weather_conditions": v2.get("weather", "Not documented"),
            }

            csv_cases.append(case)

    # ── Compute relatedness ──────────────────────────────────────────
    # Province + decade adjacency
    for i, c in enumerate(csv_cases):
        related = []
        provincial = [x["case_id"] for x in csv_cases if x["province"] == c["province"] and x["case_id"] != c["case_id"]]
        temporal = [x["case_id"] for x in csv_cases if abs((x.get("year_int") or 0) - (c.get("year_int") or 0)) <= 5 and x["case_id"] != c["case_id"]]
        shape_match = [x["case_id"] for x in csv_cases if x["shape"].lower() == c["shape"].lower() and x["case_id"] != c["case_id"]]

        c["province_adjacent"] = provincial[:5]
        related_set = list(set(provincial[:2] + temporal[:2] + shape_match[:2]))
        c["related_cases"] = related_set[:5]

    # ── Richness Score ───────────────────────────────────────────────
    # How many fields have meaningful data (0-100)
    def richness(c):
        score = 0
        total = 0
        skip = {"case_id", "date", "year", "year_int", "location", "province", "latitude", "longitude", "coordinates", "related_cases", "pattern_tags", "narrative", "source_primary_csv", "csv_evidence_summary", "csv_beings_summary"}
        for k, v in c.items():
            if k in skip:
                continue
            total += 1
            if v and str(v).strip() not in ("", "N/A", "Not documented", "Not applicable", "Unknown", "[]", 0, False, "False"):
                score += 1
        return round(score / max(total, 1) * 100)

    for c in csv_cases:
        c["richness_score"] = richness(c)

    # ── Write Output ─────────────────────────────────────────────────
    with open(V3_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(csv_cases, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(csv_cases)} cases to {V3_OUTPUT}")

    # ── Summary Stats ────────────────────────────────────────────────
    tiers = {}
    contacts = {}
    provinces = {}
    shapes = {}
    for c in csv_cases:
        t = c["internal_tier"]; tiers[t] = tiers.get(t, 0) + 1
        ct = c["contact_type"]; contacts[ct] = contacts.get(ct, 0) + 1
        p = c["province"]; provinces[p] = provinces.get(p, 0) + 1
        s = c["shape"]; shapes[s] = shapes.get(s, 0) + 1

    print(f"\n=== Tiers ===")
    for t in sorted(tiers): print(f"  {t}: {tiers[t]}")
    print(f"\n=== Contact Types ===")
    for ct in sorted(contacts): print(f"  {ct}: {contacts[ct]}")
    print(f"\n=== Provinces ===")
    for p in sorted(provinces, key=lambda x: provinces[x], reverse=True): print(f"  {p}: {provinces[p]}")
    print(f"\n=== Shapes ===")
    for s in sorted(shapes, key=lambda x: shapes[x], reverse=True): print(f"  {s}: {shapes[s]}")

    avg_rich = sum(c["richness_score"] for c in csv_cases) / len(csv_cases)
    print(f"\nAvg richness: {avg_rich:.1f}/100")

if __name__ == "__main__":
    main()
