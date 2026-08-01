#!/usr/bin/env python3
"""Apply a retrofit spec to one entity: insert <ref>{{Cite}}</ref> into the
narrative, write the 8-column ledger, publish, and run the verifier.

Spec (JSON):
{
  "title": "Kamloops pulp mill",
  "refs": [
     {"sent": 3, "source": "Radio NL — ...", "quote": "Opened in 1965, ...",
      "claim": "Mill opened 1965", "tier": "T2", "confidence": "high"}
  ],
  "inference": [ {"sent": 2, "note": "why this is a defensible reading"} ],
  "unknown":   [ "claim we could not source" ],
  "relationship_fixes": [ {"object": "Domtar", "verification": "unverified"} ]
}

Every quote is checked verbatim against the cached source BEFORE anything is
written. A spec with an unverifiable quote is refused.

usage: apply.py spec.json [--dry]
"""
import sys
import os, os, re, json

from research_mediawiki import wiki, verify
from research_mediawiki.retro import page_sentences, plain
from research_core import paths
from research_core.srccache import load_manifest, verify_quote
from research_mediawiki.profileload import PROFILE

DRY = "--dry" in sys.argv


def esc(s):
    return s.replace("|", "&#124;").replace("=", "&#61;") if False else s.replace("|", "&#124;")


def main():
    spec = json.load(open(sys.argv[1]))
    title = spec["title"]
    wiki.ensure_login()
    wt = wiki.get(title)
    if wt is None:
        print("MISSING PAGE:", title); sys.exit(1)
    if "<ref" in wt:
        print("ALREADY RETROFITTED (page has <ref>):", title); sys.exit(0)

    # ---- 1. verify every quote verbatim, and that every Source page exists
    all_src = set(wiki.list_category("Category:Sources"))
    bad = []
    for r in spec.get("refs", []):
        if r["source"] not in all_src:
            bad.append("no such Source page: %s" % r["source"])
        elif not verify_quote(r["quote"], r["source"]):
            bad.append("quote NOT verbatim in %s: %.70s..." % (r["source"], r["quote"]))
    if bad:
        print("REFUSED — quote/source problems:")
        for b in bad:
            print("   -", b)
        sys.exit(1)

    # ---- 1b. literal replacements (applied BEFORE sentence indexing).
    # Use for excising an unsourced clause or attaching an {{Inference}} marker
    # mid-sentence. Must not add/remove sentence boundaries.
    for rep in spec.get("replacements", []):
        if rep["find"] not in wt:
            print("REFUSED — replacement text not found: %.60s" % rep["find"]); sys.exit(1)
        wt = wt.replace(rep["find"], rep["replace"], 1)

    # ---- 2. insert refs (right-to-left so offsets stay valid)
    sents = {n: (a, b, raw) for n, a, b, raw in page_sentences(wt, PROFILE)}
    inserts = []
    for r in spec.get("refs", []):
        n = r["sent"]
        if n not in sents:
            print("REFUSED — no sentence #%d on the page" % n); sys.exit(1)
        cite = "<ref>{{Cite|%s|quote=%s}}</ref>" % (r["source"], esc(r["quote"]))
        inserts.append((sents[n][1], cite, n))
    for inf in spec.get("inference", []):
        n = inf["sent"]
        if n not in sents:
            print("REFUSED — no sentence #%d on the page" % n); sys.exit(1)
        inserts.append((sents[n][1], "{{Inference|note=%s}}" % esc(inf["note"]), n))
    for n in spec.get("unsourced", []):
        if n not in sents:
            print("REFUSED — no sentence #%d on the page" % n); sys.exit(1)
        inserts.append((sents[n][1], "{{Unsourced}}", n))

    # Group by position FIRST. Two inserts at the same offset must be
    # concatenated and written once: inserting them one after another makes the
    # second land inside the first, producing <<ref>A</ref>ref>B</ref>.
    bypos = {}
    for pos, text, n in inserts:
        bypos.setdefault(pos, []).append(text)

    new = wt
    for pos in sorted(bypos, reverse=True):
        text = "".join(bypos[pos])
        j = pos
        while j > 0 and new[j - 1] in " \n":
            j -= 1
        if j > 0 and new[j - 1] in ".!?":
            j -= 1
        new = new[:j] + text + new[j:]

    # ---- 3. relationship verification fixes
    for fix in spec.get("relationship_fixes", []):
        pat = re.compile(r"(\{\{Relationship\b[^}]*?\|object=%s\b[^}]*?\|verification=)([a-z-]+)"
                         % re.escape(fix["object"]), re.S)
        new, k = pat.subn(lambda m: m.group(1) + fix["verification"], new)
        if not k:
            print("WARNING: no relationship row matched object=%s" % fix["object"])

    # ---- 4. ledger
    rows = ["| id | claim | quote | source page | url | tier | status | confidence |",
            "|----|-------|-------|-------------|-----|------|--------|------------|"]
    man = load_manifest()
    i = 0
    for r in spec.get("refs", []):
        i += 1
        url = man.get(r["source"], {}).get("url", "")
        rows.append("| %d | %s | \"%s\" | %s | %s | %s | sourced | %s |" % (
            i, r.get("claim", plain(sents[r["sent"]][2]))[:120].replace("|", "/"),
            r["quote"].replace("|", "/"), r["source"], url,
            r.get("tier", "T2"), r.get("confidence", "medium")))
    for inf in spec.get("inference", []):
        i += 1
        rows.append("| %d | %s | — | — | — | — | inference | low |"
                    % (i, inf.get("claim", inf["note"])[:120].replace("|", "/")))
    for n in spec.get("unsourced", []):
        i += 1
        rows.append("| %d | %s | — | — | — | — | unsourced | — |"
                    % (i, plain(sents[n][2])[:120].replace("|", "/")))
    for u in spec.get("unknown", []):
        i += 1
        rows.append("| %d | %s | — | — | — | — | unknown | — |" % (i, u.replace("|", "/")))

    dossier = os.path.join(paths.DOSSIERS, title.replace(" ", "_"))
    os.makedirs(dossier, exist_ok=True)
    led = os.path.join(dossier, "sources.md")
    old = open(led).read() if os.path.isfile(led) else ""
    old_body = old.split("## Superseded original dossier")[0]
    ledger_md = ("# Claim ledger — %s\n\n"
                 "Retrofitted %s. Every quote below was checked verbatim against the\n"
                 "cached source text before publication.\n\n%s\n\n"
                 "## Superseded original dossier\n\n%s\n"
                 % (title, "2026-07-27", "\n".join(rows), old_body))

    if DRY:
        print("--- WIKITEXT (dry run) ---"); print(new)
        print("--- LEDGER (dry run) ---"); print("\n".join(rows))
        return

    open(led, "w").write(ledger_md)
    res = wiki.edit(title, new, "Retrofit inline citations (APA Source pages) + claim ledger (AI-drafted)")
    print("publish:", res.get("edit", {}).get("result"), res.get("error", ""))
    wiki.purge(title)

    errs = verify.verify_entity(title, wiki.get,
                                lambda: sorted(all_src),
                                lambda t: open(led).read())
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
