#!/usr/bin/env python3
"""MediaWiki CLI for core.scripts.anchorcheck: flag sentences that assert an
anchor none of their citations contains.

This is the wiki-facing half of anchorcheck.py. It knows how to fetch pages,
find cited sentences, and strip wikitext markup down to prose; the actual
anchor analysis (which name/year/figure is missing) lives in
core.scripts.anchorcheck and knows nothing about wikis.

usage: anchorcheck_cli.py [--figures]   (--figures also reports bare numbers)
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# wiki.py and retro.py have not been migrated into adapters/ yet (out of scope
# for this task -- it only splits anchorcheck.py). Until they are, this CLI
# depends on them being importable the way the original script did: located
# next to it on sys.path. A future task should give them a proper home under
# adapters/mediawiki/ and update this import accordingly.
import wiki
import retro

from adapters.mediawiki.citemarkup import parse_cites, strip_refs
from core.scripts.anchorcheck import missing_anchors


def sentence_text(raw):
    """The prose of a sentence: refs, templates and heading marks removed.

    Order matters: templates/headings/wikilinks/bold are stripped BEFORE
    strip_refs runs, because strip_refs collapses whitespace (including the
    newlines the heading pattern depends on) as part of removing <ref> tags.
    Stripping refs last, right before the final collapse, keeps this
    byte-identical to the original anchorcheck.py:sentence_text.
    """
    s = re.sub(r"\{\{[^{}]*\}\}", " ", raw)
    s = re.sub(r"^\s*=+.*?=+\s*$", " ", s, flags=re.M)
    s = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", s)
    s = s.replace("'''", "").replace("''", "")
    return strip_refs(s).strip()


def main():
    want_figures = "--figures" in sys.argv
    wiki.ensure_login()
    srcs = set(wiki.list_category("Category:Sources"))
    ents = [t for t in sorted(set(wiki.list_category("Category:Entities")) - srcs)
            if not t.startswith("Category:")]
    total = flagged = 0
    for t in ents:
        wt = wiki.get(t) or ""
        if "<ref>" not in wt:
            continue
        for n, a, b, raw in retro.page_sentences(wt):
            cites = parse_cites(raw)
            if not cites:
                continue
            total += 1
            sent = sentence_text(raw)
            if not sent:
                continue
            miss = missing_anchors(sent, [q for _, q in cites],
                                   [s for s, _ in cites], want_figures)
            if not miss:
                continue
            flagged += 1
            print("\n[%s]" % t)
            print("   CLAIM: %s" % sent[:200])
            for src, q in cites:
                print("   <- %-55s \"%s\"" % (src.strip()[:55],
                                              re.sub(r"\s+", " ", q)[:110]))
            print("   MISSING FROM EVERY QUOTE: %s" % ", ".join(miss[:6]))
    print("\nflagged %d of %d cited sentences" % (flagged, total))


if __name__ == "__main__":
    main()
