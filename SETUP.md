# DOFH — Setup & Fixes

This bundle fixes GitHub Pages navigation, publishes Seasons 1–2, and adds a
nightly auto-release for Season 3. Copy the files into your repo **keeping the
same paths**, then do the two GitHub settings below.

## 1. Files in this bundle

New:
- `docs/_layouts/episode.html` — the layout your episodes asked for but didn't exist.
- `docs/_episodes/001…010.md` — Seasons 1 & 2, ready to publish.
- `.github/workflows/release-episodes.yml` — nightly release at 9 PM IST.
- `scripts/publish_next_episode.py` + `scripts/dofh_lib.py` — the publisher.

Replace your existing copies:
- `docs/_config.yml` — now declares the `episodes` collection (the main fix).
- `docs/_includes/nav.html`, `docs/index.md`, `docs/episodes.md` — links now
  generate automatically from the collection.

Your `episodes/`, `drafts/`, and `lore/` folders are unchanged — keep them.

## 2. Why navigation was broken

Three things, now fixed:
1. `_config.yml` never declared a `collections: episodes:` block, so Jekyll
   ignored the whole `_episodes` folder and built none of those pages.
2. Episode 001 used `layout: episode`, but `_layouts/` was empty.
3. `episodes.md` listed episodes as plain text, not links.

## 3. Two GitHub settings you must set

**A. Pages source** — Settings → Pages → Build and deployment →
Source: *Deploy from a branch* → Branch: `main`, Folder: `/docs`. Save.
(Your site lives in `docs/`, so Pages must build from there.)

**B. Let the workflow push** — Settings → Actions → General →
Workflow permissions → select *Read and write permissions*. Save.
Without this the nightly job can't commit the new episode.

## 4. Go live

Commit and push everything to `main`. Pages rebuilds in a minute or two, and
Seasons 1–2 (001–010) will be browsable with working navigation.

## 5. The nightly release

The workflow runs every day at **15:30 UTC = 21:00 IST** and publishes the next
unreleased Season 3 episode (011 tonight, 012 tomorrow, …). Each run writes one
file into `docs/_episodes/` and commits it; Pages then rebuilds and the Home /
Episodes pages update themselves.

- **Test it now without waiting:** Actions tab → *Release nightly episode* →
  *Run workflow*. It should publish 011 immediately.
- **Timing:** GitHub's scheduler can drift several minutes past 21:00 at busy
  times — normal, not a bug. For an exact-time drop, use *Run workflow* manually.

## 6. Important: Season 3 isn't fully written

Only **011 (The Announcement)** and **012 (The Vendor)** have content. Drafts
**013–020 are empty files.** The workflow safely skips empty drafts and waits,
so nothing blank goes live — but episodes won't appear on those nights until you
write them. Use 011 as the format template: keep the `# DOFH #0NN` and
`## Title` headings; the publisher reads the number and title from those lines.
No front matter needed in the draft — the publisher adds it.
