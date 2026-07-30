---
name: attribution
description: Use when writing ForestWiki page prose — how to attach APA citations inline with <ref>{{Cite}}, how to mark inference with {{Inference}}, and how the Sources section is rendered.
---

# Attribution

How a sourced ledger row becomes a cited sentence on the page.

## APA lives in one place

The full **APA** citation text goes in the Source page's `citation` field, once.
See `core/references/apa.md` for the format per source type (format-neutral —
it does not assume wikitext). Do not repeat the APA string in the narrative —
`{{Cite}}` links to the Source page.

**Italics in the `citation` field must be wikitext `''…''`, never markdown
`*…*`.** MediaWiki renders `*…*` literally rather than as emphasis. Forty-three
Source pages created during this project's build used asterisks, which
displayed as literal `*Title*` instead of italics — all were fixed; check any
new or touched Source page for this before publishing.

## APA conversion history (2026-07-28)

All 116 Source pages were brought to APA. The corpus previously used a house
style (`"Title". ''Publication'', date. Accessed …`); it was converted
mechanically by `scratchpad/apaconv.py`, which pattern-matches the nine shapes
that actually occurred and refuses anything it cannot parse confidently. Sixty
converted automatically; four were done by hand (a multi-author CBC piece, an
Encyclopedia.com company history, a UNBC subject guide, and a Weyerhaeuser
press release).

### Acceptance check — pre-conversion Source pages vs. APA (2026-07-27)

Superseded by the 2026-07-28 conversion above — all four have since been
reformatted. Retained as worked examples of what the house style looked like
and how each maps to APA.

| Source page | Pre-conversion `citation` (verbatim, fetched 2026-07-27) | Verdict |
|---|---|---|
| `HR A Biography of H.R. MacMillan` | `Drushka, Ken (1995). ''HR: A Biography of H.R. MacMillan''. Madeira Park, BC: Harbour Publishing. ISBN 1-55017-129-0.` | **Close, not APA.** Given name should be an initial; APA drops the place of publication. APA: `Drushka, K. (1995). ''HR: A Biography of H.R. MacMillan''. Harbour Publishing. ISBN 1-55017-129-0.` |
| `Wikipedia — Julius Bloedel` | `"Julius Bloedel". ''Wikipedia''. Accessed 18 July 2026.` | **Not APA.** APA: `Julius Bloedel. (2026). In ''Wikipedia''. Retrieved July 18, 2026, from https://en.wikipedia.org/wiki/Julius_Bloedel` |
| `SEC Form 8-K-A — Weyerhaeuser acquisition of MacMillan Bloedel` | `Weyerhaeuser Company (2000). Form 8-K/A, "Completion of acquisition of MacMillan Bloedel Limited" (event 1 November 1999). U.S. Securities and Exchange Commission, EDGAR (CIK 0000106535).` | **Close, not APA.** Needs a period after the author, the year in parentheses as its own sentence, and the form title in italics. APA: `Weyerhaeuser Company. (2000). ''Form 8-K/A: Completion of acquisition of MacMillan Bloedel Limited'' (CIK 0000106535). U.S. Securities and Exchange Commission.` |
| `Kamloops This Week — Domtar Pulp Mill 50 Years 2015` | `"Domtar celebrates pulp mill's 50 years in Kamloops". ''Kamloops This Week'', 5 December 2015.` | **Not APA.** No author credited on the piece, so the headline moves to the author slot. APA: `Domtar celebrates pulp mill's 50 years in Kamloops. (2015, December 5). ''Kamloops This Week''. https://…` |

Conclusion: the pre-conversion corpus was internally consistent but not APA;
new and touched Source pages must use APA (with wikitext italics, per above)
from now on.

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
