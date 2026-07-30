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
    """[(source_title, quote)] for every {{Cite}} carried by a <ref> on the page."""
    return _CITE.findall(raw)


def strip_refs(text):
    """Prose with citation markup removed, so callers can analyse sentences."""
    out = _REF_PAIRED.sub(" ", text)
    out = _REF_SELF_CLOSING.sub(" ", out)
    return re.sub(r"\s+", " ", out).strip()


def format_cite(source, quote):
    """A complete <ref>, the inverse of parse_cites."""
    return "<ref>{{Cite|%s|quote=%s}}</ref>" % (source, quote)
