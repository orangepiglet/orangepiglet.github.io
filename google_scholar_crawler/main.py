from scholarly import scholarly
import json
from datetime import datetime
import os
import sys
import time


def log(message):
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}",
        flush=True
    )


log("Crawler started.")

scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")

if not scholar_id:
    log("ERROR: GOOGLE_SCHOLAR_ID is not set.")
    sys.exit(1)

log(f"Google Scholar ID loaded: {scholar_id}")

# Step 1: Search author
log("Step 1: Calling scholarly.search_author_id()...")
start = time.time()

author: dict = scholarly.search_author_id(scholar_id)

log(
    f"Step 1 completed in {time.time() - start:.2f} seconds."
)

# Step 2: Fill author information
log("Step 2: Calling scholarly.fill()...")
start = time.time()

scholarly.fill(
    author,
    sections=['basics', 'indices', 'counts', 'publications']
)

log(
    f"Step 2 completed in {time.time() - start:.2f} seconds."
)

# Step 3: Process data
log("Step 3: Processing author data...")

name = author['name']
author['updated'] = str(datetime.now())

author['publications'] = {
    v['author_pub_id']: v
    for v in author['publications']
}

log(
    f"Author: {name}, "
    f"Citations: {author.get('citedby')}, "
    f"Publications: {len(author['publications'])}"
)

# Step 4: Create results directory
log("Step 4: Creating results directory...")

os.makedirs('results', exist_ok=True)

# Step 5: Save full Google Scholar data
log("Step 5: Writing gs_data.json...")

with open('results/gs_data.json', 'w') as outfile:
    json.dump(
        author,
        outfile,
        ensure_ascii=False
    )

# Step 6: Save Shields.io data
log("Step 6: Writing gs_data_shieldsio.json...")

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}

with open('results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(
        shieldio_data,
        outfile,
        ensure_ascii=False
    )

log("Crawler completed successfully.")
