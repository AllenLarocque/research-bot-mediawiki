#!/usr/bin/env python3
"""verify.py — pre-publish verifier for ForestWiki entity pages.

This is the wiki-facing half of the original verify.py. It knows how to read
{{Cite}}/<ref> citations, {{Relationship}} blocks, malformed <ref> markup and
rendered HTML for missing templates; the claim-ledger logic (a MARKDOWN table,
not wikitext) moved to research_core.ledger, which knows nothing about wikis.

Exit status: 0 = PASS, 1 = FAIL.
"""
import re
import urllib.parse

from research_core.ledger import parse_ledger, check_ledger_coverage, check_ai_verified

# --------------------------------------------------------------------------
# Wikitext / HTML parsing
# --------------------------------------------------------------------------


def extract_cites(wt):
    """Source page names cited on the page, via {{Cite|Name}} or <ref>[[Name]]."""
    s = set(re.findall(r"\{\{Cite\|([^|}]+)", wt))
    s |= set(re.findall(r"<ref>\s*\[\[([^\]|]+)", wt))
    return {x.strip() for x in s}


def _blocks(wt, name):
    return re.findall(r"\{\{" + name + r"\b(.*?)\}\}", wt, re.S)


def parse_relationships(wt):
    out = []
    for b in _blocks(wt, "Relationship"):
        f = dict(re.findall(r"\|([a-z_]+)=([^\n|]*)", b))
        out.append({
            "predicate": f.get("predicate", "").strip(),
            "object": f.get("object", "").strip(),
            "sources": [s.strip() for s in f.get("sources", "").split(",") if s.strip()],
            "verification": f.get("verification", "").strip(),
        })
    return out


def check_ref_markup(wt):
    """Structural problems in <ref>/marker markup that nothing else catches.

    Inserting two citations at the same offset corrupts them into
    <<ref>A</ref>ref>B</ref>, which leaks a literal 'ref>' onto the rendered
    page while every {{Cite}} name still resolves.
    """
    errs = []
    if "<<ref" in wt:
        errs.append("malformed ref markup: '<<ref' (two refs inserted at the same offset)")
    if re.search(r"</ref>\s*ref>", wt):
        errs.append("malformed ref markup: '</ref>ref>' (interleaved refs)")
    opens = len(re.findall(r"<ref(?:\s[^>]*)?>", wt))
    closes = len(re.findall(r"</ref>", wt))
    selfclosing = len(re.findall(r"<ref[^>]*/>", wt))
    if opens - selfclosing != closes:
        errs.append("unbalanced <ref> tags: %d opening, %d closing" % (opens - selfclosing, closes))
    if re.search(r"\{\{Unsourced\}\}\s*\{\{Unsourced\}\}", wt):
        errs.append("duplicate {{Unsourced}} markers on the same claim")
    return errs


def missing_templates(html):
    """Templates used on the page that do not exist on this wiki.

    A missing template produces NO parser error: MediaWiki renders the literal
    text "Template:Foo" as a red link and the page merely looks odd. Found on
    2026-07-28 with {{'}}, a Wikipedia convenience template this wiki has never
    had. The name arrives URL-encoded in the redlink href.
    """
    return sorted({urllib.parse.unquote(x) for x in
                   re.findall(r'title=Template:([^"&]+)[^"]*redlink=1', html or "")})


# --------------------------------------------------------------------------
# Live wrapper (Task 3)
# --------------------------------------------------------------------------


def verify_entity(title, get_page, list_sources, read_ledger):
    """Run every mechanical check for one entity. Returns [] on PASS.

    I/O is injected so this is testable without a wiki or filesystem.

    LIMITS (be honest about these — see verification/SKILL.md):
      * "every checkable fact has a ledger row" is NOT mechanically decidable;
        this checks the direction it can (cites resolve, quotes exist) and
        leaves fact-by-fact coverage to the claim-ledger discipline.
      * the unknown-on-page check is a literal substring match, so it catches
        copy-pasted claims, not paraphrases.
    """
    wt = get_page(title) or ""
    errs = []

    errs += check_ref_markup(wt)

    cited = extract_cites(wt)
    sources = set(list_sources())
    for c in sorted(cited):
        if c not in sources:
            errs.append("cite → nonexistent Source page: '%s'" % c)

    if not cited:
        errs.append("page has no inline citations ({{Cite}}/<ref>); every checkable "
                    "fact must be cited or marked {{Inference}}")

    ledger = parse_ledger(read_ledger(title) or "")
    if not ledger:
        errs.append("no claim ledger rows found for '%s' "
                    "(expected the 8-column table: id | claim | quote | source page | "
                    "url | tier | status | confidence)" % title)

    errs += check_ai_verified(parse_relationships(wt))
    errs += check_ledger_coverage(cited, ledger)

    low = wt.lower()
    for r in ledger:
        if r["status"] == "unknown" and r["claim"] and r["claim"].lower() in low:
            errs.append("ledger claim '%s' is 'unknown' but appears on-page "
                        "(empty beats wrong)" % r["claim"][:40])

    inference_rows = [r for r in ledger if r["status"] == "inference"]
    if inference_rows and "{{Inference" not in wt:
        errs.append("%d 'inference' ledger row(s) but no {{Inference}} marker on-page"
                    % len(inference_rows))

    return errs


def check_render(title, wiki):
    """Render-level checks. Needs a live wiki; returns [] on PASS.

    Kept separate from verify_entity (which is pure-ish and injectable) but
    called by BOTH main() and the publishing scripts — a check that only main()
    runs is a check that new pages never get.
    """
    errs = []
    r = wiki.render(title)
    if r.get("error_markers"):
        errs.append("render errors: %s" % r["error_markers"])
    missing = missing_templates(r.get("html", ""))
    if missing:
        errs.append("page uses template(s) that do not exist on this wiki: %s. They render "
                    "as the literal text 'Template:Name'." % ", ".join(missing))
    wt_now = wiki.get(title) or ""
    if "{{Relationship" in wt_now:
        html = r.get("html", "")
        if 'id="Relationships"' not in html and ">Relationships<" not in html:
            errs.append("page has a {{Relationship}} block but renders no Relationships "
                        "section (Cargo rows missing). Check for a comma in a Source title in "
                        "sources=, then do a NULL EDIT (re-save); purge alone will not fix it.")
        def norm_title(x):
            x = x.strip()
            return x[:1].upper() + x[1:] if x else x
        known = {norm_title(x) for x in wiki.list_category("Category:Sources")}
        for m in re.findall(r"\|sources=([^\n]*)", wt_now):
            for part in m.split(","):
                if part.strip() and norm_title(part) not in known:
                    errs.append("relationship sources= contains '%s', which is not a Source "
                                "page. sources= is comma-delimited, so Source titles must not "
                                "contain commas." % part.strip()[:60])
    return errs


def main():
    import sys

    # Deferred to inside main() (matching the original) so that importing
    # this module for its pure/injectable functions never requires wiki.py
    # (and a live wiki) to be present.
    from research_mediawiki import wiki
    from research_core.paths import ledger as ledger_path

    if len(sys.argv) < 2:
        print("usage: verify.py \"<Entity page title>\"", file=sys.stderr)
        sys.exit(2)
    title = sys.argv[1]

    def read_ledger(t):
        path = ledger_path(t)
        try:
            with open(path) as f:
                return f.read()
        except OSError:
            return ""

    wiki.ensure_login()
    errs = verify_entity(title, wiki.get,
                         lambda: wiki.list_category("Category:Sources"),
                         read_ledger)
    if errs:
        print("VERIFY FAIL: %s" % title)
        for e in errs:
            print("  - " + e)
        sys.exit(1)

    rerrs = check_render(title, wiki)
    if rerrs:
        print("VERIFY FAIL: %s" % title)
        for e in rerrs:
            print("  - " + e)
        sys.exit(1)

    wt_now = wiki.get(title) or ""
    n = len(extract_cites(wt_now))
    print("VERIFY PASS: %s (render clean, %d cite(s) all resolve)" % (title, n))


if __name__ == "__main__":
    main()
