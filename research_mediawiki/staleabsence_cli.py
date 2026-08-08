#!/usr/bin/env python3
"""MediaWiki CLI for research_core.staleabsence: find claims of absence that
have stopped being true.

A page saying "the Workers' Unity League has no page here" is asserting
something about the wiki, and nothing tells that sentence when the page is
created. Two such sentences were false by the time the 2026-08 voice cleanup
reached them, and both were noticed only because an unrelated pattern happened
to fire on the same sentence.

This is the wiki-facing half. research_core.staleabsence finds the claims and
guesses their subjects from capitalisation; the better answer is the sentence's
own link targets, which only this side can parse.

It never writes. Whether a stale sentence should be deleted, rewritten, or
turned into a plain cross-reference depends on what the sentence was for, and
that is not a substitution a script should be making.

usage:
  staleabsence_cli.py                 every entity and event page
  staleabsence_cli.py --page "Sayward"    one page (repeatable)
  staleabsence_cli.py --all-claims    list every absence claim, stale or not

exit status: 0 when no claim has expired, 1 when any has, 2 on a usage or fetch
failure.
"""
import argparse
import sys

from research_core.staleabsence import absence_claims, candidate_names, expired
from research_mediawiki import wiki
from research_mediawiki.retro import narrative_span, page_sentences, wikilinks
from research_mediawiki.voicemarkup import note_spans


def regions(title, markup):
    """The stretches of a page a sentence can sensibly be cut from.

    Narrative sentences, plus each relationship row's note= value. Raw markup
    is not prose -- a heading and a template parameter both end without a full
    stop -- so splitting the whole page on sentence punctuation produces
    "sentences" that run from one section into the next and bury the claim's
    subject among every other capitalised word between them.

    Three surfaces, because a claim was found on each:

    - narrative sentences, via page_sentences;
    - each relationship row's note= value, which renders to a reader;
    - prose BELOW the relationship rows. narrative_span ends at the first
      {{Relationship}}, so page_sentences cannot see anything after it -- and
      Robert Sommers carried "Wick Gray, David Sturdy and Judge Arthur Lord
      have no pages here" in exactly that position, invisible to the first
      draft of this probe. A page's last paragraph is still a page's prose.
    """
    out = [raw for _, _, _, raw in page_sentences(markup)]
    out += [markup[a:b] for a, b in note_spans(markup)]

    _, narrative_end = narrative_span(markup)
    for line in markup[narrative_end:].splitlines():
        line = line.strip()
        # A template call or a table row is markup, not prose. Its innards are
        # already covered by note_spans where they matter.
        if not line or line.startswith(("{{", "|", "}}", "==", "*", "#", "<")):
            continue
        out.append(line)
    return out


def claims_on(title, markup):
    """Every absence claim on one page, across all its regions."""
    return [claim for region in regions(title, markup)
            for claim in absence_claims(region)]


def names_in_sentence(title, sentence):
    """Extra subjects for a claim: the sentence's link targets.

    Never the page's own title. A page always exists, so offering it would make
    every absence claim on every page look expired -- and pages routinely link
    themselves in bold or through a redirect.
    """
    return [t for t in wikilinks(sentence) if t != title]


def choose_titles(args):
    if args.page:
        return list(args.page)
    titles = set(wiki.list_category("Category:Entities"))
    titles -= set(wiki.list_category("Category:Sources"))
    return sorted(t for t in titles if not t.startswith("Category:"))


def fetch(titles):
    pages = {}
    for t in titles:
        markup = wiki.get(t)
        if markup is None:
            print("MISSING: %s (no such page)" % t, file=sys.stderr)
        else:
            pages[t] = markup
    return pages


def wanted_names(pages):
    """Every title any absence claim might be about, across the corpus.

    Collected in one pass so existence can be asked in batches. Asking per
    claim would be hundreds of round trips to answer one question.
    """
    names = set()
    for title, markup in pages.items():
        for claim in claims_on(title, markup):
            names.update(candidate_names(claim.sentence))
            names.update(names_in_sentence(title, claim.sentence))
    return names


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--page", action="append", help="check one page (repeatable)")
    p.add_argument("--all-claims", action="store_true",
                   help="list every absence claim found, expired or not")
    args = p.parse_args(argv)

    wiki.ensure_login()
    titles = choose_titles(args)
    if not titles:
        print("ERROR: selected no pages to check", file=sys.stderr)
        return 2

    pages = fetch(titles)
    if not pages:
        print("ERROR: fetched no pages from %d titles" % len(titles), file=sys.stderr)
        return 2

    if args.all_claims:
        total = 0
        for title in sorted(pages):
            for claim in claims_on(title, pages[title]):
                total += 1
                print("%-32s %s" % (title[:32], claim.sentence[:110]))
        print("\n%d absence claim(s) in %d pages" % (total, len(pages)))
        return 0

    # expired() raises rather than returning [] when it finds no claims at all,
    # because across a whole corpus that means the phrase list has stopped
    # matching. Across ONE page it means the page makes no claim of absence,
    # which is the ordinary case and not an error -- so the guard is skipped
    # only for an explicitly named page, never for the sweep.
    if args.page and not any(claims_on(t, m) for t, m in pages.items()):
        print("no absence claim on the %d page(s) checked" % len(pages))
        return 0

    present = wiki.existing(wanted_names(pages))
    stale = expired(pages, present, extra_names=names_in_sentence,
                    sentences=regions)

    if not stale:
        print("clean: %d pages, no expired absence claim" % len(pages))
        return 0

    for title, claim, live in stale:
        print("\n=== %s" % title)
        print("  says:   %s" % claim.sentence[:160])
        print("  but:    %s now exists" % ", ".join(live))
    print("\n%d expired claim(s) across %d pages" % (len(stale), len(pages)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
