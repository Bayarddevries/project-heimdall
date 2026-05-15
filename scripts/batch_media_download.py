#!/usr/bin/env python3
"""Batch Wikipedia thumbnail downloader for HEIMDALL media enrichment."""
import subprocess, json, time, os, urllib.parse

# (case_id, wikipedia_title, local_name, description)
CASES = [
    ("CAN-022", "Langenburg,_Saskatchewan", "Langenburg", "Town in Saskatchewan"),
    ("CAN-035", "Diefenbunker", "Diefenbunker", "Cold War bunker, Carp ON"),
    ("CAN-029", "Nahanni_National_Park", "Nahanni", "Nahanni National Park NWT"),
    ("CAN-048", "Vancouver", "Vancouver", "Vancouver BC skyline"),
    ("CAN-053", "Sudbury", "Greater_Sudbury", "Sudbury ON"),
    ("CAN-042", "Mont_Saint-Hilaire", "Mont-Saint-Hilaire", "Mont Saint-Hilaire QC"),
    ("CAN-041", "Fort_Erie", "Fort_Erie", "Fort Erie ON"),
    ("CAN-047", "Hamilton,_Ontario", "Hamilton", "Hamilton ON"),
    ("CAN-021", "Granby,_Quebec", "Granby", "Granby QC"),
    ("CAN-017", "Prince_George,_British_Columbia", "Prince-George", "Prince George BC"),
    ("CAN-033", "Shelburne,_Nova_Scotia", "Shelburne", "Shelburne NS"),
    ("CAN-031", "Kelowna", "Kelowna", "Kelowna BC"),
    ("CAN-049", "Oshawa", "Oshawa", "Oshawa ON"),
    ("CAN-025", "Clarenville", "Clarenville", "Clarenville NL"),
    ("CAN-034", "Montreal", "Montreal-1990", "Montreal QC (1990 case)"),
    ("CAN-004", "Rivers,_Manitoba", "Rivers-MB", "Rivers MB"),
    ("CAN-023", "Carman,_Manitoba", "Carman", "Carman MB"),
    ("CAN-019", "Oromocto", "Oromocto", "Oromocto NB"),
    ("CAN-040", "Fox_Lake_(Yukon)", "Fox-Lake", "Fox Lake YT"),
    ("CAN-045", "Harbour_Mille", "Harbour-Mille", "Harbour Mille NL"),
    ("CAN-050", "Calgary", "Calgary", "Calgary AB (near Ashmount)"),
    ("CAN-052", "Hafford", "Hafford", "Hafford SK"),
    ("CAN-008", "Temagami", "Temagami", "Temagami ON (near Clan Lake)"),
    ("CAN-024", "Montreal", "Montreal-1977", "Montreal QC (1977 case)"),
    ("CAN-036", "Saint-Zotique", "Saint-Zotique", "Saint-Zotique QC"),
    ("CAN-039", "Saint-Jean-sur-Richelieu", "Saint-Jean-sur-Richelieu", "St-Jean-sur-Richelieu QC"),
    ("CAN-026", "Baskatong_Reservoir", "Baskatong", "Baskatong Reservoir QC"),
    ("CAN-038", "Port_Colborne", "Port-Colborne", "Port Colborne ON"),
    ("CAN-056", "Sheridan_Lake_(British_Columbia)", "Sheridan-Lake", "Sheridan Lake BC"),
    ("CAN-027", "Saddle_Lake,_Alberta", "Saddle-Lake", "Saddle Lake AB"),
]

HEIMDALL = "/root/project-heimdall"
os.chdir(HEIMDALL)

results = []

for case_id, wiki_title, folder_name, desc in CASES:
    # Fetch Wikipedia API for page image
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&titles={wiki_title}&prop=pageimages&format=json&pithumbsize=1200'
    r = subprocess.run(["curl", "-s", api_url], capture_output=True, text=True, timeout=15)
    
    if r.returncode != 0:
        results.append((case_id, wiki_title, "error", ""))
        time.sleep(0.3)
        continue
    
    try:
        data = json.loads(r.stdout)
    except:
        results.append((case_id, wiki_title, "json-error", ""))
        time.sleep(0.3)
        continue
    
    pages = data.get("query", {}).get("pages", {})
    img_url = None
    for pid, page in pages.items():
        if "thumbnail" in page:
            img_url = page["thumbnail"]["source"]
            # Clean URL - remove query params for actual download
            clean_url = img_url.split("?")[0].replace("/thumb/", "/").rsplit("/", 1)[0]
            # Alternative: get the actual file URL
            # The thumbnail URL pattern is: /thumb/a/b/Filename.jpg/800px-Filename.jpg
            # The original is: /a/b/Filename.jpg
            orig_url = clean_url  # already cleaned above
    
    if img_url:
        # Extract the actual image URL from the thumbnail path
        # Thumbnail: .../thumb/a/b/Filename.jpg/800px-Filename.jpg
        # Original:  .../a/b/Filename.jpg
        parts = img_url.split("/thumb/")
        if len(parts) > 1:
            # Path after /thumb/
            subpath = parts[1]
            # Remove the size prefix at the end
            path_parts = subpath.rsplit("/", 1)
            if len(path_parts) > 1:
                orig_path = path_parts[0]
                orig_url = f"https://upload.wikimedia.org/wikipedia/commons/{orig_path}"
            else:
                orig_url = img_url.split("?")[0]
        else:
            orig_url = img_url.split("?")[0]
        
        # Create directory
        img_dir = f"docs/images/{case_id}"
        os.makedirs(img_dir, exist_ok=True)
        
        # Determine extension
        ext = os.path.splitext(orig_url.split("/")[-1])[1] or ".jpg"
        local_file = f"{img_dir}/{folder_name.lower()}{ext}"
        
        # Download
        dl = subprocess.run(["curl", "-sL", "-o", local_file, orig_url], 
                          capture_output=True, text=True, timeout=30)
        
        if dl.returncode == 0 and os.path.getsize(local_file) > 1000:
            size = os.path.getsize(local_file)
            results.append((case_id, wiki_title, f"downloaded ({size//1024}KB)", orig_url))
            print(f"✅ {case_id} | {folder_name}: {size//1024}KB -> {local_file}")
        else:
            results.append((case_id, wiki_title, "dl-failed", orig_url))
            print(f"❌ {case_id} | {folder_name}: download failed")
    else:
        results.append((case_id, wiki_title, "no-image", ""))
        print(f"❌ {case_id} | {folder_name}: no image on Wikipedia")
    
    time.sleep(0.35)

print("\n\n=== SUMMARY ===")
success = sum(1 for r in results if "download" in r[2])
fail = sum(1 for r in results if r[2] not in ("downloaded",))
print(f"Downloaded: {success}/{len(results)}")
print(f"Failed: {fail}/{len(results)}")
for case_id, title, status, url in results:
    status_char = "✅" if "download" in status else "❌"
    print(f"  {status_char} {case_id} ({title}): {status}")
