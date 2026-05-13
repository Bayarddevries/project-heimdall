#!/usr/bin/env python3
"""
Regenerate 56 markdown case files from cases-v5-master.json.
Format matches existing CAN-012.md (classified aesthetic).
"""

import json
import os
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "data" / "cases-v5-master.json"
MD_DIR = Path(__file__).parent.parent / "data" / "cases"

# Ensure directory exists
MD_DIR.mkdir(parents=True, exist_ok=True)

# Clean old files
for f in MD_DIR.iterdir():
    if f.suffix == '.md':
        f.unlink()

with open(JSON_PATH) as fp:
    cases = json.load(fp)

def build_markdown(case):
    """Generate markdown content for a case file."""
    cid = case['case_id']
    name = case.get('case_name', case['location_full'] or case['witnesses'])
    date_str = case.get('date', str(case.get('year', 'Unknown')))
    location = case.get('location_full', f"{case.get('case_name', '')}, {case.get('province', '')}")
    coords = f"{case.get('latitude', 0)}, {case.get('longitude', 0)}"
    shape = case.get('shape', 'Unknown')
    contact = case.get('contact_type', 'N/A')
    hynek = case.get('hynek_classification', 'N/A')
    witness_count = case.get('witness_count', 0)
    witness_text = case.get('witnesses', 'Not documented')
    evidence = case.get('physical_evidence', [])
    narrative = case.get('narrative', 'No narrative available.')
    pattern_tags = case.get('pattern_tags', [])
    related = case.get('related_cases', [])
    media = case.get('media_urls', [])
    official = case.get('official_reports', [])
    tier = case.get('internal_tier', 'C')
    credibility = case.get('witness_credibility', 'Low')
    
    # Format date from narrative first line if possible
    title = f"{name} — {date_str}"
    
    # --- FRONTMATTER --- (avoid em-dashes in YAML)
    fm = f"""---
case_id: {cid}
title: "{title}"
date: {date_str}
location: {location}
coordinates: {coords}
encounter_type: {hynek}
shape: {shape}
witness_count: {witness_count}
contact_type: {contact}
physical_evidence: {evidence[0] if evidence else "None reported"}
sources:
  - {case.get('source_primary', 'Not documented')}
classification:
  hynek: {hynek}
  credibility: {credibility}
  tier: {tier}
status: COMPLETE
---

"""
    # --- BODY ---
    body = f"""# {cid}: {name}
**Date:** {date_str}
**Location:** {location} ({coords})
**Classification:** {hynek}

## Case Summary

{narrative}

"""
    # Witnesses section
    body += f"""## Witnesses

**Count:** {witness_count}
**Description:** {witness_text}
**Credibility:** {credibility}

"""
    if case.get('witness_primary'):
        body += f"**Primary Witness:** {case['witness_primary']}\n\n"
    if case.get('witness_occupation'):
        body += f"**Occupation:** {case['witness_occupation']}\n\n"
    
    # Physical Evidence section
    if evidence and evidence[0] not in ("None", "Unknown", "N/A", ""):
        body += "## Physical Evidence\n\n"
        for item in evidence:
            body += f"- {item}\n"
        body += "\n"
    
    # Electromagnetics / Radiation
    if case.get('electromagnetics'):
        body += f"## Electromagnetic Effects\n\n{case['electromagnetics']}\n\n"
    if case.get('radiation_detected'):
        body += f"## Radiation\n\n{case.get('radiation_details', 'Radiation detected at site.')}\n\n"
    
    # Official Reports
    if official:
        body += "## Official Reports\n\n"
        for report in official:
            body += f"- {report}\n"
        body += "\n"
    
    # Media URLs
    if media:
        body += "## Media\n\n"
        for url in media:
            body += f"- {url}\n"
        body += "\n"
    
    # Pattern Tags
    if pattern_tags:
        body += f"## Pattern Tags\n\n`{'` `'.join(pattern_tags)}`\n\n"
    
    # Related Cases
    if related:
        body += f"## Related Cases\n\n{', '.join(related)}\n\n"
    
    # Object Characteristics
    details = []
    for field, label in [
        ('shape_detail', 'Shape Detail'),
        ('size_estimate', 'Size Estimate'),
        ('speed', 'Speed'),
        ('altitude', 'Altitude'),
        ('color', 'Color'),
        ('sound', 'Sound'),
        ('duration', 'Duration'),
        ('weather_conditions', 'Weather'),
    ]:
        if case.get(field):
            details.append(f"**{label}:** {case[field]}")
    
    if details:
        body += "## Object Characteristics\n\n"
        body += "\n".join(details) + "\n\n"
    
    # Being / Entity info
    if case.get('being_type') and case['being_type'] != '':
        body += "## Entity Details\n\n"
        body += f"**Type:** {case['being_type']}\n"
        if case.get('being_appearance'):
            body += f"**Appearance:** {case['being_appearance']}\n"
        if case.get('being_count', 0) > 0:
            body += f"**Count:** {case['being_count']}\n"
        if case.get('being_behavior'):
            body += f"**Behavior:** {case['being_behavior']}\n"
        body += "\n"
    
    return fm + body


# Generate all 56 markdown files
for case in cases:
    md_path = MD_DIR / f"{case['case_id']}.md"
    content = build_markdown(case)
    with open(md_path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f"Generated {md_path.name} ({len(content)} chars)")

print(f"\nDone! Generated {len(cases)} markdown files in {MD_DIR}")
