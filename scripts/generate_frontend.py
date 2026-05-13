#!/usr/bin/env python3
"""
Generate narratives.js and sync cases-full.json from cases-v5-master.json.
narratives.js: var NARRATIVES = { "CAN-001": "markdown_string...", ... };
cases-full.json: copy of master JSON for frontend ALL_CASES.
"""

import json
import re
import os
import shutil
from pathlib import Path

BASE = Path(__file__).parent.parent
JSON_PATH = BASE / "data" / "cases-v5-master.json"
MD_DIR = BASE / "data" / "cases"

with open(JSON_PATH) as fp:
    cases = json.load(fp)

# Build NARRATIVES from markdown files
narratives = {}
for case in cases:
    cid = case['case_id']
    md_file = MD_DIR / f"{cid}.md"
    
    if md_file.exists():
        content = md_file.read_text(encoding='utf-8')
        # Strip YAML frontmatter
        match = re.match(r'^---\s*\n.*?\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            body = match.group(1).strip()
        else:
            body = content.strip()
        narratives[cid] = body
        print(f"  {cid}: {len(body)} chars from .md")
    else:
        # Fallback to JSON narrative
        narrative = case.get('narrative', '')
        if narrative and str(narrative).strip() not in ("", "N/A", "Not documented"):
            narratives[cid] = str(narrative)
            print(f"  {cid}: {len(narrative)} chars from JSON (no .md file)")
        else:
            narratives[cid] = "No narrative on file."
            print(f"  {cid}: No narrative available")

# Write narratives.js (docs/narratives.js and docs/data/narratives.js)
js_content = "var NARRATIVES = {\n"
for i, (cid, text) in enumerate(narratives.items()):
    # Escape for JS string literal
    escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
    js_content += f'  "{cid}": "{escaped}"'
    if i < len(narratives) - 1:
        js_content += ","
    js_content += "\n"
js_content += "};\n"

# Write both locations
for js_path in [BASE / "docs" / "narratives.js", BASE / "docs" / "data" / "narratives.js"]:
    js_path.parent.mkdir(parents=True, exist_ok=True)
    with open(js_path, 'w', encoding='utf-8') as fp:
        fp.write(js_content)
    print(f"\nWrote {js_path} ({len(js_content)} bytes)")

# Sync cases-full.json
src = JSON_PATH
dst = BASE / "docs" / "data" / "cases-full.json"
dst.parent.mkdir(parents=True, exist_ok=True)

# Verify the JSON is valid before copying
with open(src) as fp:
    data = json.load(fp)
print(f"\nVerified {len(data)} cases in source JSON")

shutil.copy2(src, dst)
print(f"Synced to {dst}")

# Verification
print("\n=== VERIFICATION ===")
print(f"NARRATIVES entries: {len(narratives)}")
print(f"cases-full.json cases: {len(data)}")

# Count how many have rich markdown vs short text
rich_count = sum(1 for t in narratives.values() if len(t) > 800)
short_count = sum(1 for t in narratives.values() if len(t) <= 800)
print(f"Rich narratives (>800 chars): {rich_count}")
print(f"Short narratives (<=800 chars): {short_count}")
