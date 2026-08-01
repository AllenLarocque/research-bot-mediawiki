#!/usr/bin/env python3
"""Publish a NEW entity page + its claim ledger, then verify.

spec: {title, wikitext, ledger: [[claim, quote, source, tier, confidence], ...],
       unsourced: [claim,...], unknown: [claim,...]}
Every quote is checked verbatim against the cached source first; refuses otherwise.
"""
import sys, os, json

from research_mediawiki import wiki, verify
from research_core import paths
from research_core.srccache import load_manifest, verify_quote


def main():
    spec = json.load(open(sys.argv[1]))
    title, wt = spec["title"], spec["wikitext"]
    wiki.ensure_login()
    all_src = set(wiki.list_category("Category:Sources"))

    bad = []
    for row in spec["ledger"]:
        claim, quote, src = row[0], row[1], row[2]
        if src not in all_src:
            bad.append("no such Source page: " + src)
        elif not verify_quote(quote, src):
            bad.append("quote NOT verbatim in %s: %.70s..." % (src, quote))
    if bad:
        print("REFUSED:")
        for b in bad:
            print("   -", b)
        sys.exit(1)

    man = load_manifest()
    rows = ["| id | claim | quote | source page | url | tier | status | confidence |",
            "|----|-------|-------|-------------|-----|------|--------|------------|"]
    i = 0
    for row in spec["ledger"]:
        i += 1
        claim, quote, src = row[0], row[1], row[2]
        tier = row[3] if len(row) > 3 else "T2"
        conf = row[4] if len(row) > 4 else "high"
        url = man.get(src, {}).get("url", "")
        rows.append("| %d | %s | \"%s\" | %s | %s | %s | sourced | %s |"
                    % (i, claim.replace("|", "/"), quote.replace("|", "/"), src, url, tier, conf))
    for c in spec.get("unsourced", []):
        i += 1
        rows.append("| %d | %s | — | — | — | — | unsourced | — |" % (i, c.replace("|", "/")))
    for c in spec.get("unknown", []):
        i += 1
        rows.append("| %d | %s | — | — | — | — | unknown | — |" % (i, c.replace("|", "/")))

    d = os.path.join(paths.DOSSIERS, title.replace(" ", "_"))
    os.makedirs(d, exist_ok=True)
    led = os.path.join(d, "sources.md")
    open(led, "w").write("# Claim ledger — %s\n\nDrafted 2026-07-27. Every quote checked "
                         "verbatim against the cached source before publication.\n\n%s\n"
                         % (title, "\n".join(rows)))

    res = wiki.edit(title, wt, "Create entity page, cited (AI-drafted, awaiting verification)")
    print("publish:", res.get("edit", {}).get("result"), res.get("error", ""))
    # A new page cannot see its own Cargo relationship rows on first parse, and
    # purge does not fix it. Re-save identical wikitext (null edit) to populate
    # the relationships table, then purge.
    if "{{Relationship" in wt:
        wiki.edit(title, wt, "Null edit to populate Cargo relationship rows (AI-drafted)")
    wiki.purge(title)

    errs = verify.verify_entity(title, wiki.get, lambda: sorted(all_src), lambda t: open(led).read())
    if errs:
        print("VERIFY FAIL:")
        for e in errs:
            print("   -", e)
        sys.exit(1)
    errs = verify.check_render(title, wiki)
    if errs:
        print("VERIFY FAIL (render):")
        for e in errs:
            print("   -", e)
        sys.exit(1)
    r = wiki.render(title)
    print("VERIFY PASS | render clean | Sources section:", ">Sources<" in r["html"])


main()
