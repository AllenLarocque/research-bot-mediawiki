#!/usr/bin/env python3
"""Wikitext structure for the citation retrofit: where the narrative region
is, how it splits into sentences, and which sources a page actually uses.

This is the wiki-facing remainder of retro.py. `narrative_span`,
`page_sentences` and `sources_used` all parse `{{Relationship}}` /
`{{Entity footer}}` template syntax and `|sources=` infobox fields -- real
wikitext structure -- so they stay here rather than moving to research_core/.

`plain()` (wikitext -> readable text) stays here too, alongside them, even
though the Task 8 brief's interface sketch put it in research_core.textutil:
its own implementation strips `[[links]]`, `<ref>` tags and `{{templates}}`
by recognising that syntax directly, which is exactly the wikitext-structure
knowledge research_core/ is not allowed to carry (tests/test_layering.py scans research_core/
source text for that syntax literally). The rest of the original text
utilities (`split_sentences`, `words`, `norm`, `slug`) and the source-cache
readers (`load_manifest`, `source_text`, `src_sentences`, `verify_quote`)
moved to research_core.textutil and research_core.srccache, which this module
uses rather than duplicates.
"""
import re

from research_core.textutil import split_sentences


def plain(s):
    """Wikitext -> readable text."""
    s = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def narrative_span(wt):
    """(start, end) offsets of the prose region in the wikitext."""
    end = len(wt)
    for pat in (r"\{\{Relationship\b", r"\{\{Entity footer\b"):
        m = re.search(pat, wt)
        if m:
            end = min(end, m.start())
    # start: after the LEADING run of templates (banner, infobox). Stop as soon
    # as real prose begins — templates inside the prose (e.g. {{Inference}}) must
    # not move the start.
    i, start = 0, 0
    while i < end:
        if wt[i].isspace():
            i += 1
            continue
        if wt.startswith("{{", i):
            depth, j = 0, i
            while j < end:
                if wt.startswith("{{", j):
                    depth += 1; j += 2; continue
                if wt.startswith("}}", j):
                    depth -= 1; j += 2
                    if depth == 0:
                        break
                    continue
                j += 1
            i = start = j
            continue
        break
    return start, end


def page_sentences(wt):
    """[(idx, abs_start, abs_end, raw_text)] for the narrative region."""
    s, e = narrative_span(wt)
    region = wt[s:e]
    out = []
    for n, (a, b) in enumerate(split_sentences(region), 1):
        raw = region[a:b]
        if raw.strip():
            out.append((n, s + a, s + b, raw))
    return out


def sources_used(wt, ledtext, manifest):
    used = {s.strip() for m in re.findall(r"\|sources=([^\n]*)", wt)
            for s in m.split(",") if s.strip()}
    for t in manifest:
        if t in ledtext or t in wt:
            used.add(t)
    return used
