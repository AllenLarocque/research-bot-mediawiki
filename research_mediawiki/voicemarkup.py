#!/usr/bin/env python3
"""What a voice audit needs to know about wikitext, and nothing else.

research_core.voiceaudit matches patterns against text and returns offsets. Two
things it cannot work out for itself, because both are properties of the markup:
which spans a reader never sees, and which surface an offset sits on. This
module is the MediaWiki answer to both, in the same spirit as citemarkup.py --
the one place that knows what the markup looks like, so the checker upstairs
does not have to.

The skipped spans matter more than the surfaces. The response to a voice finding
is "reword this". Rewording a quotation is fabrication, and text kept in
guillemets is a withdrawn quotation preserved byte-for-byte precisely so a later
reader can still see it. A finding in either is an instruction to do damage, so
both are blanked before matching.
"""
import re

# HEADING and NOTE are imported, never redefined. voiceaudit keys its
# per-surface severities on these exact strings, so a local copy that drifted
# would not raise -- every finding would quietly take the default severity
# instead, and the surface-dependent rule would stop working with nothing to
# show for it.
from research_core.voiceaudit import HEADING, NOTE, PROSE, scan

# A citation's quote= is a verbatim copy of a source. A source is free to say
# "the wiki" or "corpus"; that is the publisher's word, not the agent's, and it
# is not the agent's to edit.
_REF = re.compile(r"<ref[^>]*>.*?</ref>", re.S | re.I)
_REF_SELF_CLOSING = re.compile(r"<ref[^>]*/>", re.I)
# Guillemets wrap a retracted quotation, kept byte-for-byte so nothing is lost.
_RETRACTED = re.compile("‹.*?›", re.S)
# Rendered to nobody.
_COMMENT = re.compile(r"<!--.*?-->", re.S)
# Shown as literal markup, usually to document syntax.
_LITERAL = re.compile(r"<(nowiki|pre|syntaxhighlight)\b[^>]*>.*?</\1>", re.S | re.I)
# An inline gap marker. A reader DOES see this one, which is why it is worth
# saying what the list is really for: not "invisible", but "not the agent's
# prose to reword". {{Unsourced}} beside a claim marks something a contributor
# can close, exactly as a red link does. The word "unsourced" in it is the
# template's name, so flagging it asks an agent to edit the data model.
_MARKER = re.compile(r"\{\{\s*Unsourced\b[^}]*\}\}", re.I)

_UNREADABLE = (_REF, _REF_SELF_CLOSING, _RETRACTED, _COMMENT, _LITERAL, _MARKER)

_HEADING = re.compile(r"^(={2,})\s*(.+?)\s*\1\s*$", re.M)
# A note= parameter renders on the page. It is page surface, and the page-voice
# rule governs it -- a row's note is not dossier text.
_NOTE = re.compile(r"\|\s*note\s*=", re.I)


def unreadable_spans(markup):
    """(start, end) of every span the voice rule does not govern.

    Mostly text no reader sees -- citations, retractions, comments -- but the
    test is authorship, not visibility: a span belongs here when its words are
    somebody else's (a publisher's, a template's) and rewording them would be
    fabrication, vandalism of provenance, or an edit to the data model.
    """
    spans = []
    for pattern in _UNREADABLE:
        spans += [(m.start(), m.end()) for m in pattern.finditer(markup)]
    return sorted(spans)


def note_spans(markup):
    """(start, end) of every note= value.

    Scanned rather than matched with `[^|}]*`: a note may contain a wikilink,
    and a piped link has a pipe in it that a lazy matcher stops at, truncating
    the value and losing anything narrated after the link.
    """
    spans = []
    for m in _NOTE.finditer(markup):
        i = m.end()
        depth = 0
        while i < len(markup):
            if markup.startswith("[[", i):
                depth += 1
                i += 2
                continue
            if markup.startswith("]]", i):
                depth = max(0, depth - 1)
                i += 2
                continue
            if depth == 0 and (markup[i] == "|" or markup.startswith("}}", i)):
                break
            i += 1
        spans.append((m.end(), i))
    return spans


def heading_spans(markup):
    """(start, end) of every section heading's text, brackets excluded."""
    return [(m.start(2), m.end(2)) for m in _HEADING.finditer(markup)]


def surface(markup):
    """offset -> "heading" | "note" | "prose", for one page's markup."""
    headings = heading_spans(markup)
    notes = note_spans(markup)

    def label(offset):
        if any(a <= offset < b for a, b in headings):
            return HEADING
        if any(a <= offset < b for a, b in notes):
            return NOTE
        return PROSE

    return label


def scan_page(markup):
    """research_core.voiceaudit.scan, wired up for wikitext."""
    return scan(markup, skip=unreadable_spans(markup), surface=surface(markup))
