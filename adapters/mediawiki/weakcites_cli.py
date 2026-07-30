#!/usr/bin/env python3
"""MediaWiki CLI for core.scripts.weakcites: flag citations whose quote looks
unlikely to support its sentence.

This is the wiki-facing half of weakcites.py. It knows how to fetch pages, find
cited sentences, and turn wikitext into plain prose; the actual overlap/anchor
scoring lives in core.scripts.weakcites and knows nothing about wikis.

usage: weakcites_cli.py [threshold]   (threshold overrides the default 0.20,
                                        e.g. `weakcites_cli.py 0.15`)
"""
import sys
import re

from adapters.mediawiki import wiki
from adapters.mediawiki.citemarkup import parse_cites
from adapters.mediawiki.retro import page_sentences, plain
from core.scripts.weakcites import overlap, is_weak, DEFAULT_THRESH
from core.scripts.textutil import words


def main():
    # Same argv convention as the original module-level THRESH read: an
    # optional first CLI argument that looks like a number overrides the
    # default threshold.
    thresh = (float(sys.argv[1])
              if len(sys.argv) > 1 and sys.argv[1][0].isdigit()
              else DEFAULT_THRESH)

    wiki.ensure_login()
    srcs = set(wiki.list_category("Category:Sources"))
    ents = [t for t in sorted(set(wiki.list_category("Category:Entities")) - srcs)
            if not t.startswith("Category:")]
    flagged = 0
    total = 0
    for t in ents:
        wt = wiki.get(t) or ""
        if "<ref>" not in wt:
            continue
        for n, a, b, raw in page_sentences(wt):
            cites = parse_cites(raw)
            if not cites:
                continue
            sent = plain(raw)
            sw = set(words(sent))
            if not sw:
                continue
            for src, q in cites:
                total += 1
                ov = overlap(sent, q)
                if is_weak(sent, q, thresh):
                    flagged += 1
                    print("\n[%s] overlap=%.2f" % (t, ov))
                    print("   CLAIM: %s" % sent[:180])
                    print("   QUOTE: %s" % re.sub(r"\s+", " ", q)[:180])
                    print("   SRC:   %s" % src.strip()[:60])
    print("\nflagged %d of %d citation pairs (threshold %.2f)" % (flagged, total, thresh))


if __name__ == "__main__":
    main()
