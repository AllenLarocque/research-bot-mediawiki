---
name: attribution
description: Use when writing ForestWiki page prose — how to attach APA citations inline with <ref>{{Cite}}, how to mark inference with {{Inference}}, and how the Sources section is rendered.
---

# Attribution

How a sourced ledger row becomes a cited sentence on the page.

## APA lives in one place

The full **APA** citation text goes in the Source page's `citation` field, once.
See `references/apa.md` for the format per source type. Do not repeat the APA
string in the narrative — `{{Cite}}` links to the Source page.

## Citing a fact

Every `sourced` checkable fact carries an inline citation:

```wikitext
The mill produced its first pulp on 30 November 1965<ref>{{Cite|Kamloops This Week — Domtar Pulp Mill 50 Years 2015|quote=the mill produced its first pulp on November 30, 1965}}</ref>.
```

- `{{Cite|<Source page>}}` — required first parameter, the exact Source page title.
- `|p=` — optional pinpoint (page, section).
- `|quote=` — the verbatim words. Use the same quote as the ledger row.

Reuse a repeated citation with named refs:

```wikitext
first use<ref name="ktw">{{Cite|Kamloops This Week — Domtar Pulp Mill 50 Years 2015}}</ref>
later use<ref name="ktw"/>
```

## Marking inference

A claim with `status=inference` in the ledger goes on-page **only** with a
marker naming what it rests on:

```wikitext
The mill likely drew residuals from the neighbouring sawmill{{Inference|note=both were operating on adjacent sites from 1965}}.
```

This renders a visible red "[editorial synthesis: … — unverified]" and files the
page into `Category:Contains unverified inference` for human review. Never
present inference as sourced fact, and never use `{{Inference}}` to smuggle in a
guess no source supports at all.

## The Sources section

Do **not** hand-write `== Sources ==` or `<references/>`. `{{Entity footer}}`
invokes `Module:Sources`, which renders the section from the page's inline refs
— and renders nothing when the page has none. A hand-written `<references/>`
would produce the footnote list twice.

## Worked example (acceptance check)

Three sentences: two sourced facts and one inference.

```wikitext
The mill produced its first pulp on 30 November 1965<ref>{{Cite|Kamloops This Week — Domtar Pulp Mill 50 Years 2015|quote=the mill produced its first pulp on November 30, 1965}}</ref>. It passed to [[Kruger Inc.]] on 1 June 2022<ref>{{Cite|Kruger — Kamloops Pulp Mill Acquisition 2022|quote=completed the acquisition}}</ref>. The two operations likely shared a log supply{{Inference|note=adjacent sites, overlapping tenure dates}}.
```

`extract_cites()` on that wikitext returns exactly the two Source pages:

```
{'Kamloops This Week — Domtar Pulp Mill 50 Years 2015',
 'Kruger — Kamloops Pulp Mill Acquisition 2022'}
```

(Verified 2026-07-27 — the `{{Inference}}` marker correctly contributes no
citation, since it is not a source.)
