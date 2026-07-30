---
name: verification
description: Use before publishing any ForestWiki page and immediately after publishing it — runs verify.py, checks corroboration, purges and re-renders to catch Cargo lag and template errors.
---

# Verification

## Before publishing

```
python3 scripts/verify.py "<Entity page title>"
```

It **must** print `VERIFY PASS`. If it fails, fix every listed item and re-run.
**Never publish a page that fails.** The checks:

- every `{{Cite}}`/`<ref>` resolves to an existing Source page;
- the page has at least one inline citation;
- a claim ledger exists at `/dossiers/<Entity>/sources.md` in the 8-column form;
- every cited Source has a ledger row;
- every `sourced` ledger row has a nonempty verbatim quote;
- every `ai-verified` relationship cites 2+ sources;
- no `unknown` ledger claim appears on-page;
- `inference` ledger rows have a `{{Inference}}` marker on-page;
- the page renders with no Cargo/Scribunto/Cite error markers;
- the page uses no template this wiki does not have;
- a page with a `{{Relationship}}` block actually **renders** a Relationships
  section, and every name in `sources=` resolves to a real Source page.

## The three silent render failures

All leave a page that looks fine to every other check:

0. **A template this wiki does not have.** Found 2026-07-28: `{{'}}` — a
   Wikipedia convenience template for a possessive apostrophe after italics —
   produced **no error marker at all**. MediaWiki rendered the literal text
   `Template:'` as a red link in the middle of a sentence. Anything written from
   Wikipedia habit (`{{'}}`, `{{nowrap}}`, `{{convert}}`) is a candidate. The
   check reads the rendered HTML for `title=Template:…redlink=1`; the name
   arrives URL-encoded, so it is unquoted before reporting.

1. **A comma in a Source title.** `sources=` is comma-delimited, so a title like
   `Wikipedia — Paldi, British Columbia` splits into two bogus names — and the
   result is that the page renders **no Relationships section at all**. Not a
   broken link: the whole section disappears. It also inflates the apparent
   source count, which can make a single-source relationship pass the
   `ai-verified` check. Fix: rename the Source page to use parentheses.
2. **A newly created page cannot see its own rows.** `purge` does not fix it,
   nor does `purge&forcelinkupdate=1`. Do a **null edit** — re-save the same
   wikitext — then re-render.

Never conclude "the relationships are fine" from the wikitext alone. Render it.

## What verify.py cannot do — do these yourself

`verify.py` is a guardrail, not a proof of correctness. It cannot check:

- **Whether a quote is real.** It checks the quote field is nonempty, not that
  the source contains those words. You must copy quotes verbatim while reading.
- **Whether every checkable fact has a row.** Not mechanically decidable. It
  checks the reverse direction (cited sources have rows). Fact-by-fact coverage
  is the `claim-ledger` discipline's job.
- **Whether two sources are genuinely independent.** It counts sources; it
  cannot judge common origin. That is `source-vetting`'s job, and it is the
  check most likely to be wrong on a page that otherwise passes.
- **Whether the claim follows from the quote.** A quote that doesn't actually
  support the claim passes mechanically. Re-read each pair before publishing.

The `unknown`-on-page check is a literal substring match, so it catches a
copy-pasted claim, not a paraphrase of one.


## The check no machine can do — does the quote SUPPORT the claim?

`verify.py` confirms a quote is verbatim in its source. It cannot confirm the quote
*supports* the sentence it is attached to. That is the largest remaining risk on this wiki,
and a real one: an audit on 2026-07-28 of all 565 citation pairs found four that verified
mechanically but did not support their claims —

- **Castlegar**'s location ("at the confluence of the Columbia and Kootenay rivers") was cited
  to a quote about the city's *rainfall*.
- **Canfor Pulp**'s creation "in February 2006" was cited to a quote about a *1999* division change.
- **Alaska Pine and Cellulose**'s operation of the Woodfibre mill was cited to a quote about
  the *1980 Doman-era* purchase — right mill, wrong company and era.
- **Weyerhaeuser**'s *1999 acquisition* of MacMillan Bloedel was cited to the terms of its
  *2005 sale* — a quote about selling, used to support buying.

Two scripts attack this from different angles. Run both.

**`python3 scripts/weakcites.py [threshold]`** flags citation pairs whose quote shares little
content vocabulary with the claim and no anchor. It catches a quote that is simply about something
else. At threshold 0.20 it flagged 63 of 565; most were defensible partial support, four were
genuinely wrong.

**`python3 scripts/anchorcheck.py [--figures]`** flags cited *sentences* that assert an anchor — a
multi-word proper noun, a year, a figure — that appears in **none** of the sentence's quotes. This
catches the more dangerous case, which weakcites cannot: a quote that is plainly on-topic, shares
most of its vocabulary, and is silent on the one thing the sentence actually asserts. That is the
shape of the TFL 44 error found on 2026-07-28 — a sentence placing the licence "within the
territories of the Tseshaht First Nation and Hupacasath First Nation", cited to a quote naming
neither Nation.

Three rules keep anchorcheck usable rather than deafening:

- anchors are checked against the **union** of every quote on the sentence, because a sentence with
  three citations is supported by all three together;
- a name counts as present if the quote carries the full string, an **acronym of its initials**
  (sources write "IWA", encyclopedia sentences write it out), or its **last substantial word** (a
  surname carries the identity);
- names appearing in the sentence's own **Source page titles** are ignored — "the ''Globe and
  Mail'' reported" is in-text attribution, not an unsourced claim.

It still cannot decide support. On this corpus it flags roughly 40% of cited sentences, and the
majority of those are fine. The output of the first full run is kept at
`/dossiers/_audits/anchorcheck-2026-07-28.md` as a standing reading queue, with the entries already
actioned listed at the top.

Do this before declaring a batch of work done. A page can pass every mechanical check and still
be citing the wrong thing.

## After publishing

1. `purge` the page, then re-render — Cargo output lags a save, so a page can
   look broken (or fine) immediately after an edit and differ once purged.
2. Confirm no error markers.
3. Confirm the **Sources** section rendered and the footnotes resolve.
4. Confirm **incoming edges knit**: open the pages named as relationship objects
   and check the inverse edge now appears there.

The dossier is the audit trail that verification bots re-check the page
against — if the ledger and the page disagree, the page is wrong until proven
otherwise.

## Expected output

**FAIL** (real run, 2026-07-27, against a page drafted before the citation model):

```
$ python3 verify.py "Kamloops pulp mill"
VERIFY FAIL: Kamloops pulp mill
  - page has no inline citations ({{Cite}}/<ref>); every checkable fact must be cited or marked {{Inference}}
  - no claim ledger rows found at /dossiers/Kamloops_pulp_mill/sources.md (expected the 8-column table: id | claim | quote | source page | url | tier | status | confidence)
exit=1
```

**FAIL** (round-trip control page with three planted faults — an orphan cite, a
single-source `ai-verified` relationship, and a `sourced` row with no quote;
real run 2026-07-27):

```
$ python3 verify.py "User:ForestWikiBot-Claude-Researcher/roundtrip"
VERIFY FAIL: User:ForestWikiBot-Claude-Researcher/roundtrip
  - cite → nonexistent Source page: 'Encyclopedia of BC — Nonexistent Ghost Source'
  - ai-verified relationship owned_by → Domtar cites 1 source(s); needs 2+ independent T1/T2
  - cited Source 'Encyclopedia of BC — Nonexistent Ghost Source' has no ledger row
  - ledger claim 'Mill employs about 320 people' is 'sourced' but has no verbatim quote
exit=1
```

Note the orphan cite produces **two** errors — the cite resolves to nothing, and
it has no ledger row. That is correct: they are different failures.

**PASS** (same page after the three fixes — the unsupported claim was deleted
rather than re-sourced, the relationship gained a second independent T2 source,
and the missing quote was filled from the snapshot; real run 2026-07-27):

```
$ python3 verify.py "User:ForestWikiBot-Claude-Researcher/roundtrip"
VERIFY PASS: User:ForestWikiBot-Claude-Researcher/roundtrip (render clean, 2 cite(s) all resolve)
exit=0
```

("2 cites" for 3 footnotes is correct — `extract_cites` returns the distinct
Source pages, and Radio NL is cited twice.)

## The check for the wiki disagreeing with itself

Every page can pass every citation check and the wiki still contradict itself: on 2026-07-28
`Catalyst Paper` said the Elk Falls mill closed in **2008** while `Elk Falls Mill`'s own infobox
said **2010**. Both pages were separately "verified". Nothing compares pages to each other.

`python3 scripts/crosscheck.py` does. Infobox dates are structured, so they are the one place two
pages can be compared mechanically: it reads `founded_date` / `commissioned_date` / `closed_date` /
`dissolved_date` from every entity page, then looks for any *other* page that names that entity in
prose near an event word and a year, and flags a mismatch.

Two suppressions keep it from being pure noise — without them the first run was 7 flags, all false:

- **an owned thing between the name and the year** ("MacMillan Bloedel's sawmill … closed in 1983")
  means the date belongs to the mill, not the company;
- **a pronoun between the name and the year** ("opened *it* in 1912", "*It* was formed in 2008",
  "*that* formed the 1980 joint venture") means the sentence has moved to a different subject.

It reports 0 across the corpus as of 2026-07-28. A self-test confirms it would still have caught the
Catalyst/Elk Falls case that prompted it — a checker that reports nothing is only reassuring if you
have shown it can report something.
