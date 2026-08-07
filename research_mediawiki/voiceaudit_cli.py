#!/usr/bin/env python3
"""MediaWiki CLI for research_core.voiceaudit: find prose written to the
reviewer instead of to the reader.

This is the wiki-facing half of voiceaudit.py. It knows how to choose pages and
fetch them; the pattern set and the severities live in research_core.voiceaudit
and know nothing about wikis.

It never writes. There is no --write to get wrong: the fix for a finding is a
judgment about what a sentence was trying to say, and that is not a substitution
a script should be making unattended.

usage:
  voiceaudit_cli.py                     every entity and event page
  voiceaudit_cli.py --page "Crofton"    one page (repeatable)
  voiceaudit_cli.py --file list.txt     one title per line
  voiceaudit_cli.py --summary           counts per page, worst first
  voiceaudit_cli.py --titles            flagged titles only, ready for --file
  voiceaudit_cli.py --errors-only       drop the WARN findings
  voiceaudit_cli.py --include-sources   audit Source: pages too (see below)

exit status: 0 when nothing was flagged, 1 when anything was, 2 on a usage or
fetch failure. The non-zero-on-findings behaviour is what makes it usable in a
definition of done.

Source pages are excluded by default. A Source page's job is to describe what
its source covers and how it was captured, so the vocabulary this check flags is
the vocabulary that page is supposed to use. Auditing them by default would bury
the real findings under several hundred correct ones.
"""
import argparse
import sys

from research_core.voiceaudit import ERROR, WARN, audit, counts, worst_first
from research_mediawiki import wiki
from research_mediawiki.voicemarkup import scan_page


def choose_titles(args):
    """The titles to audit, given the CLI arguments.

    Category membership rather than template sniffing: Category:Entities is the
    wiki's own answer to "is this an article", and it already includes the event
    pages. Sources are a subset of it, which is why they are subtracted rather
    than filtered by name.
    """
    if args.page:
        return list(args.page)
    if args.file:
        with open(args.file) as fh:
            return [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

    titles = set(wiki.list_category("Category:Entities"))
    if not args.include_sources:
        titles -= set(wiki.list_category("Category:Sources"))
    return sorted(t for t in titles if not t.startswith("Category:"))


def fetch(titles):
    """{title: markup}. A title that does not exist is reported, not skipped
    silently -- a typo in a --file list should not read as a clean page."""
    pages = {}
    missing = []
    for t in titles:
        markup = wiki.get(t)
        if markup is None:
            missing.append(t)
        else:
            pages[t] = markup
    for t in missing:
        print("MISSING: %s (no such page)" % t, file=sys.stderr)
    return pages


def report(results, errors_only, summary, titles_only=False):
    order = worst_first(results)
    if titles_only:
        # One title per line and nothing else, so the output feeds straight back
        # in through --file. Worth a flag rather than leaving callers to cut
        # fields off the summary: titles contain spaces, and every awk recipe
        # for stripping the counts breaks on the first title that does not.
        for title in order:
            if errors_only and not any(f.severity == ERROR for f in results[title]):
                continue
            print(title)
        return

    if summary:
        for title in order:
            findings = [f for f in results[title]
                        if not errors_only or f.severity == ERROR]
            if not findings:
                continue
            e = sum(1 for f in findings if f.severity == ERROR)
            w = len(findings) - e
            print("%3d error  %3d warn   %s" % (e, w, title))
        return

    for title in order:
        findings = [f for f in results[title]
                    if not errors_only or f.severity == ERROR]
        if not findings:
            continue
        print("\n=== %s" % title)
        for f in findings:
            print("  %-5s %-16s %-7s line %-4d %s"
                  % (f.severity, f.name, f.where, f.line, f.snippet[:120]))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--page", action="append", help="audit one page (repeatable)")
    p.add_argument("--file", help="file of titles, one per line")
    p.add_argument("--summary", action="store_true", help="counts per page only")
    p.add_argument("--titles", action="store_true",
                   help="flagged titles only, one per line, ready for --file")
    p.add_argument("--errors-only", action="store_true", help="drop WARN findings")
    p.add_argument("--include-sources", action="store_true",
                   help="audit Source pages too (off by default; see module docstring)")
    args = p.parse_args(argv)

    if args.page and args.file:
        p.error("--page and --file are alternatives")

    wiki.ensure_login()
    titles = choose_titles(args)
    if not titles:
        # Not "clean". Selecting no pages means the category query or the file
        # was wrong, and reporting success here would convert an unexamined
        # corpus into one that looks examined.
        print("ERROR: selected no pages to audit", file=sys.stderr)
        return 2

    pages = fetch(titles)
    if not pages:
        print("ERROR: fetched no pages from %d titles" % len(titles), file=sys.stderr)
        return 2

    # audit() raises on an empty mapping; the guard above means it cannot here,
    # and the raise stays as the backstop for callers that skip this CLI.
    # scan_page is what makes this a wikitext audit: without it, audit() would
    # match inside quotations.
    results = audit(pages, scanner=scan_page)

    if not results:
        if not args.titles:
            print("clean: %d pages, no findings" % len(pages))
        return 0

    report(results, args.errors_only, args.summary, args.titles)
    if args.titles:
        # Nothing but titles on stdout: the summary line would be read back in
        # as a page title by the next --file run.
        return 1

    c = counts(results)
    shown = c[ERROR] if args.errors_only else c[ERROR] + c[WARN]
    print("\n%d error, %d warn across %d of %d pages"
          % (c[ERROR], c[WARN], len(results), len(pages)))
    return 1 if shown else 0


if __name__ == "__main__":
    sys.exit(main())
