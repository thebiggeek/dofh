---
layout: default
title: Episodes
---

{% include nav.html %}

# Episodes

{%- comment -%}
  Generated from the `episodes` collection. New episodes published into
  docs/_episodes/ appear here automatically, with their dates.
{%- endcomment -%}

{% assign ordered = site.episodes | sort: "number" %}
{% assign seasons = ordered | map: "season" | uniq | sort %}

{% for s in seasons %}
{% assign season_eps = ordered | where: "season", s %}
{% assign first_ep = season_eps | first %}
{% assign last_ep = season_eps | last %}
## Season {{ s }} — {{ first_ep.season_title }}

{% if first_ep.date %}*Began {{ first_ep.date | date: "%-d %B %Y" }}{% if last_ep.date and last_ep.number != first_ep.number %} · latest {{ last_ep.date | date: "%-d %B %Y" }}{% endif %}*{% endif %}

{% for ep in season_eps %}
- [{{ ep.number | prepend: "00" | slice: -3, 3 }} {{ ep.title }}]({{ ep.url | relative_url }}){% if ep.date %} — {{ ep.date | date: "%-d %b %Y" }}{% endif %}
{%- endfor %}

---
{% endfor %}

{% if ordered.size == 0 %}
_No episodes published yet. Check back soon._
{% endif %}

New episodes are released daily at 9:00 PM IST.
