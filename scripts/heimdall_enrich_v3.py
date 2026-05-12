#!/usr/bin/env python3
"""
Project HEIMDALL — Local Enrichment Pipeline v3
Enriches cases-v2.json with computed fields, cross-references, and structured data.
Saves to data/cases-v3.json

No external API calls — all enrichment is local computation.
"""

import json
import os
from collections import defaultdict

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cases-v2.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cases-v3.json")

# Load base cases
with open(DATA_PATH) as f:
    cases = json.load(f)

print(f"Loaded {len(cases)} cases from cases-v2.json")
print("=" * 60)

# ── ENRICHMENT PASS 1: Cross-references between cases ──
print("\n[Pass 1] Computing cross-references and adjacent cases...")

# Group by province, decade, shape, witness type
by_province = defaultdict(list)
by_decade = defaultdict(list)
by_shape = defaultdict(list)
by_hynek = defaultdict(list)

for case in cases:
    by_province[case.get("province", "Unknown")].append(case["case_id"])
    decade = f"{(case['year_int'] // 10) * 10}s"
    by_decade[decade].append(case["case_id"])
    by_shape[case.get("shape", "Unknown")].append(case["case_id"])
    by_hynek[case.get("hynek_classification", "Unknown")].append(case["case_id"])

for case in cases:
    cid = case["case_id"]
    
    # Adjacent cases (same province, different case)
    province_cases = [c for c in by_province.get(case.get("province", ""), []) if c != cid]
    case["adjacent_same_province"] = province_cases[:5]
    
    # Decade peers
    decade = f"{(case['year_int'] // 10) * 10}s"
    decade_peers = [c for c in by_decade.get(decade, []) if c != cid]
    case["adjacent_same_decade"] = decade_peers[:5]
    
    # Shape peers
    shape_peers = [c for c in by_shape.get(case.get("shape", ""), []) if c != cid]
    case["shape_related_cases"] = shape_peers[:5]
    
    # Related cases (fill in existing field)
    all_related = list(set(
        province_cases[:2] + decade_peers[:2] + shape_peers[:1]
    ))
    if all_related:
        case["related_cases"] = all_related[:5]

print(f"Computed cross-references for all cases")

# ── ENRICHMENT PASS 2: Compute new fields from existing data ──
print("\n[Pass 2] Computing derived fields...")

for case in cases:
    # Pattern tags (compute from existing data)
    tags = []
    
    # Era tags
    if case.get("year_int", 0) < 1950:
        tags.append("pre_space_age")
    elif case.get("year_int", 0) < 1970:
        tags.append("space_race_era")
    elif case.get("year_int", 0) < 1980:
        tags.append("close_encounter_era")
    elif case.get("year_int", 0) < 2000:
        tags.append("modern_era")
    else:
        tags.append("digital_era")
    
    # Hynek category tags
    hynek = case.get("hynek_classification", "")
    if hynek == "CE1":
        tags.append("close_encounter_first_kind")
    elif hynek == "CE2":
        tags.append("close_encounter_second_kind")
    elif hynek == "CE3":
        tags.append("close_encounter_third_kind")
    elif hynek == "CE4":
        tags.append("close_encounter_fourth_kind")
    elif hynek == "NL":
        tags.append("nocturnal_light")
    elif hynek == "DD":
        tags.append("daylight_disc")
    elif hynek == "RV":
        tags.append("radar_visual")
    
    # Physical evidence tags
    if case.get("physical_evidence") and "none" not in case.get("physical_evidence", "").lower():
        tags.append("physical_trace")
    if case.get("medical_effects") and "none" not in case.get("medical_effects", "").lower():
        tags.append("medical_effects")
    if case.get("electromagnetics") and "none" not in case.get("electromagnetics", "").lower():
        tags.append("em_interference")
    
    # Official response
    source = case.get("source_primary", "").upper()
    if "RCMP" in source or "RCAF" in source or "MILITARY" in source or "NAVY" in source:
        tags.append("official_witness")
        case["has_official_witness"] = True
    else:
        case["has_official_witness"] = False
    
    if "MUFON" in source or "UFOLOGY" in source:
        tags.append("ufology_researched")
    
    # Multi-witness
    witness_count = case.get("witness_count")
    if isinstance(witness_count, int) and witness_count > 10:
        tags.append("mass_sighting")
        case["is_mass_sighting"] = True
    else:
        case["is_mass_sighting"] = False
    
    # Media available
    if case.get("media_available") and case.get("media_available").lower() not in ["none", "no", ""]:
        tags.append("media_evidence")
        case["has_media"] = True
    else:
        case["has_media"] = False
    
    # Being encounter
    if case.get("being_type") and case.get("being_type", "").upper() not in ["NONE", "N/A", ""]:
        tags.append("entity_encounter")
        case["has_entity_encounter"] = True
    else:
        case["has_entity_encounter"] = False
    
    case["pattern_tags"] = tags
    
    # Compute narrative richness score
    richness_score = 0
    for field in ["narrative", "witness_details", "physical_evidence", "being_description", 
                   "media_available", "source_primary"]:
        if case.get(field) and str(case.get(field)).strip() and str(case.get(field)) != "none":
            richness_score += 1
    case["data_richness_score"] = richness_score

print(f"Enriched all cases with pattern tags and derived fields")

# ── ENRICHMENT PASS 3: Compute statistics ──
print("\n[Pass 3] Computing aggregate statistics...")

# Province distribution
prov_counts = defaultdict(int)
for case in cases:
    prov_counts[case.get("province", "Unknown")] += 1

# Decade distribution
decade_counts = defaultdict(int)
for case in cases:
    decade = f"{(case['year_int'] // 10) * 10}s"
    decade_counts[decade] += 1

# Shape distribution
shape_counts = defaultdict(int)
for case in cases:
    shape_counts[case.get("shape", "Unknown")] += 1

# Hynek distribution
hynek_counts = defaultdict(int)
for case in cases:
    hynek_counts[case.get("hynek_classification", "Unknown")] += 1

# Tier distribution
tier_counts = defaultdict(int)
for case in cases:
    tier_counts[case.get("internal_tier", "Unknown")] += 1

stats = {
    "total_cases": len(cases),
    "provinces": dict(sorted(prov_counts.items(), key=lambda x: x[1], reverse=True)),
    "decades": dict(sorted(decade_counts.items())),
    "shapes": dict(sorted(shape_counts.items(), key=lambda x: x[1], reverse=True)),
    "hynek_classifications": dict(sorted(hynek_counts.items(), key=lambda x: x[1], reverse=True)),
    "tiers": dict(sorted(tier_counts.items(), key=lambda x: x[1], reverse=True)),
    "mass_sightings": sum(1 for c in cases if c.get("is_mass_sighting")),
    "official_witnesses": sum(1 for c in cases if c.get("has_official_witness")),
    "entity_encounters": sum(1 for c in cases if c.get("has_entity_encounter")),
    "media_evidence": sum(1 for c in cases if c.get("has_media")),
    "physical_traces": sum(1 for c in cases if c.get("data_richness_score", 0) >= 4),
}

# Save stats
stats_path = os.path.join(os.path.dirname(__file__), "..", "data", "stats.json")
with open(stats_path, "w") as f:
    json.dump(stats, f, indent=2)

print(f"  Total cases: {stats['total_cases']}")
print(f"  Provinces: {len(stats['provinces'])}")
print(f"  Decades: {len(stats['decades'])}")
print(f"  Shapes: {len(stats['shapes'])}")
print(f"  Mass sightings: {stats['mass_sightings']}")
print(f"  Official witnesses: {stats['official_witnesses']}")
print(f"  Entity encounters: {stats['entity_encounters']}")
print(f"  Media evidence: {stats['media_evidence']}")

# ── ENRICHMENT PASS 4: Generate timeline data ──
print("\n[Pass 4] Generating timeline...")

# Sort by date
timeline = sorted(cases, key=lambda c: c.get("year_int", 9999))
timeline_data = []
for case in timeline:
    timeline_data.append({
        "case_id": case["case_id"],
        "date": case.get("date", ""),
        "year": case.get("year", ""),
        "year_int": case.get("year_int", 0),
        "location": case.get("location", ""),
        "province": case.get("province", ""),
        "shape": case.get("shape", ""),
        "hynek": case.get("hynek_classification", ""),
        "tier": case.get("internal_tier", ""),
        "witness_credential": case.get("witness_credibility", ""),
        "has_media": case.get("has_media", False),
        "has_entity": case.get("has_entity_encounter", False),
        "richness_score": case.get("data_richness_score", 0),
    })

timeline_path = os.path.join(os.path.dirname(__file__), "..", "data", "timeline.json")
with open(timeline_path, "w") as f:
    json.dump(timeline_data, f, indent=2)

print(f"Generated timeline with {len(timeline_data)} entries")

# ── Save enriched cases ──
print(f"\nSaving enriched cases to {OUTPUT_PATH}...")
with open(OUTPUT_PATH, "w") as f:
    json.dump(cases, f, indent=2)

print(f"\n{'=' * 60}")
print("ENRICHMENT COMPLETE!")
print(f"Output: {OUTPUT_PATH}")
print(f"Stats: {stats_path}")
print(f"Timeline: {timeline_path}")

# Count new fields added
new_field_count = 0
for case in cases:
    new_fields = ["adjacent_same_province", "adjacent_same_decade", "shape_related_cases",
                  "related_cases", "pattern_tags", "has_official_witness", "is_mass_sighting",
                  "has_media", "has_entity_encounter", "data_richness_score"]
    for field in new_fields:
        if case.get(field) is not None:
            new_field_count += 1

print(f"New fields populated: {new_field_count} / {len(cases) * len(new_fields)}")
