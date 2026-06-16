---
layout: default
title: Home
---

{% include nav.html %}

---

The Digital Officer From Hell appears wherever technology,
bureaucracy, procurement and common sense collide.

---

## Latest Episode

{%- comment -%} Auto-pulls the highest-numbered published episode. {%- endcomment -%}
{% assign ordered = site.episodes | sort: "number" %}
{% assign latest = ordered | last %}
{% if latest %}
### Season {{ latest.season }} — {{ latest.season_title }}

**[#{{ latest.number }} — {{ latest.title }}]({{ latest.url | relative_url }})**

_Released {{ latest.date | date: "%B %-d, %Y" }}_

[Browse all episodes &raquo;]({{ '/episodes.html' | relative_url }})
{% else %}
_Episodes are on the way. New episodes release nightly at 9:00 PM IST._
{% endif %}

---

> "The transformation has been successful."
>
> — Final Report, probably

---

New episodes are released daily at 9:00 PM IST.
