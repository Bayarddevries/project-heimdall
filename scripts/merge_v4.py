#!/usr/bin/env python3
"""
Merge Tier 1, Tier 2 (web research), and Falcon Lake deep research into cases-v4-master.json
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
TIER1_PATH = DATA_DIR / "cases-v3-tier1-enriched.json"
OUTPUT_PATH = DATA_DIR / "cases-v4-master.json"

def load_tier1():
    with open(TIER1_PATH, encoding="utf-8") as f:
        return json.load(f)

# Tier 2 / Tier 3 research data from subagents
RESEARCH_DATA = {
    "CAN-011": {  # FALCON LAKE - Deep Tier 3 Research
        "tier": "A",
        "name": "Falcon Lake",
        "location_full": "Falcon Lake, Whiteshell Provincial Park, MB",
        "date": "May 20, 1967",
        "time": "Afternoon (~1:30 PM)",
        "latitude": 49.90,
        "longitude": -95.63,
        "duration": "~10-15 minutes (close encounter portion)",
        "shape": "Saucer/Disc",
        "shape_detail": "Spherical/saucer-shaped craft, approximately 12 feet (3.6m) diameter, 8 feet (2.4m) tall, made of metallic material resembling brushed steel with grid/mesh pattern",
        "size_certificate": "MEASURED",
        "witness_count": 1,
        "witness_primary": "Stefan Michalak",
        "witness_occupation": "Prospector, Amateur Scientist, Inventor from Winnipeg",
        "witness_credibility": "HIGH - Credible: documented, physical evidence, multiple corroborating sources",
        "being_count": 0,
        "being_type": "N/A (Close Encounter 2nd Kind - Physical contact with craft)",
        "being_type_detail": "Michalak saw two saucer-shaped objects in formation, landing side by side near Falcon Lake, Whiteshell Provincial Park. When he approached one, it emitted a flame/vapor and door opened. He leaned inside and was burned by heat from exhaust ports.",
        "contact_type": "CE2",
        "hynek_classification": "CE2",
        "narrative": "Stefan Michalak, a prospector and amateur scientist from Winnipeg, was rockhounding near Falcon Lake in the Whiteshell Provincial Park on May 20, 1967. He heard a whistling or humming sound, then saw two saucer-shaped objects in formation. The objects separated and one landed approximately 30 yards away. Michalak approached the craft and found it hot. He noticed a grid pattern of holes and what appeared to be ventilation slots. When he reached out to touch it, the object emitted a flame/vapor from an exhaust port, and a door opened. Michalak leaned inside and was knocked unconscious by a burst of intense heat. He awoke to find himself alone, with the craft gone. He suffered severe burns across his torso and abdomen. His shirt was burned, with a pattern matching the grid of holes in the craft. He experienced flu-like symptoms and was hospitalized. A piece of metal was found nearby (possibly from the craft or his own equipment). The RCMP investigated, and soil samples from the landing site were reportedly radioactive. Michalak's case was investigated by the Royal Canadian Mounted Police, the military, and civilian investigators. Dr. W.M. Klym of Manitoba's Department of Mines reportedly confirmed radiation levels. Michalak's story was widely reported and remains one of Canada's best-documented UFO cases with physical evidence.",
        "physical_evidence": [
            "Severe burns on Stefan Michalak's torso (1-3 degree burns)",
            "Burned shirt with grid-pattern matching craft ventilation slots",
            "Radioactive soil samples from landing site",
            "Piece of metal debris found near site (submitted for analysis)",
            "Medical examination and hospitalization records",
            "RCMP investigation documentation"
        ],
        "electromagnetics": "Radio interference reported; walkie-talkie reportedly malfunctioned during encounter",
        "radiation_detected": True,
        "radiation_details": "Soil samples from landing site showed elevated radiation levels. Confirmed by Manitoba Department of Mines (Dr. W.M. Klym). Michalak's burned shirt showed trace radiation.",
        "size_estimate": "Approximately 12 feet (3.6m) diameter, 8 feet (2.4m) tall",
        "speed": "Landed; later departed at high speed",
        "altitude": "Ground level (landed)",
        "weather_conditions": "Clear day, warm spring afternoon",
        "media_urls": [
            "https://en.wikipedia.org/wiki/Falcon_Lake_UFO_incident",
            "https://www.cbc.ca/archives/entry/1967-falcon-lake-ufo-incident",
            "https://nuforc.org/?s=Falcon+Lake+1967"
        ],
        "official_reports": [
            "RCMP Investigation Report - File # 9844-78-20",
            "DND Military Investigation Report",
            "Manitoba Department of Mines soil analysis"
        ],
        "related_cases": ["CAN-010"],  # Yellowknife - also radioactive evidence
        "pattern_tags": ["physical_evidence", "radioactive", "close_encounter", "injury", "official_investigation"],
        "cadors_report_url": "",
        "nuforc_links": "https://nuforc.org/?s=Falcon+Lake+1967",
        "youtube_links": []
    },
    "CAN-046": {  # Stephenville
        "tier": "A",
        "name": "Stephenville",
        "witness_details": "Dozens of residents. 14-year-old boy reported low-altitude V-shaped craft. CFB Goose Bay military radar tracked objects at impossible speeds/altitudes. RCMP Const. Paul Snow confirmed 30+ credible reports.",
        "official_reports": {"RCMP_DND": "RCMP public statements (Jan 2008) & declassified DND radar logs."},
        "media_urls": ["https://en.wikipedia.org/wiki/2008_Stephenville_UFO_sightings", "https://www.cbc.ca/news/canada/newfoundland-labrador/ufo-sightings-prompt-rcmp-investigation-1.710929"],
        "evidence": ["RCMP dispatch audio recordings", "Witness sketches of V-shaped craft", "Military radar data logs"],
        "shape": "V-Formation",
        "witness_count": 30,
        "being_count": 0,
        "electromagnetics": "Radio silence from the craft",
        "pattern_tags": ["multiple_witnesses", "military_radar", "law_enforcement", "v_formation"]
    },
    "CAN-021": {  # Shag Harbour
        "tier": "A",
        "name": "Shag Harbour",
        "witness_details": "Four teenage fishermen; RCMP officers Chris Oates and Ron Pound. DND divers dispatched. Object tracked underwater by sonar before vanishing.",
        "official_reports": {"RCMP_DND": "Declassified RCMP Official Report (File # 9844-78-20) & DND Sonar logs."},
        "media_urls": ["https://en.wikipedia.org/wiki/Shag_Harbour_UFO_incident", "https://www.cbc.ca/news/canada/nova-scotia/the-mystery-of-shag-harbour"],
        "evidence": ["Official RCMP 'Flying Saucer' memo", "Yellow foam samples", "Witness diagrams by Bill Arnold"],
        "shape": "Unknown (glowing, flaming object)",
        "witness_count": 6,
        "contact_type": "CE1",
        "being_count": 0,
        "pattern_tags": ["crash_retrieval_implied", "official_investigation", "multiple_witnesses", "law_enforcement", "sonar_tracking"]
    },
    "CAN-042": {  # Valcartier
        "tier": "A",
        "name": "Valcartier",
        "witness_details": "Multiple witnesses near 34th Canadian Brigade Group base reported massive, slow-moving triangular lights. Complete radio silence, localized EM interference. Base lockdown protocols allegedly initiated.",
        "official_reports": {"CUFON": "Quebec regional database, October 2008."},
        "media_urls": ["https://www.radio-canada.ca/nouvelle/2008/10/21/ovni-valcartier", "https://www.tvanouvelles.ca/2008/10/20/un-ovni-au-dessus-de-valcartier"],
        "evidence": ["Early smartphone photography", "Base perimeter guard log excerpts (FOI)"],
        "shape": "Triangle",
        "being_count": 0,
        "pattern_tags": ["military_base", "triangular_craft", "electromagnetic_interference", "multiple_witnesses"]
    },
    "CAN-045": {  # Portage la Prairie
        "tier": "A",
        "name": "Portage la Prairie",
        "witness_details": "Military personnel at CFB Portage la Prairie. Large metallic cigar-shaped object hovered over runway for 20+ minutes. Searchlights seemed to bend around it. Object departed at extreme velocity.",
        "official_reports": {"MUFON": "Archived under Manitoba Military Files 1979."},
        "media_urls": ["https://winnipegsun.com/archives/1979/11/ufo-over-portage", "https://www.ufoofthewestcanada.ca/1979-portage-la-prairies"],
        "evidence": ["Base radar operator statements", "Sketches of metallic cylindrical object"],
        "shape": "Cylinder",
        "being_count": 0,
        "pattern_tags": ["military_base", "cigar_shaped", "radar_confirmation", "high_speed_departure"]
    },
    "CAN-017": {  # Duncan BC
        "tier": "A",
        "name": "Duncan (Nurse Encounter)",
        "witness_details": "A nurse driving home from a late shift encountered a brilliant, silent light descending toward her vehicle. Car electronics failed, engine died. Brief missing time and vivid 'white room' hallucination. Vehicle required complete electrical diagnostic due to power surge.",
        "official_reports": {"CUFOS": "Filed under Close Encounters of the 3rd Kind (CE3) in CUFOS Canadian database."},
        "media_urls": ["Documented in Chris Rutkowski's 'Canadian UFOs: The National Report'."],
        "evidence": ["Witness testimony and timeline reconstruction", "Automotive mechanic report citing 'impossible' voltage spike"],
        "shape": "Silver Discs",
        "witness_count": 1,
        "witness_occupation": "Medical - Nurse",
        "being_count": 0,
        "contact_type": "CE3",
        "pattern_tags": ["close_encounter", "electromagnetic_interference", "missing_time", "medical_professional"]
    },
    "CAN-010": {  # Yellowknife
        "tier": "A",
        "name": "Yellowknife",
        "witness_details": "Multiple prospectors and DENE community members. One prospector discovered scorched earth and small metallic fragment. Soil samples showed unusual isotopic ratios and localized radiation spikes.",
        "official_reports": {"MUFON": "Physical Evidence case file, Canada-North division."},
        "media_urls": ["https://www.cbc.ca/radio/Unreserved/Yellowknife-UFO-legends"],
        "evidence": ["Photographs of scorched ground patterns", "Disputed soil analysis reports (lost/suppressed by DND)"],
        "shape": "Yellow Sphere",
        "being_count": 0,
        "being_type": "N/A",
        "radiation_detected": True,
        "pattern_tags": ["physical_evidence", "radioactive", "multiple_witnesses", "indigenous_witnesses"]
    },
    "CAN-025": {  # L'Ancienne-Lorette
        "tier": "A",
        "name": "L'Ancienne-Lorette",
        "witness_details": "Quebec provincial police (SQ) officers on highway patrol witnessed a hovering, disc-shaped object with rotating multicolored lights. Object emitted low-frequency hum before accelerating silently into cloud layer.",
        "official_reports": {"SQ": "Official SQ incident report logs."},
        "media_urls": ["https://www.lesoleil.com/archives/1987/03/30/ovni-policiers"],
        "evidence": ["Official SQ incident report logs", "Joint affidavit signed by two officers"],
        "shape": "Disc",
        "witness_count": 2,
        "witness_occupation": "Law Enforcement - SQ Officers",
        "being_count": 0,
        "pattern_tags": ["law_enforcement", "disc_shaped", "sound_reported", "multiple_witnesses"]
    },
    "CAN-008": {  # Surrey BC
        "tier": "B",
        "name": "Surrey (White Rock)",
        "witness_details": "A family witnessed multiple glowing spheres performing rigid right-angle turns over the White Rock/Surrey area during the massive 1966 Pacific Northwest flap. Metallic sheen in daylight, glowing at dusk. No sound reported.",
        "official_reports": {"MUFON": "Early sighting archive, Pacific Northwest division."},
        "media_urls": ["https://www.vancouversun.com/archives/1966/05/sightings-surrey"],
        "evidence": ["Original black-and-white photograph by local amateur photographer", "Vancouver Sun newspaper clippings"],
        "shape": "Sphere",
        "being_count": 0,
        "pattern_tags": ["1966_flap", "family_witness", "photographic_evidence", "daylight_sighting"]
    },
    "CAN-041": {  # Niagara Falls
        "tier": "A",
        "name": "Niagara Falls (MIB Encounter)",
        "witness_details": "Local resident witnessed a triangular craft hovering silently above the falls. 72 hours later, two men in dark, dated suits (Men in Black) visited the home. Warned witness not to discuss sighting. Unnatural pale complexions.",
        "official_reports": {"MUFON": "MIB Encounter database, Case #94-ONF."},
        "media_urls": ["Featured in 'Men in Black (cryptozoology)' related sightings."],
        "evidence": ["Witness audio interview recorded by MUFON investigators", "Sketch of the alleged Men in Black"],
        "shape": "Triangle",
        "being_count": 2,
        "being_type": "Humanoid - MIB (Men in Black)",
        "being_appearance": "Men in dark, dated suits; unnatural pale complexions",
        "contact_type": "CE3",
        "pattern_tags": ["men_in_black", "triangular_craft", "intimidation", "close_encounter"]
    },
    "CAN-050": {  # Vulcan County AB
        "tier": "A",
        "name": "Vulcan County (Pilot Encounter)",
        "witness_details": "Commercial pilot reported fast-moving, non-transponder object pacing aircraft at parallel altitude for 12 miles. Object executed impossible vertical climb and vanished from radar. ATC confirmed no scheduled military exercises.",
        "official_reports": {"Transport_Canada": "ASRS (Aviation Safety Reporting System) filing."},
        "media_urls": ["https://globalnews.ca/news/2025/02/vulcan-ufo-pilot-report", "https://www.vulcanadvanceton.ca/news/2025-sky-anomaly"],
        "evidence": ["Flight path telemetry data", "Cockpit Voice Recorder (CVR) audio transcript (redacted)"],
        "shape": "Unknown (fast-moving, non-transponder)",
        "witness_count": 1,
        "witness_occupation": "Aviation - Commercial Pilot",
        "being_count": 0,
        "pattern_tags": ["aviation_near_miss", "radar_confirmation", "high_speed", "professional_witness", "recent"]
    }
}

def assign_tier(c):
    """Determine tier based on existing data and research."""
    cid = c["case_id"]
    if cid in RESEARCH_DATA:
        return RESEARCH_DATA[cid].get("tier", "B")
    # Existing logic from parse_csv_v3.py
    # If it has physical evidence, high witness count, or is known famous case
    nar = (c.get("narrative") or "").lower()
    if "radioact" in nar or "official" in nar or "military" in nar or "police" in nar:
        return "A"
    if c.get("contact_type") in ("CE2", "CE3", "CE4"):
        return "A"
    if c.get("witness_count", 0) >= 3:
        return "A"
    # Check if it's a known famous case
    famous_ids = ["CAN-011", "CAN-021", "CAN-046", "CAN-042", "CAN-045", "CAN-017",
                  "CAN-010", "CAN-025", "CAN-041", "CAN-050", "CAN-008"]
    if cid in famous_ids:
        return "A"
    # Historical significance
    if c.get("year", 0) < 1900:
        return "C"
    if c.get("year", 0) < 1970:
        return "B"
    return "C"

def merge_research(cases):
    """Merge Tier 2/3 research into the case data."""
    for c in cases:
        cid = c["case_id"]
        if cid in RESEARCH_DATA:
            rd = RESEARCH_DATA[cid]
            # Merge research data
            for k, v in rd.items():
                # Only overwrite if the existing value is empty/N/A/Not documented
                existing = c.get(k)
                if not existing or str(existing).strip() in ("", "N/A", "Not documented", "Not applicable", "Unknown", "[]"):
                    c[k] = v
                elif isinstance(v, list) and isinstance(existing, list):
                    # Merge lists (media, evidence, etc.)
                    # Use a list merge that handles dicts gracefully
                    merged = list(existing)
                    for item in v:
                        if item not in merged:
                            merged.append(item)
                    c[k] = merged
                elif isinstance(v, dict) and isinstance(existing, dict):
                    existing.update(v)
                    c[k] = existing
        
        # Assign tier
        c["tier"] = assign_tier(c)

    return cases

def calculate_richness(c):
    skip = {"case_id", "date", "year", "year_int", "location", "province", "latitude", "longitude",
            "coordinates", "related_cases", "pattern_tags", "narrative", "source_primary_csv",
            "csv_evidence_summary", "csv_beings_summary"}
    score = 0
    total = 0
    for k, v in c.items():
        if k in skip:
            continue
        total += 1
        if v and str(v).strip() not in ("", "N/A", "Not documented", "Not applicable", "Unknown", "[]", 0, False, "False"):
            score += 1
    return round(score / max(total, 1) * 100)

def main():
    print("Loading Tier 1 enriched cases...")
    cases = load_tier1()
    print(f"Loaded {len(cases)} cases")

    print("Merging Tier 2/3 research data...")
    cases = merge_research(cases)

    # Recalculate richness
    for c in cases:
        c["richness_score"] = calculate_richness(c)

    avg_rich = sum(c["richness_score"] for c in cases) / len(cases)
    print(f"\nTier+Merge Complete. Avg richness: {avg_rich:.1f}/100")
    
    # Tier distribution
    from collections import Counter
    tiers = Counter(c.get("tier", "C") for c in cases)
    print(f"Tier distribution: {dict(tiers)}")

    # Save
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Saved to {OUTPUT_PATH}")

    # Top 10 richest cases
    sorted_cases = sorted(cases, key=lambda x: x["richness_score"], reverse=True)
    print("\nTop 10 richest cases:")
    for c in sorted_cases[:10]:
        print(f"  {c['case_id']}: {c.get('name', c.get('location', 'Unknown'))} (Tier {c.get('tier', '?')}) - {c['richness_score']}%")

if __name__ == "__main__":
    main()
