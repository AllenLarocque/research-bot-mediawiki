#!/usr/bin/env python3
"""Create a ForestWiki Source page properly: fetch, snapshot, archive, publish.

Steps, in order, refusing rather than guessing:
  1. fetch the URL and save a snapshot under /dossiers/<Entity>/snapshots/
  2. request a Wayback capture and CHECK it is the real page, not an
     interstitial/challenge (a bad capture is false provenance)
  3. publish the Source page with an APA citation
  4. add the cleaned text to the local source cache so verify_quote works

This is the wiki-facing half of the original mksource.py. `fetch` and
`clean` (generic HTTP GET + HTML-to-text) moved to research_core.webarchive
unchanged; `{{Source}}` page construction below is wikitext structure and
stays here, alongside the ForestWiki identity string that goes out over the
wire (research_core.webarchive.DEFAULT_UA is a neutral fallback for callers
that don't care -- this script always passes its own UA explicitly, so the
bytes it actually sends are unchanged from before the split).

The original imported `retro` for its source-text cache path (`retro.CACHE`,
`retro.slug`, `retro.load_manifest`); retro.py has since been split (Task 8)
into research_core.paths (CACHE), research_core.textutil (slug),
research_core.srccache (load_manifest) and the wiki-facing remainder at
research_mediawiki/retro.py (which no longer carries any of the three), so
those references are repointed to their new research_core/ homes below.

usage: mksource.py spec.json
spec: {title, url, citation, publication_date, publication_date_precision,
       source_type, description, entity, snapshot_name}
"""
import sys
import os
import json

from research_mediawiki import wiki
from research_core.webarchive import fetch, clean
from research_core.paths import CACHE, DOSSIERS
from research_core.textutil import slug
from research_core.srccache import load_manifest
import urllib.request

# Sent with every outbound request this script makes. Deliberately NOT
# research_core.webarchive.DEFAULT_UA: this is the ForestWiki-identifying UA
# the original mksource.py used, and every fetch()/urlopen() call below
# passes it explicitly so the wire behaviour is unchanged by the split.
UA = "ForestWiki Research allen.larocque@gmail.com"


def main():
    s = json.load(open(sys.argv[1]))
    title, url = s["title"], s["url"]
    wiki.ensure_login()

    print("fetching", url)
    # NOTE: the original relied on mksource.py's own fetch(ua=None) defaulting
    # to its module-level UA. research_core.webarchive.fetch(ua=None) now
    # defaults to the neutral DEFAULT_UA instead, so the fallback to UA must
    # be explicit here to keep this script's outbound requests unchanged.
    raw = fetch(s.get("fetch_url", url), ua=s.get("user_agent") or UA)
    text = clean(raw)
    print("  got %d chars of text" % len(text))
    if len(text) < 300:
        print("REFUSED — page yielded almost no text"); sys.exit(1)

    ent = s["entity"].replace(" ", "_")
    snapdir = os.path.join(DOSSIERS, ent, "snapshots")
    os.makedirs(snapdir, exist_ok=True)
    snap = os.path.join(snapdir, s["snapshot_name"])
    open(snap, "w").write(raw)
    print("  snapshot ->", snap)

    # Wayback capture, then verify it is the real page
    arc = s.get("archive_url", "")
    try:
        if arc:
            raise RuntimeError("archive_url supplied in spec; skipping save")
        req = urllib.request.Request("https://web.archive.org/save/" + url,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as r:
            final = r.geturl()
        if "/web/" in final:
            body = clean(fetch(final, ua=UA))
            probe = s.get("verify_phrase", "")
            bad = any(k in body.lower() for k in
                      ("challenge-inline", "enable javascript", "are you a robot",
                       "access denied", "just a moment"))
            if bad or (probe and probe.lower() not in body.lower()):
                print("  archive capture REJECTED (interstitial or missing content):", final)
            else:
                arc = final
                print("  archive ->", arc)
    except Exception as e:
        print("  archive attempt failed:", str(e)[:100])

    body = ["{{AI-contributed}}", "{{Source",
            "|citation=" + s["citation"],
            "|url=" + url]
    if arc:
        body.append("|archive_url=" + arc)
    body += ["|publication_date=" + s.get("publication_date", ""),
             "|publication_date_precision=" + s.get("publication_date_precision", "day"),
             "|source_type=" + s.get("source_type", "News article"),
             "}}", s.get("description", ""), ]
    if not arc:
        body.append("\nProvenance note: no valid Wayback capture was obtained for this URL "
                    "on %s; a local snapshot is held in the entity dossier."
                    % s.get("fetch_date", "27 July 2026"))
    body.append("{{Entity footer}}")

    res = wiki.edit(title, "\n".join(body), "Create Source page (AI-drafted)")
    print("publish:", res.get("edit", {}).get("result"), res.get("error", ""))

    open(os.path.join(CACHE, slug(title) + ".txt"), "w").write(text)
    man = load_manifest()
    man[title] = {"title": title, "url": url, "archive_url": arc,
                  "via": "fresh-fetch", "chars": len(text)}
    json.dump(man, open(os.path.join(CACHE, "manifest.json"), "w"), indent=1)
    print("cache updated; source ready for citation")


if __name__ == "__main__":
    main()
