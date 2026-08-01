# forestwiki-research (MediaWiki adapter)

A modular skill set that makes ForestWiki drafting produce credible,
fully-attributed, hallucination-resistant entity pages.

This is the MediaWiki-facing half of the `forestwiki-research-bot` repo. The
wiki-agnostic logic (text utilities, ledger schema, source cache, path
resolution) lives in `research_core/`; this directory holds everything that
actually knows what a wiki is (the API client, wikitext parsing,
`{{Cite}}`/`{{Inference}}` handling, CLI entry points) plus the
BC-forestry-agnostic-but-project-specific docs below.

```
research_core/               wiki-agnostic: text utils, ledger, source cache, paths
  SKILL.md                   router: pipeline, self-critique gate, definition of done
  source-vetting/SKILL.md    credibility tiers (T1–T4) + the independence test
  claim-ledger/SKILL.md      8-column ledger schema + gate C
  references/apa.md          APA formats per source type
  textutil.py, srccache.py, paths.py, ledger.py, addcite.py, ...  (stdlib only)

research_mediawiki/          this directory: wiki-facing code + docs
  README.md                  this file
  attribution/SKILL.md       APA + {{Cite}} + {{Inference}} + Sources section
  verification/SKILL.md      the verifier, its limits, post-publish checks
  publishing/SKILL.md        page shape, tags, Cargo lag, snapshots, gotchas

  wiki.py                    MediaWiki API client (stdlib only)
  retro.py                   wikitext structure: narrative span, sentence spans, sources used

  --- publishing ---
  mksource.py                create a Source page: fetch, snapshot, archive, publish, cache
  newpage.py                 publish a NEW entity page + ledger, then verify
  apply.py                   retrofit citations onto an EXISTING page
  addcite_cli.py             attach one already-cached quote to a phrase, and log it

  --- checking ---
  verify.py                  pre-publish verifier + CLI (also check_render for publishers)
  weakcites_cli.py           quote/claim vocabulary overlap
  anchorcheck_cli.py         sentences asserting an anchor no quote carries
  crosscheck_cli.py          pages that date the same entity differently from each other
  backfill.py                archive_url backfill from the Wayback Machine

profiles/bc_forestry/        BC-forestry vocabulary (owned-things list, etc.)
tests/                       one test_*.py per module; tests/run_all.py runs all of them
docs/                        design docs, historical plans
```

## Install

Copy the whole `forestwiki-research-bot` checkout's `research_core/`,
`research_mediawiki/` and `profiles/bc_forestry/` into the skills directory so
the router and sub-skills are invocable, or point your harness at this repo
directly:

```bash
cp -r research_core research_mediawiki profiles ~/.claude/skills/forestwiki-research/
```

The router triggers on "research / draft / publish a ForestWiki entity"; it then
calls the sub-skills in pipeline order. The one-line pointer in the ForestWiki
`CLAUDE.md` (see below) guarantees it is reached even in a container where the
skills directory is not preloaded.

## Running the scripts

They target the ForestWiki research container and use **Python 3 stdlib only**
(no `requests` — the container has none, and PEP 668 blocks pip installs).
Run them from the repo root so `research_core.*` / `research_mediawiki.*`
imports resolve.

Environment:

| Variable | Purpose |
|---|---|
| `MW_API` | MediaWiki API endpoint, e.g. `http://mediawiki/api.php` |
| `MW_RESEARCH_BOT_USER` | bot account name (`@research` suffix is added) |
| `MW_RESEARCH_BOT_APP_PASS` | bot application password |
| `MW_COOKIE_JAR` | optional; session cookie path (default `~/.forestwiki_cookies.txt`) |

```bash
python3 -m research_mediawiki.verify "Kamloops pulp mill"   # pre-publish gate; exit 0 = PASS
python3 research_mediawiki/backfill.py                      # fill empty archive_url from Wayback
python3 research_mediawiki/wiki.py render "MacMillan Bloedel"
```

Tests (no network, no credentials needed):

```bash
python3 tests/run_all.py
```

## The ledger lives in the dossier

The verifier reads the claim ledger from `/dossiers/<Entity_Name>/sources.md`
(spaces in the title become underscores). That file — an 8-column table of
`id | claim | quote | source page | url | tier | status | confidence` — is what
makes each on-page fact traceable, and what verification bots re-check against.

## Wiki-side dependencies

This skill set assumes these exist on the wiki (all created 2026-07-27; wikitext
kept in `/dossiers/_skillset/wiki-side/`):

- `Template:Cite` — inline citation, links the Source page
- `Template:Inference` — visible "editorial synthesis — unverified" marker
- `Module:Sources` — renders the Sources section from inline refs
- `Template:Entity footer` — invokes `Module:Sources`
- `Template:Source` — `citation` field documented as APA

## Known state

The ~89 entity pages drafted before this skill set have no inline citations and
no 8-column ledger, so they **fail verification by design**. Retrofitting them is
separate, tracked work (see `research_core/SKILL.md`'s retrofit-backlog note).

## Configuration

The scripts need a wiki and two directories. All of it comes from the environment;
nothing is hardcoded to the container this was written in.

| Variable | Meaning |
|---|---|
| `MW_API` | MediaWiki `api.php` endpoint |
| `MW_RESEARCH_BOT_USER` | bot account name (used as `<user>@research`) |
| `MW_RESEARCH_BOT_APP_PASS` | bot password |
| `MW_COOKIE_JAR` | cookie jar path for the login session |
| `RESEARCH_DOSSIERS` | dossier root holding `<Entity>/sources.md` (default `/dossiers`) |
| `RESEARCH_SCRATCH` | working directory (default `/tmp/research`) |
| `RESEARCH_SRC_CACHE` | cached source text; defaults to `<RESEARCH_SCRATCH>/srccache` |

The `FORESTWIKI_*` names (`FORESTWIKI_DOSSIERS`, `FORESTWIKI_SCRATCH`,
`FORESTWIKI_SRC_CACHE`) are honoured as fallbacks so a half-migrated checkout
keeps working, but `RESEARCH_*` is the current name and `/tmp/research` is the
current default — not `/tmp/forestwiki`.

`research_core/paths.py` is the single place these are resolved. It deliberately
does not create the cache directory: a missing cache should fail loudly, because
`research_core.srccache.verify_quote` silently returns "not verbatim" for every
quote when the cache is empty, and that failure mode is indistinguishable from
a genuine bad quote.

## Relationship to the ForestWiki repo (`/workspace`)

This repo is a **sibling checkout**, not a subdirectory of ForestWiki. The
ForestWiki repo's `docker-compose.yml` mounts this repo's `research/` directory
(`../forestwiki-research-bot/research:/provision:ro`) into the agent-only
research container at container start. That relative path assumes both repos
are checked out side by side, e.g.:

```
~/code/forestwiki/                  (the ForestWiki repo, at /workspace in the dev container)
~/code/forestwiki-research-bot/     (this repo)
```

If the sibling checkout is missing or misnamed, the mount source resolves to a
directory that doesn't exist and Docker silently mounts nothing there instead of
failing — the research container will start but `research/CLAUDE.md` and
`research/PILOT.md` will not be found under `/provision`. Check for a sibling
`forestwiki-research-bot` checkout first if the research container comes up
without its briefing files.

## The source cache does not travel

`RESEARCH_SRC_CACHE` (or `FORESTWIKI_SRC_CACHE`) holds the cleaned text of every
source ever fetched, and it is what `verify_quote` checks quotes against. It is
rebuildable — `mksource.py` repopulates an entry whenever a Source page is
created — but until it is rebuilt, quote verification against older sources will
fail. Either carry the cache directory along with the skill, or expect to
re-fetch.
