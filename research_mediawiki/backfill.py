#!/usr/bin/env python3
"""Backfill empty archive_url on ForestWiki Source pages from the Wayback Machine.

This is the wiki-facing half of the original backfill.py. `wayback` (query
archive.org's lookup API for the closest existing capture of a URL) moved to
research_core.webarchive unchanged apart from its User-Agent default; the
`|archive_url=` rewriting below is wikitext structure and stays here.

The original hardcoded User-Agent: ForestWiki-Researcher/1.0 for its wayback
lookups (backfill.py:27) -- a different string from mksource.py's UA, but
still project-identifying, not personal. research_core.webarchive.wayback's
own default is now the neutral DEFAULT_UA ("Research bot"), so this script
passes "ForestWiki-Researcher/1.0" explicitly on every call below, keeping
the actual bytes this script puts on the wire unchanged from before the split.

usage: backfill.py
"""
import re
import time

from research_mediawiki import wiki
from research_core.webarchive import wayback as _wayback

# The exact UA the original backfill.py sent; kept local so the request the
# adapter makes over the wire is unchanged from before the split.
UA = "ForestWiki-Researcher/1.0"


def wayback(url, tries=4):
    return _wayback(url, tries=tries, ua=UA)


def list_sources():
    out, cont = [], None
    while True:
        p = {"action": "query", "list": "categorymembers",
             "cmtitle": "Category:Sources", "cmlimit": "500"}
        if cont:
            p["cmcontinue"] = cont
        r = wiki._req(p)
        out += [m["title"] for m in r["query"]["categorymembers"]]
        cont = r.get("continue", {}).get("cmcontinue")
        if not cont:
            return out


def main():
    wiki.ensure_login()

    filled, nosnap, ratelimited, skip = [], [], [], 0
    for title in list_sources():
        wt = wiki.get(title)
        if wt is None:
            continue
        m_url = re.search(r"^\|url=(\S.*)$", wt, re.M)
        m_arc = re.search(r"^\|archive_url=(.*)$", wt, re.M)
        if not m_url or (m_arc and m_arc.group(1).strip()):
            skip += 1
            continue  # no url, or archive_url already present
        url = m_url.group(1).strip()
        snap = wayback(url)
        if snap is None:
            ratelimited.append(title); continue
        if not snap:
            nosnap.append(title); continue
        if m_arc:  # archive_url line exists but empty
            new = wt[:m_arc.start()] + "|archive_url=" + snap + wt[m_arc.end():]
        else:      # insert archive_url after the url line
            new = wt[:m_url.end()] + "\n|archive_url=" + snap + wt[m_url.end():]
        # wiki.edit raises on a failed save. Keep going for a single page's
        # failure — this batch is long and Wayback rate-limits legitimately —
        # but an auth failure is not per-page: ensure_login() inside edit()
        # raises before the first save, which aborts the run as it should.
        # Previously an unauthenticated run bucketed every page as
        # "ratelimited" and reported a tidy summary of nothing happening.
        try:
            wiki.edit(title, new, "Backfill archive_url from Wayback Machine (AI-drafted)")
            filled.append(title)
        except RuntimeError as e:
            print("EDIT FAILED %s: %s" % (title, e))
            ratelimited.append(title)
        time.sleep(1)

    print("FILLED (%d):" % len(filled))
    for t in filled: print("  +", t)
    print("NO WAYBACK SNAPSHOT (%d):" % len(nosnap))
    for t in nosnap: print("  -", t)
    print("RATE-LIMITED / RETRY LATER (%d):" % len(ratelimited))
    for t in ratelimited: print("  ?", t)
    print("already-had-archive-or-no-url skipped: %d" % skip)


if __name__ == "__main__":
    main()
