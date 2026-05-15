#!/usr/bin/env python3
"""
Post-pipeline media_urls restorer.
Run AFTER generate_frontend.py to restore media_urls that the pipeline destroys.
Saves and restores from scripts/media_backup.json.
"""
import json, shutil, os, sys

HEIMDALL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(HEIMDALL, "scripts", "media_backup.json")

# Load current pipeline output
with open(os.path.join(HEIMDALL, "data", "cases-full.json")) as f:
    data = json.load(f)

case_map = {c["case_id"]: c for c in data}

# Load media backup
if os.path.exists(BACKUP):
    with open(BACKUP) as f:
        media_backup = json.load(f)
    
    restored = 0
    for case_id, entries in media_backup.items():
        if case_id in case_map:
            # Only restore if current has fewer entries
            current = case_map[case_id].get("media_urls") or []
            if len(current) < len(entries):
                case_map[case_id]["media_urls"] = entries
                restored += 1
    
    # Write updated JSON
    with open(os.path.join(HEIMDALL, "data", "cases-full.json"), "w") as f:
        json.dump(data, f, indent=2)
    
    # Sync to docs/
    shutil.copy(
        os.path.join(HEIMDALL, "data", "cases-full.json"),
        os.path.join(HEIMDALL, "docs", "data", "cases-full.json")
    )
    
    with_media = sum(1 for c in data if c.get("media_urls") and len(c["media_urls"]) > 0)
    print(f"✅ Restored media_urls for {restored} cases")
    print(f"Cases with media: {with_media}/{len(data)}")
else:
    print("⚠️ No media backup found at", BACKUP)
    print("Run with 'save' argument first to create backup")
