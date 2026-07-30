#!/usr/bin/env python3
"""MediaWiki CLI for core.scripts.addcite: attach an already-cached verbatim
quote to a phrase on a page, and log it.

This is the wiki-facing half of addcite.py. It knows how to log in, fetch and
edit pages, verify quotes against cached sources, and append ledger rows; the
actual anchor-insertion surgery lives in core.scripts.addcite and knows
nothing about wikis.

usage: addcite_cli.py spec.json
spec: [{page, after, source, quote, claim, tier}, ...]
      `after` is the exact page text the <ref> should follow.
"""
import sys
import os
import json
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# wiki.py, paths.py and verify.py have not been migrated into adapters/ yet
# (out of scope for this task, which only resolves retro.py per Task 8).
# Until they are, this CLI depends on them being importable the way the
# original script did: located next to it on sys.path. A future task should
# give them a proper home under adapters/mediawiki/ and update this import
# accordingly. (paths.py itself already has a core/ home as
# core.scripts.paths -- this bare shim import predates that move and is
# left alone here as out of scope; Task 8 only resolves the retro.py half.)
import wiki
import paths
import verify

from adapters.mediawiki.citemarkup import format_cite
from core.scripts.addcite import insert_after
from core.scripts.srccache import load_manifest, verify_quote


def main():
    specs = json.load(open(sys.argv[1]))
    wiki.ensure_login()
    all_src = set(wiki.list_category("Category:Sources"))
    man = load_manifest()

    bad = []
    for s in specs:
        if s["source"] not in all_src:
            bad.append("%s: no such Source page: %s" % (s["page"], s["source"]))
        elif not verify_quote(s["quote"], s["source"]):
            bad.append("%s: quote NOT verbatim in %s: %.60s..."
                       % (s["page"], s["source"], s["quote"]))
    if bad:
        print("REFUSED:")
        for b in bad:
            print("   -", b)
        sys.exit(1)

    by_page = {}
    for s in specs:
        by_page.setdefault(s["page"], []).append(s)

    for page, rows in by_page.items():
        wt = wiki.get(page)
        if wt is None:
            print("SKIP (no such page):", page)
            continue
        for s in rows:
            ref = format_cite(s["source"], s["quote"])
            try:
                wt = insert_after(wt, s["after"], ref)
            except ValueError as e:
                print("REFUSED %s: %s" % (page, e))
                sys.exit(1)
        res = wiki.edit(page, wt, "Cite claims the anchor audit found uncited (AI-drafted)")
        print("%-38s %s" % (page, res.get("edit", {}).get("result")))

        led = paths.ledger(page)
        md = open(led).read()
        last = max(int(m) for m in re.findall(r"^\|\s*(\d+)\s*\|", md, re.M))
        out = []
        for i, s in enumerate(rows, 1):
            out.append("| %d | %s | \"%s\" | %s | %s | %s | sourced | high |"
                       % (last + i, s["claim"].replace("|", "/"),
                          s["quote"].replace("|", "/"), s["source"],
                          man.get(s["source"], {}).get("url", ""), s.get("tier", "T2")))
        open(led, "w").write(md.rstrip("\n") + "\n" + "\n".join(out) + "\n")

        wiki.purge(page)
        errs = verify.verify_entity(page, wiki.get, lambda: sorted(all_src),
                                    lambda t: open(led).read())
        errs += verify.check_render(page, wiki)
        print("    verify:", errs or "PASS")
        if errs:
            sys.exit(1)


if __name__ == "__main__":
    main()
