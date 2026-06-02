#!/usr/bin/env python3
"""
Publish the next Season 3 episode.

Run by the nightly GitHub Actions workflow. Logic:

  1. Look at which episodes are already published (files in docs/_episodes/).
  2. Walk the Season 3 drafts in order (011, 012, ... 020).
  3. Find the first one that is NOT yet published.
  4. If that draft is empty (no content written yet), stop and do nothing
     -- the schedule simply waits until you write it. Nothing broken gets
     pushed live.
  5. Otherwise, generate docs/_episodes/0XX-slug.md from the draft and exit.

The workflow handles committing/pushing only if a new file appeared.

Exit codes:
  0  = success (either published one, or nothing to do)
  >0 = unexpected error
"""

import os
import re
import sys
import glob
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dofh_lib import build_episode_doc, parse_episode  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = os.path.join(REPO, "drafts", "season-03-the-great-digital-transformation")
EPISODES_OUT = os.path.join(REPO, "docs", "_episodes")

# Optional: IST publish date stamp (so the date shown matches release night in India).
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def published_numbers():
    nums = set()
    for path in glob.glob(os.path.join(EPISODES_OUT, "*.md")):
        m = re.match(r"(\d+)-", os.path.basename(path))
        if m:
            nums.add(int(m.group(1)))
    return nums


def draft_number(path):
    m = re.match(r"(\d+)-", os.path.basename(path))
    return int(m.group(1)) if m else 99999


def main():
    done = published_numbers()
    drafts = sorted(glob.glob(os.path.join(DRAFTS, "*.md")), key=draft_number)

    for draft in drafts:
        num = draft_number(draft)
        if num in done:
            continue  # already live

        raw = open(draft, encoding="utf-8").read()
        if not raw.strip():
            print(f"::notice::Next episode #{num:03d} has no content yet "
                  f"({os.path.basename(draft)}). Nothing to publish tonight.")
            return 0

        # Sanity-check the draft parses before we publish it.
        try:
            parse_episode(raw)
        except ValueError as e:
            print(f"::warning::Draft #{num:03d} is malformed: {e}. Skipping.")
            return 0

        today_ist = datetime.datetime.now(IST).date()
        filename, contents = build_episode_doc(raw, publish_date=today_ist)
        out_path = os.path.join(EPISODES_OUT, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(contents)

        # Expose details to the workflow via GITHUB_OUTPUT (for the commit message).
        number, title = parse_episode(raw)
        gh_out = os.environ.get("GITHUB_OUTPUT")
        if gh_out:
            with open(gh_out, "a", encoding="utf-8") as f:
                f.write(f"published=true\n")
                f.write(f"number={number:03d}\n")
                f.write(f"title={title}\n")
                f.write(f"file=docs/_episodes/{filename}\n")
        print(f"Published DOFH #{number:03d} - {title} -> docs/_episodes/{filename}")
        return 0

    print("All Season 3 episodes are already published. Nothing to do.")
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write("published=false\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
