#!/usr/bin/env python3
"""The one place that knows what <ref>{{Cite|Name|quote=...}}</ref> looks like.

Before this module, the same regex was duplicated verbatim in anchorcheck.py and
weakcites.py, <ref>-stripping was reimplemented in anchorcheck.py and
crosscheck.py, and addcite.py built the markup by hand. Four modules could not
move to core/ because of markup none of them actually cared about — they wanted
(source, quote) pairs and prose.
"""
import re

# Kept byte-identical to the original in anchorcheck.py:148 / weakcites.py:37 so
# this is a pure move. Any behaviour change belongs in its own commit.
_CITE = re.compile(r"\{\{Cite\|([^|}]+)\|quote=(.*?)\}\}</ref>", re.S)
_REF_PAIRED = re.compile(r"<ref>.*?</ref>", re.S)
_REF_SELF_CLOSING = re.compile(r"<ref[^>]*/>")


def parse_cites(raw):
    """[(source_title, quote)] for every {{Cite}} carried by a <ref> on the page.

    Known limitation: two {{Cite}} blocks inside a single <ref> are NOT parsed as
    separate results. The first Cite block absorbs the second into its quote:
    parse_cites('<ref>{{Cite|S1|quote=q1}}{{Cite|S2|quote=q2}}</ref>')
    -> [('S1', 'q1}}{{Cite|S2|quote=q2')]
    """
    return _CITE.findall(raw)


def remove_refs(text):
    """Prose with <ref> markup removed and nothing else touched.

    Whitespace is deliberately NOT collapsed: callers that run further
    line-oriented passes (heading and markup stripping) need the original line
    structure intact. Collapsing here silently breaks a heading whose ==
    fence straddles a multi-line <ref>.
    """
    out = _REF_PAIRED.sub(" ", text)
    return _REF_SELF_CLOSING.sub(" ", out)


def strip_refs(text):
    """remove_refs plus whitespace collapse — matches crosscheck.py's prose().

    Deliberately no .strip(): crosscheck.py:55 does not strip, and callers that
    want trimmed output do it themselves.
    """
    return re.sub(r"\s+", " ", remove_refs(text))


def format_cite(source, quote):
    """A complete <ref>, the inverse of parse_cites."""
    return "<ref>{{Cite|%s|quote=%s}}</ref>" % (source, quote)
