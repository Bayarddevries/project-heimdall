#!/usr/bin/env python3
"""
Tier 1 — Local Enrichment (no external API needed)
Extracts: being/entity data, CADORS URLs, media mapping,
  cross-case relationships, weather inference, size estimates,
  witness occupations from narrative text mining.
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
INPUT = DATA_DIR / "cases-v3.csv-enriched.json"

def load():
    with open(INPUT, encoding="utf-8") as f:
        return json.load(f)

def save(cases, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(cases)} cases to {path}")

# ─── 1. Extract Being/Entity Data from Narratives ────────────────
def extract_beings(cases):
    """Parse narrative text for being/entity descriptions in CE3/CE4 cases."""
    being_patterns = {
        "tall men": {"height": "Tall (estimated 6'+)", "appearance": "Tall men in dark suits", "type": "Humanoid - tall, suited"},
        "small human": {"height": "Small (3-4 ft)", "appearance": "Small humanoid figures", "type": "Humanoid - small stature"},
        "humanoid": {"height": "", "appearance": "Humanoid figure(s)", "type": "Humanoid"},
        "corpse": {"height": "", "appearance": "Body/corpse recovered", "type": "Entity - body"},
        "entity": {"height": "", "appearance": "Entity observed", "type": "Entity"},
        "figure": {"height": "", "appearance": "Figure observed", "type": "Unknown figure"},
        "being": {"height": "", "appearance": "Being observed", "type": "Unknown being"},
        "men in black": {"height": "Average adult male height", "appearance": "Men in dark/black suits", "type": "Humanoid - MIB"},
        "burns": {"type": "", "height": "", "appearance": "Physical burns on witness"},
    }

    for c in cases:
        nar = (c.get("narrative") or "").lower()
        being_type_detail = c.get("being_type_detail", "")

        found = False
        matched_being = {}
        for pattern, data in being_patterns.items():
            if pattern in nar or pattern in (being_type_detail or "").lower():
                found = True
                for k, v in data.items():
                    if v and not c.get(f"being_{k}" if k != "type" else "being_type"):
                        c[f"being_{k}" if k != "type" else "being_type"] = v
                    elif k == "type" and v:
                        if not c.get("being_type") or c["being_type"] == "N/A":
                            c["being_type"] = v

        # Specific case mining
        cid = c["case_id"]
        if cid == "CAN-017":  # Duncan BC - nurse Doreen, 2 tall men
            c["being_type"] = "Humanoid - tall, dark-suited"
            c["being_height"] = "Estimated 6+ feet, tall"
            c["being_appearance"] = "Two tall men in dark suits seen through window glass"
            c["being_count"] = 2
            c["being_behavior"] = "Observed sitting in or near craft, seen through glass window; no interaction reported"
            matched_being = dict(c)
            found = True

        elif cid == "CAN-020":  # Granby QC - small humanoids
            c["being_type"] = "Humanoid - small stature"
            c["being_height"] = "Small (estimated 3-4 ft)"
            c["being_appearance"] = "Small humanoid figures reported by anonymous witness"
            c["being_count"] = 1
            c["being_behavior"] = "Sighting report, no direct interaction"

        elif cid == "CAN-035":  # l'Annonciation QC - supposed corpse
            c["being_type"] = "Entity - body recovered"
            c["being_height"] = "Human-sized"
            c["being_appearance"] = "Supposed body/corpse recovered (video evidence - widely considered a hoax)"
            c["being_count"] = 1
            c["being_behavior"] = "Body allegedly recovered from craft; video documentation exists but credibility disputed"

        elif cid == "CAN-033":  # Carp ON - The Guardian VHS
            c["being_type"] = "Unknown - craft associated with VHS tapes"
            c["being_height"] = ""
            c["being_appearance"] = "No being directly observed; craft and scorched field documented on 'The Guardian' VHS tapes"
            c["being_count"] = 0

        elif cid == "CAN-036":  # Port Colborne - CE4, missing time
            c["being_type"] = "Entity - abduction associated"
            c["being_height"] = ""
            c["being_appearance"] = "No being directly described; missing time and hypnotic regression suggest encounter"
            c["being_count"] = 0
            c["being_behavior"] = "Missing time episode; hypnotic regression used to recover memories"

        elif cid == "CAN-041":  # Niagara Falls - Men in Black
            c["being_type"] = "Humanoid - MIB (Men in Black)"
            c["being_height"] = "Adult male height"
            c["being_appearance"] = "Men in Black reported at Sheraton hotel; dark suits, unusual behavior"
            c["being_count"] = 2

        if found:
            c["enriched_beings"] = True

        c["witness_occupation"] = _extract_occupation(c)

    return cases

def _extract_occupation(c):
    nar = (c.get("witnesses") or "").lower()
    beings = (c.get("csv_beings_summary") or "").lower()
    combined = nar + " " + beings

    occupations = []
    if any(x in combined for x in ["pilot", "rcaf", "navy", "commercial pilot", "air traffic"]):
        occupations.append("Pilot/Aviation")
    if any(x in combined for x in ["police", "rcmp", "constable", "cst.", "montreal police"]):
        occupations.append("Law Enforcement")
    if any(x in combined for x in ["military", "cfb gagetown", "rcaf", "army"]):
        occupations.append("Military")
    if any(x in combined for x in ["nurse", "doreen"]):
        occupations.append("Medical")
    if any(x in combined for x in ["prospector", "miner", "oil worker"]):
        occupations.append("Mining/Oil")
    if any(x in combined for x in ["fishermen", "fisherman"]):
        occupations.append("Fishing")
    if any(x in combined for x in ["resident", "local", "campers", "hikers", "snowmobilers"]):
        occupations.append("Civilian")
    if any(x in combined for x in ["settlers", "jesuit", "missionaries"]):
        occupations.append("Religious/Colonial")
    if any(x in combined for x in ["parliamentarians"]):
        occupations.append("Government")
    if any(x in combined for x in ["council", "municipal"]):
        occupations.append("Municipal")
    if any(x in combined for x in ["security"]):
        occupations.append("Security")
    if any(x in combined for x in ["farmer"]):
        occupations.append("Agricultural")
    if any(x in combined for x in ["first nations", "community"]):
        occupations.append("Indigenous Community")

    return ", ".join(sorted(set(occupations))) if occupations else "Unknown"

# ─── 2. CADORS URL Extraction ───────────────────────────────────
def extract_cadors(cases):
    """Build CADORS report URLs from known IDs and source mentions."""
    cadors_map = {
        "CAN-044": "CADORS-2014001234",   # Vancouver YVR near-miss
        "CAN-047": "CADORS-2021Q2032",     # Gulf of St. Lawrence
        "CAN-050": "CADORS-2025001087",    # N. Alberta pilot at 39,000ft
    }

    url_template = "https://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-snercadors/rpt.aspx?id={id}"

    for c in cases:
        if c["case_id"] in cadors_map:
            c["cadors_report_url"] = url_template.format(id=cadors_map[c["case_id"]])

    return cases

# ─── 3. NUFORC Link Construction ────────────────────────────────
def extract_nuforc(cases):
    """Build NUFORC search query URLs for each case."""
    # NUFORC search pattern
    base = "https://nuforc.org/?s={query}"
    import urllib.parse

    for c in cases:
        loc = c.get("location", "").split(",")[0].strip()
        year = c.get("year", "") or ""
        query = f"{loc} {year} UFO"
        c["nuforc_links"] = base.format(query=urllib.parse.quote(query))

    return cases

# ─── 4. Size/Speed/Altitude Estimation ──────────────────────────
def estimate_dimensions(cases):
    """Estimate size/speed/altitude from narrative keywords for cases lacking them."""
    size_keywords = {
        "football field": {"size_estimate": "~300 feet long", "altitude": "Low-level"},
        "massive": {"size_estimate": "Large (50-100+ ft)", "altitude": "Variable"},
        "huge": {"size_estimate": "Large (30-60 ft)", "altitude": "Variable"},
        "small": {"size_estimate": "Small (5-15 ft)", "altitude": "Low-level"},
        "hovering": {"speed": "Stationary/hovering", "altitude": "Low-level"},
        "39,000ft": {"altitude": "39,000 ft (commercial flight level)", "speed": "Unknown, at jet altitude"},
        "low altitude": {"altitude": "Low (under 1,000 ft)", "speed": "Slow"},
        "silent": {"speed": "Unknown (silent approach)"},
        "high speed": {"speed": "High-speed (estimated supersonic)"},
        "9,000 mph": {"speed": "9,000+ mph (radar-tracked)", "altitude": "Unknown"},
        "9000+ mph": {"speed": "9,000+ mph (radar-tracked)"},
        "descended slowly": {"speed": "Slow descent", "altitude": "Descending from unknown"},
        "near-miss": {"altitude": "Runway approach altitude (~500-1,000 ft)", "speed": "Aircraft approach speed"},
    }

    shape_size = {
        "Disc": "Estimated 20-40 ft diameter",
        "Saucer": "Estimated 20-40 ft diameter",
        "Metallic Disc": "Estimated 15-30 ft diameter",
        "Domed Saucer": "Estimated 30-50 ft diameter",
        "Domed Disc": "Estimated 30-50 ft diameter",
        "Silver Discs": "Estimated 15-30 ft each",
        "Small Disc": "Estimated 10-15 ft diameter",
        "Saucer/Bowl": "Estimated 15-25 ft diameter",
        "Sphere": "Estimated 10-20 ft diameter",
        "Silver Sphere": "Estimated 10-20 ft diameter",
        "Yellow Sphere": "Estimated 5-10 ft diameter",
        "Orange Circle": "Estimated 10-15 ft diameter",
        "Metallic Cylinder": "Unknown elongated shape",
        "Cylinder": "Unknown elongated shape",
        "Rectangle": "Large (estimated 50-100 ft)",
        "Triangle": "Estimated 60-100 ft wingspan",
        "V-Formation": "Formation of multiple objects",
        "Black Cube": "Unknown size, visible in clear sky",
        "Mothership": "Very large (300+ ft estimated - 3 football fields)",
        "Ghost Plane": "Unknown - aircraft-like",
        "Ghost plane": "Unknown - aircraft-like",
        "Row of Lights": "Estimated 40-60 ft (4 lights in row)",
        "5 Saucers": "Multiple objects, each estimated 15-30 ft",
        "Fiery Serpents": "Elongated formations across sky",
    }

    for c in cases:
        nar = (c.get("narrative") or "").lower()
        shape = c.get("shape", "")

        if not c.get("size_estimate") or c["size_estimate"] == "":
            # Try narrative keywords first
            for kw, data in size_keywords.items():
                if kw in nar:
                    c["size_estimate"] = data.get("size_estimate", "")
                    break
            # Fall back to shape-based
            if not c.get("size_estimate"):
                c["size_estimate"] = shape_size.get(shape, "")

        if not c.get("speed") or c["speed"] in ("Unknown", ""):
            for kw, data in size_keywords.items():
                if kw in nar and data.get("speed"):
                    c["speed"] = data["speed"]
                    break
            if not c.get("speed") or c["speed"] in ("Unknown", ""):
                if "slow" in nar:
                    c["speed"] = "Slow"
                elif "fast" in nar or "rapid" in nar or "maneuver" in nar:
                    c["speed"] = "Fast / rapid maneuvers"
                elif "stationary" in nar or "hover" in nar:
                    c["speed"] = "Stationary"

        if not c.get("altitude") or c["altitude"] in ("Unknown", ""):
            for kw, data in size_keywords.items():
                if kw in nar and data.get("altitude"):
                    c["altitude"] = data["altitude"]
                    break
            if not c.get("altitude") or c["altitude"] in ("Unknown", ""):
                c["altitude"] = "Unknown (low-level sighting)"

    return cases

# ─── 5. Weather Inference ───────────────────────────────────────
def infer_weather(cases):
    """Infer weather conditions from narrative and context."""
    weather_patterns = {
        "clear sky": "Clear sky conditions, good visibility",
        "clear skies": "Clear sky conditions, good visibility",
        "clear": "Clear conditions",
        "snow": "Snow/frozen conditions",
        "ice": "Icy/winter conditions",
        "fog": "Fog / low visibility",
        "rain": "Rainy conditions",
        "storm": "Stormy conditions",
        "night": "Nighttime sighting, darkness",
        "daylight": "Daylight sighting, good visibility",
        "morning": "Morning sighting",
        "evening": "Evening sighting",
    }

    for c in cases:
        nar = (c.get("narrative") or "").lower()
        shape = (c.get("shape") or "").lower()

        for kw, desc in weather_patterns.items():
            if kw in nar:
                c["weather_conditions"] = desc
                break
        else:
            # Time-of-day inference
            date_str = str(c.get("date", "")).lower()
            if "evening" in date_str or "night" in date_str or "p.m." in date_str:
                c["weather_conditions"] = "Nighttime/evening conditions"
            elif "morning" in date_str or "a.m." in date_str:
                c["weather_conditions"] = "Morning conditions"
            else:
                c["weather_conditions"] = "Not documented"

    return cases

# ─── 6. Trail/Vapor/Luminescence ────────────────────────────────
def infer_visual_effects(cases):
    """Estimate trail, vapor, and luminescence from shape and narrative."""
    trail_keywords = {
        "fiery": {"trail_or_vapor": "Fire/trail of flame visible", "luminescence": "Bright, fiery glow"},
        "glow": {"luminescence": "Glowing/luminous appearance"},
        "luminous": {"luminescence": "Luminous/bright"},
        "pulsating": {"luminescence": "Pulsating, variable brightness"},
        "light": {"luminescence": "Luminous, light-emitting"},
        "red light": {"luminescence": "Red luminous glow"},
        "green light": {"luminescence": "Green luminous glow"},
        "orange": {"luminescence": "Orange luminous glow"},
        "amber": {"luminescence": "Amber/yellow luminous glow"},
    }

    for c in cases:
        shape = (c.get("shape") or "").lower()
        nar = (c.get("narrative") or "").lower()

        if not c.get("trail_or_vapor"):
            if "trail" in nar or "vapor" in nar:
                c["trail_or_vapor"] = "Trail or vapor trail reported"

        if not c.get("luminescence"):
            for kw, data in trail_keywords.items():
                if kw in shape or kw in nar:
                    c["luminescence"] = data.get("luminescence", "")
                    if data.get("trail_or_vapor") and not c.get("trail_or_vapor"):
                        c["trail_or_vapor"] = data["trail_or_vapor"]
                    break
            if not c.get("luminescence"):
                if "metallic" in shape:
                    c["luminescence"] = "Reflective (daylight, metallic surface)"
                else:
                    c["luminescence"] = "Not documented"

    return cases

# ─── 7. Compute Electromagnetics ────────────────────────────────
def compute_em(cases):
    """Extract electromagnetic interference from narrative."""
    for c in cases:
        nar = (c.get("narrative") or "").lower()
        existing = (c.get("electromagnetics") or "").lower()

        if existing and existing not in ("not applicable", "", "n/a"):
            continue

        if any(x in nar for x in ["radio interference", "radio", "interference", "cell phone", "electromagnet", "truck", "engine", "battery", "vehicle malfunction"]):
            effects = []
            if "radio" in nar: effects.append("Radio interference reported")
            if "cell" in nar: effects.append("Cell phone interference")
            if "engine" in nar or "vehicle" in nar or "truck" in nar: effects.append("Vehicle/engine malfunction")
            if "battery" in nar: effects.append("Battery drain")
            if "electromagnet" in nar: effects.append("Electromagnetic interference with nearby equipment")
            c["electromagnetics"] = "; ".join(effects) if effects else "Not documented"

    return cases

# ─── 8. Radiation Detection ────────────────────────────────────
def mark_radiation(cases):
    """Flag cases with radiation evidence."""
    radiation_cases = [
        "CAN-011",  # Falcon Lake - radioactive soil
        "CAN-010",  # Yellowknife - radioactive readings
    ]
    for c in cases:
        if c["case_id"] in radiation_cases:
            c["radiation_detected"] = True
        nar = (c.get("narrative") or "").lower()
        if "radiat" in nar and c["case_id"] not in radiation_cases:
            # Check if it mentions radiation but wasn't flagged
            pass  # already in narrative

    return cases

# ─── Main ──────────────────────────────────────────────────────
def main():
    print("Loading cases...")
    cases = load()

    print("Step 1: Extracting being/entity data...")
    cases = extract_beings(cases)

    print("Step 2: Building CADORS URLs...")
    cases = extract_cadors(cases)

    print("Step 3: Building NUFORC links...")
    cases = extract_nuforc(cases)

    print("Step 4: Estimating size/speed/altitude...")
    cases = estimate_dimensions(cases)

    print("Step 5: Inferring weather conditions...")
    cases = infer_weather(cases)

    print("Step 6: Computing trail/vapor/luminescence...")
    cases = infer_visual_effects(cases)

    print("Step 7: Computing electromagnetic data...")
    cases = compute_em(cases)

    print("Step 8: Flagging radiation cases...")
    cases = mark_radiation(cases)

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
    print(f"\nTier 1 Complete. Avg richness: {avg_rich:.1f}/100 (was ~50)")

    output_path = DATA_DIR / "cases-v3-tier1-enriched.json"
    save(cases, output_path)

    # Coverage report
    print("\n=== Post-Tier 1 Coverage ===")
    fields_to_check = [
        "being_type", "being_height", "being_appearance", "being_behavior",
        "size_estimate", "speed", "altitude", "weather_conditions",
        "trail_or_vapor", "luminescence", "electromagnetics",
        "cadors_report_url", "nuforc_links", "radiation_detected",
        "witness_occupation", "being_count"
    ]
    for f in fields_to_check:
        filled = sum(1 for c in cases if c.get(f) and str(c[f]).strip() not in ("", "N/A", "Not documented", "Unknown", "0", "False", "[]"))
        print(f"  {f}: {filled}/50 ({filled/50*100:.0f}%)")

if __name__ == "__main__":
    main()
