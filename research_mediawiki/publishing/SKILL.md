---
name: publishing
description: Use when creating or editing any ForestWiki page — page shape, required edit tags, Cargo lag, snapshots, archive capture, and the operational gotchas already hit on this wiki.
---

# Publishing

## Page shape (exact order)

1. `{{AI-contributed}}`
2. Entity template call with sourced field values — **omit unknown fields**
3. Narrative prose — cited, modest, no speculation
4. `{{Relationship}}` rows
5. `{{Entity footer}}` — renders Relationships, Timeline and Sources

Create a Source page (`Template:Source`) for every source cited: APA `citation`,
`url`, `archive_url`, `publication_date` + precision, `source_type`.

Leave genuine red links in the narrative — they recruit future contributors.

## Non-negotiables

- **Every edit carries `tags=ai-contributed`.** The server enforces it too.
- **Never set the bot flag.** (`wiki.edit()` deliberately does not send `bot`.)
- Relationship `sources=` is **comma-delimited**, so **Source page titles must
  not contain commas.** Use an em dash: `Publication — Topic Year`.
  **This is worse than a broken link:** a comma in a cited Source title makes the
  page render *no Relationships section at all* — the rows vanish silently and
  the page still looks fine. Found on 2026-07-27 affecting 8 pages, caused by
  Source titles like `Wikipedia — Paldi, British Columbia`. Those 11 Source pages
  were renamed to `Wikipedia — Paldi (British Columbia)`. If you must cite a
  place-name source, parenthesise the region; never comma it.
- Titles must match exactly, including the em dash and any apostrophe.

## Gotchas already hit on this wiki

- **Tolerant JSON.** MediaWiki sometimes appends trailing bytes after the JSON
  body; `json.loads` then raises "Extra data". `wiki.parse_response()` uses
  `raw_decode`. Do not replace it with `json.loads`.
- **Apostrophes in titles** break naive shell/python one-liners. Pass titles as
  arguments or via a file — never interpolate them into a quoted code string.
- **Cargo lag.** Relationship and Timeline output is Cargo-backed and lags the
  save. `purge` then re-render before trusting what you see.
- **A NEW page cannot see its own relationship rows on first parse.** After
  creating a page, `purge` — even `purge` with `forcelinkupdate=1` — is NOT
  enough: the Relationships section renders empty. You must do a **null edit**
  (re-save the identical wikitext), which repopulates Cargo. Verified
  2026-07-27 on 20 newly created pages. `verify.py` now fails a page that has a
  `{{Relationship}}` block but renders no Relationships section.
- **Login idempotency.** `ensure_login()` reuses an existing bot-password
  session; do not re-login on every call.
- **Self-transclusion in template docs.** Writing `{{Cite}}` inside a template's
  own `<noinclude>` doc transcludes it. Wrap examples in `<nowiki>`.
- **`{{#if:{{#tag:references|}}|…}}` is broken** — the `#tag` call inside the
  condition consumes the page's refs and the following `<references/>` renders
  empty. `Module:Sources` handles this; do not "simplify" the footer back.

## Provenance capture

- Save a copy of every source used to `/dossiers/<Entity>/snapshots/`.
- Capture an archive link via `https://web.archive.org/save/<URL>` and record
  both `url` and `archive_url`.
- **Verify the capture is the real page.** A saved snapshot can land on a
  bot-challenge interstitial or a paywall; recording that as `archive_url` is
  false provenance. Check the snapshot's title/content before recording it.
- If archive.org is down: save the local snapshot, leave `archive_url` empty
  with a note on the Source page, and re-run `scripts/backfill.py` later.
- If a source genuinely has no valid snapshot, say so **on the Source page**, so
  the gap is visible rather than silent.

## Acceptance check — dry-run against a live entity (2026-07-27)

Checked `Kamloops pulp mill` against this checklist:

| Item | Status |
|---|---|
| Page shape order | ✅ banner → `{{Facility}}` → narrative → 5 `{{Relationship}}` rows → `{{Entity footer}}` |
| Edits tagged `ai-contributed` | ✅ |
| Not bot-flagged | ✅ |
| Source titles comma-free | ✅ (em-dash style throughout) |
| Renders clean | ✅ no error markers; Relationships + Timeline present |
| Source pages exist for citations | ✅ |
| Snapshots saved | ✅ `/dossiers/Kamloops_pulp_mill/snapshots/` populated |
| `archive_url` captured | ✅ |
| **Inline citations** | ❌ **gap** — page predates the citation model; no `<ref>`s |
| **Claim ledger (8-column)** | ❌ **gap** — `sources.md` is the old free-form table |

So a representative existing page satisfies the operational layer but fails the
new attribution layer — which is the expected state. The ~89 pages drafted
before this skill set need a citation retrofit pass; that is tracked work, not a
silent gap.
