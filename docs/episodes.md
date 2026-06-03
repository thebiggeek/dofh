---
layout: default
title: Episodes
---

{% include nav.html %}

# Episodes

{%- comment -%}
  Everything below is generated from the `episodes` collection.
  When the nightly workflow publishes a new file into docs/_episodes/,
  it appears here automatically. No manual editing required.
{%- endcomment -%}

{% assign ordered = site.episodes | sort: "number" %}

{% assign seasons = ordered | map: "season" | uniq | sort %}
{% for s in seasons %}
## Season {{ s }}{% assign first_in_season = ordered | where: "season", s | first %} — {{ first_in_season.season_title }}

{% assign season_eps = ordered | where: "season", s %}
{% for ep in season_eps %}
- [{{ ep.number | prepend: "00" | slice: -3, 3 }} {{ ep.title }}]({{ ep.url | relative_url }})
{%- endfor %}

---
{% endfor %}

{% if ordered.size == 0 %}
_No episodes published yet. Check back soon._
{% endif %}

New episodes are released daily at 9:00 PM IST.
