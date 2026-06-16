"""
Shared helpers for turning raw DOFH episode markdown into Jekyll collection
documents (the files that live in docs/_episodes/ and become web pages).

A raw episode file looks like:

    # DOFH #011

    ## The Announcement

    The Junior Officer entered ...

We extract the number (11) and the title ("The Announcement"), then write a
docs/_episodes/011-the-announcement.md file with YAML front matter on top and
the ORIGINAL body left intact underneath.
"""

import re
import datetime

# Which season each episode number belongs to, and the season's display title.
SEASONS = {
    1: (range(1, 6),   "The Portal"),
    2: (range(6, 11),  "Cyber Security"),
    3: (range(11, 21), "The Great Digital Transformation"),
    4: (range(21, 31), "The Reckoning"),
    5: (range(31, 41), "The Accountability"),
}


def season_for(number: int):
    for season_num, (rng, title) in SEASONS.items():
        if number in rng:
            return season_num, title
    return 0, "Unknown"


def parse_episode(raw_text: str):
    """Return (number, title) parsed from the raw episode body, or raise."""
    num_match = re.search(r"#\s*DOFH\s*#(\d+)", raw_text)
    if not num_match:
        raise ValueError("Could not find a '# DOFH #NNN' heading in the file.")
    number = int(num_match.group(1))

    # Title is the first '## ...' heading.
    title_match = re.search(r"^##\s+(.+?)\s*$", raw_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else f"Episode {number}"
    return number, title


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_episode_doc(raw_text: str, publish_date: datetime.date | None = None):
    """
    Build (filename, file_contents) for a docs/_episodes/ document.

    publish_date is stamped into front matter; defaults to today.
    """
    number, title = parse_episode(raw_text)
    season_num, season_title = season_for(number)
    if publish_date is None:
        publish_date = datetime.date.today()

    slug = slugify(title)
    filename = f"{number:03d}-{slug}.md"

    front_matter = (
        "---\n"
        "layout: episode\n"
        f'title: "{title}"\n'
        f"number: {number}\n"
        f"season: {season_num}\n"
        f'season_title: "{season_title}"\n'
        f"date: {publish_date.isoformat()}\n"
        f"permalink: /episodes/{number:03d}-{slug}/\n"
        "---\n\n"
    )

    body = raw_text.strip("\n") + "\n"
    return filename, front_matter + body
