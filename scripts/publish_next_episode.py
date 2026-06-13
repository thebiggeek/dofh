#!/usr/bin/env python3
"""
Publish the next DOFH episode.

Logic:

1. Look at already published episodes in docs/_episodes/.
2. Walk season folders in order (The last script froze at season3)
3. Within each season, find the first unpublished episode.
4. Publish it.
5. Stop after publishing one episode.

"""

import os
import re
import sys
import glob
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dofh_lib import build_episode_doc, parse_episode  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS_ROOT = os.path.join(REPO, "drafts")
EPISODES_OUT = os.path.join(REPO, "docs", "_episodes")

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

def published_numbers():
nums = set()

```
for path in glob.glob(os.path.join(EPISODES_OUT, "*.md")):
    m = re.match(r"(\d+)-", os.path.basename(path))
    if m:
        nums.add(int(m.group(1)))

return nums
```

def draft_number(path):
m = re.match(r"(\d+)-", os.path.basename(path))
return int(m.group(1)) if m else 99999

def season_dirs():
dirs = glob.glob(os.path.join(DRAFTS_ROOT, "season-*"))

```
def season_sort_key(path):
    folder = os.path.basename(path)
    m = re.match(r"season-(\d+)", folder, re.IGNORECASE)
    return int(m.group(1)) if m else 99999

return sorted(dirs, key=season_sort_key)
```

def main():
done = published_numbers()

```
for season_dir in season_dirs():

    drafts = sorted(
        glob.glob(os.path.join(season_dir, "*.md")),
        key=draft_number
    )

    unpublished = []

    for draft in drafts:
        num = draft_number(draft)

        if num not in done:
            unpublished.append(draft)

    # Entire season already published
    if not unpublished:
        continue

    # Publish first unpublished episode in this season
    draft = unpublished[0]

    raw = open(draft, encoding="utf-8").read()

    if not raw.strip():
        print(
            f"::notice::Next episode #{draft_number(draft):03d} "
            f"has no content yet ({os.path.basename(draft)}). "
            f"Nothing to publish tonight."
        )
        return 0

    try:
        parse_episode(raw)
    except ValueError as e:
        print(
            f"::warning::Draft #{draft_number(draft):03d} "
            f"is malformed: {e}. Skipping."
        )
        return 0

    today_ist = datetime.datetime.now(IST).date()

    filename, contents = build_episode_doc(
        raw,
        source_path=draft,
        publish_date=today_ist
    )

    out_path = os.path.join(EPISODES_OUT, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(contents)

    number, title = parse_episode(raw)

    gh_out = os.environ.get("GITHUB_OUTPUT")

    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write("published=true\n")
            f.write(f"number={number:03d}\n")
            f.write(f"title={title}\n")
            f.write(f"file=docs/_episodes/{filename}\n")

    print(
        f"Published DOFH #{number:03d} - "
        f"{title} -> docs/_episodes/{filename}"
    )

    return 0

print("All episodes are already published. Nothing to do.")

gh_out = os.environ.get("GITHUB_OUTPUT")

if gh_out:
    with open(gh_out, "a", encoding="utf-8") as f:
        f.write("published=false\n")

return 0
```

if **name** == "**main**":
sys.exit(main())

