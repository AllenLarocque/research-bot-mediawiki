#!/usr/bin/env python3
"""MediaWiki CLI for core.scripts.crosscheck: flag pages that date another
entity's founding or closing differently from that entity's own page.

This is the wiki-facing half of crosscheck.py. It knows how to fetch pages,
read structured founding/closing dates out of an entity's template call, and
turn wikitext into plain prose; the actual conflict logic (which year, which
suppression rule) lives in core.scripts.crosscheck and knows nothing about
wikis. The BC-forestry "owned things" vocabulary is domain knowledge, not
wiki knowledge -- it comes from profiles.bc_forestry and is passed down as a
parameter, the same way core.scripts.crosscheck receives it.

usage: crosscheck_cli.py [--window N]
"""
import sys
import re

from adapters.mediawiki import wiki
from adapters.mediawiki.citemarkup import remove_paired_refs
from core.scripts.crosscheck import date_conflicts, OPEN_FIELDS, CLOSE_FIELDS
from profiles.bc_forestry.vocabulary import OWNED_THINGS


def infobox_years(wt):
    """{field: year} from the entity template call."""
    out = {}
    for f in OPEN_FIELDS + CLOSE_FIELDS:
        m = re.search(r"\|%s=(\d{4})" % f, wt)
        if m:
            out[f] = m.group(1)
    return out


def prose(wt):
    """Page text with refs, templates and link syntax stripped.

    Matches the original crosscheck.py:50-55 exactly: only PAIRED <ref>...</ref>
    tags are removed here, not self-closing ones. That distinction matters
    because the self-closing pattern also matches <references/>, which real
    wiki pages carry -- removing it would strip text the original preserved.
    """
    s = remove_paired_refs(wt)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    s = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", s)
    return re.sub(r"\s+", " ", s)


def main():
    window = 90
    for i, a in enumerate(sys.argv):
        if a == "--window":
            window = int(sys.argv[i + 1])
    wiki.ensure_login()
    srcs = set(wiki.list_category("Category:Sources"))
    ents = [t for t in sorted(set(wiki.list_category("Category:Entities")) - srcs)
            if not t.startswith("Category:")]
    raw = {t: (wiki.get(t) or "") for t in ents}
    years = {t: infobox_years(raw[t]) for t in ents}
    text = {t: prose(raw[t]) for t in ents}

    flagged = 0
    for host in ents:
        body = text[host]
        for subject in ents:
            if subject == host or not years[subject]:
                continue
            for c in date_conflicts(subject, body, years[subject], OWNED_THINGS, window):
                flagged += 1
                print("\n[%s] says %s %s in %s" % (host, subject, c["kind"], c["year"]))
                print("   but [%s]'s own infobox says %s" % (subject, ", ".join(c["own"])))
                print("   context: …%s…" % c["context"])
    print("\nflagged %d cross-page date disagreements" % flagged)


if __name__ == "__main__":
    main()
