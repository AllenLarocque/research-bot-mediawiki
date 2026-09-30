# Wiki rules

Rules for writing to ForestWiki. The first section would hold for any
MediaWiki; the rest is this wiki's schema, versioned in the stack repo's
`wiki-content/`.

## Any MediaWiki

- The API is `$MW_API`; log in with the bot password `$MW_RESEARCH_BOT_USER@research` / `$MW_RESEARCH_BOT_APP_PASS`, take a CSRF token, then `action=edit`.
- Every edit carries `tags=ai-contributed`; never mark an edit as bot.
- A long run of edits draws `ratelimited`; sleep seventy seconds and retry.
- A title that resolves may be a redirect; cite the target.
- The search index does not reflect page content reliably; read pages, do not search them.

## Sources

- Create a Source page for every source you cite: citation, url, archive_url, publication_date with precision, source_type.
- Before creating one, search existing Source pages by URL with `srcdupe`, not by title; a document with two dates, or already named otherwise, is found twice.
- A comma in a Source page title splits a `sources=` list; do not use one.
- A redundant Source page is superseded, never deleted: say what replaced it, move its citations and ledger rows, and leave the duplication visible.
- A fetch failure is a fact about the day; it lives in the sidecar, never on a page.

## Page shape

1. `{{AI-contributed}}`
2. The entity template with sourced fields; omit unknown fields.
3. Cited prose, each load-bearing sentence wrapped as `{{Claim|…<ref>…</ref>}}`.
4. `{{Relationship}}` rows.
5. `{{Entity footer}}`
- Fetch the entity's template, `Category:Predicates` and an exemplar page before drafting; the wiki describes itself.
- Wrap one whole sentence per `{{Claim}}`, including its `<ref>`; do not wrap the lead definition or navigation.
- Rewording a claim resets its verification count and changing only its citation does not; do not reflow verified prose for style.
- When you replace an absence sentence with a section, keep the heading it sat under.
- Leave genuine red links; they recruit contributors.

## Relationship rows

- Predicate from the vocabulary, dates with `date_precision`, `sources=` naming Source pages.
- `ai-verified` needs two publishers; the Source title names the host, not the author, so read the citation field before counting.
- A row's source must say what the row says; when a row matters, open what it cites.
- Read what a row renders as, not what it was meant to say.
- Retire an `{{Inference}}` when a source states the fact; mark the ledger row retired, do not delete it.

## Page voice

- A page is written for a reader years from now who does not know how it was made: write about the subject and the sources, never about the work.
- Never name the machinery: this file, the corpus, dossiers, snapshots, rows, counts, "this wiki".
- The limits of the sources are the reader's business and the limits of your search are not: "No source found gives X" is content, "nothing read for it gives X" is not.
- A disagreement between sources is content; attribute each and move on, and never write what the page said before.
- A `note=` on a row renders; it is page surface.
- Section headings carry voice: "What the sources do not cover", not "What this page does not say".
- `voiceaudit` finds these spans; an error is never right on a page, and a warn is a question to answer.

## Done means

- The page is live, bannered, every row cited, every edit tagged, and every Source page exists.
- The dossier is complete: ledger, captures, sidecars, and a line in `_runs.md`.
- `research_mediawiki.voiceaudit_cli --page "<Entity>"` reports no error and every warn has been answered.
- `research_core.quoteaudit.audit` reports no MISSING row for the entity without a written verdict.
- You re-fetched the rendered page and saw no template error.
