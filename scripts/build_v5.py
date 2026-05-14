"""
build_v5.py — Rebuild dataset with 6 missing events added chronologically.
Reads original CSV, inserts 6 new rows in correct positions, generates
cases with corrected CAN-001 through CAN-056 numbering, and maps the
RESEARCH_DATA to the right case_ids.
"""
import csv, json

# ── 1. Read original CSV ──────────────────────────────────────────────
with open("/mnt/c/Users/bayar/Downloads/CANADIAN UFO SIGHTINGS.csv") as f:
    old_rows = list(csv.DictReader(f))   # 50 rows

# ── 2. New events to insert (in chronological position) ──────────────
# Each entry: (insert_after_original_index, row_dict)
# Positions refer to the original 50-row CSV (0-indexed).
NEW_ENTRIES = [
    (9, {   # After Agassiz BC (index 9), before Falcon Lake
        "Date": "1966",
        "Location": "Surrey (White Rock), BC",
        "Coordinates": "49.2, -122.8",
        "Shape": "Glowing Orbs",
        "Contact (Hynek)": "NL",
        "Beings/Witnesses": "Family",
        "Evidence/Physical Impact": "Photographs; multiple reports during 1966 PNW flap",
        "Primary Source": "Vancouver Sun Archives",
    }),
    (25, {   # After Saddle Lake AB (index 25), before Nahanni Valley
        "Date": "1979",
        "Location": "Portage la Prairie, MB",
        "Coordinates": "49.5, -98.7",
        "Shape": "Metallic Cylinder",
        "Contact (Hynek)": "DD",
        "Beings/Witnesses": "Military personnel (CFB)",
        "Evidence/Physical Impact": "Radar operators; object hovered over runway 20+ min",
        "Primary Source": "Military Radar Logs",
    }),
    (26, {   # After Nahanni Valley (index 26), before Kelowna
        "Date": "1987",
        "Location": "L'Ancienne-Lorette, QC",
        "Coordinates": "46.8, -71.4",
        "Shape": "Disc",
        "Contact (Hynek)": "CE1",
        "Beings/Witnesses": "SQ Officers (2)",
        "Evidence/Physical Impact": "Joint affidavit; official SQ incident report",
        "Primary Source": "SQ Incident Logs",
    }),
    (39, {   # After Niagara Falls (index 39), before Harbour Mille
        "Date": "Jan 5, 2008",
        "Location": "Stephenville, NL",
        "Coordinates": "48.9, -58.6",
        "Shape": "V-Formation",
        "Contact (Hynek)": "DD",
        "Beings/Witnesses": "Dozens of residents; teen boy; CFB Goose Bay radar",
        "Evidence/Physical Impact": "30+ credible reports; military radar tracks at impossible speeds; RCMP dispatch audio",
        "Primary Source": "RCMP & DND Radar Data",
    }),
    (40, {   # After Stephenville (index 40), before Harbour Mille
        "Date": "Oct 2008",
        "Location": "Valcartier, QC",
        "Coordinates": "46.9, -71.5",
        "Shape": "Triangle",
        "Contact (Hyneck)": "NL",
        "Beings/Witnesses": "Multiple witnesses near military base",
        "Evidence/Physical Impact": "Massive triangular craft; base lockdown alleged; EM interference",
        "Primary Source": "Radio-Canada; CUFON",
    }),
    (48, {   # After N. Alberta (index 48), before Sheridan Lake
        "Date": "Feb 2025",
        "Location": "Vulcan County, AB",
        "Coordinates": "50.5, -113.2",
        "Shape": "Unknown (fast non-transponder)",
        "Contact (Hynek)": "RV",
        "Beings/Witnesses": "Commercial pilot",
        "Evidence/Physical Impact": "Flight telemetry; CVR audio; ATC confirmation; no military exercises",
        "Primary Source": "ASRS / Global News",
    }),
]

# ── 3. Build new row list with insertions ─────────────────────────────
new_rows = []
insert_map = {}  # original_index -> list of new rows
for idx, row in NEW_ENTRIES:
    insert_map.setdefault(idx, []).append(row)

for i, row in enumerate(old_rows):
    new_rows.append(row)
    if i in insert_map:
        for nr in insert_map[i]:
            new_rows.append(nr)

# Verify: should be 56
assert len(new_rows) == 56, f"Expected 56 rows, got {len(new_rows)}"

# ── 4. Create case entries with correct CAN-xxx IDs ───────────────────
cases = []
for i, row in enumerate(new_rows):
    cid = f"CAN-{i+1:03d}"
    lat, lng = [float(x.strip()) for x in row["Coordinates"].split(",")]
    contact = row.get("Contact (Hynek)", "NL")
    # Fix typo in one row
    contact = row.get("Contact (Hynek)", row.get("Contact (Hyneck)", "NL"))
    
    cases.append({
        "case_id": cid,
        "date": row["Date"],
        "location": row["Location"],
        "latitude": lat,
        "longitude": lng,
        "shape": row["Shape"],
        "contact_type": contact,
        "witness_count": 0,  # will be enriched from research
        "narrative": f"UFO sighting reported in {row['Location']}.",
        "evidence": row["Evidence/Physical Impact"],
        "source": row["Primary Source"],
        "witness_details": row["Beings/Witnesses"],
    })

# ── 5. Map RESEARCH_DATA → correct case_ids ──────────────────────────
# First, build a location/year → case_id lookup for the new numbering
lookup = {}
for c in cases:
    key = (c["location"], c["date"])
    lookup[key] = c["case_id"]
    # Also by partial location match
    loc_part = c["location"].split(",")[0].strip().lower()
    lookup[loc_part] = c["case_id"]

# Research data for existing events (remapped):
RESEARCH_REMAP = {
    "Falcon Lake": {"year": "May 20, 1967"},
    "Shag Harbour": {"year": "Oct 4, 1967"},
    "Duncan": {"year": "Jan 1, 1970"},
    "Yellowknife": {"year": "1960"},
    "Niagara Falls": {"year": "2008"},
    # New events:
    "Stephenville": {"year": "Jan 5, 2008"},
    "Valcartier": {"year": "Oct 2008"},
    "Portage la Prairie": {"year": "1979"},
    "L'Ancienne-Lorette": {"year": "1987"},
    "Surrey": {"year": "1966"},
    "Vulcan County": {"year": "Feb 2025"},
}

# Print the new ID mapping
print("NEW CASE ID MAPPING:")
print("=" * 70)
for loc_info, year_info in RESEARCH_REMAP.items():
    for c in cases:
        if loc_info.lower() in c["location"].lower():
            print(f"  {loc_info:25s} → {c['case_id']}  ({c['location']}, {c['date']})")
            break

print(f"\nTotal cases: {len(cases)}")

# ── 6. Write the new CSV for archiving ───────────────────────────────
fieldnames = ["Date", "Location", "Coordinates", "Shape", "Contact (Hynek)", 
              "Beings/Witnesses", "Evidence/Physical Impact", "Primary Source"]
with open("/root/project-heimdall/data/canadian_ufo_sightings_v5.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for row in new_rows:
        # Normalize: pick the correct Contact column name
        r = dict(row)
        if "Contact (Hyneck)" in r:
            r["Contact (Hynek)"] = r.pop("Contact (Hyneck)")
        w.writerow(r)

print("\nCSV written: data/canadian_ufo_sightings_v5.csv")
print("Next step: run merge_v5.py with corrected RESEARCH_DATA keys")
