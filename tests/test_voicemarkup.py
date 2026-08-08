#!/usr/bin/env python3
"""Wikitext-side tests for the voice audit: what a reader never sees, and which
surface an offset sits on.

The pattern set and the severities are tested in the template repo against
research_core.voiceaudit, which is not allowed to know what a <ref> is.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))
try:
    from research_core.voiceaudit import ERROR
    from research_mediawiki.voicemarkup import (
        HEADING, NOTE, heading_spans, note_spans, scan_page, surface,
        unreadable_spans,
    )
    HAVE_VOICEAUDIT = True
except ImportError:
    # This repo's tests run against adapters/wiki/template -- its OWN pin of the
    # template, deliberately separate from the one PYTHONPATH names at runtime
    # (see the diamond note in the deployable's .gitmodules). research_core
    # .voiceaudit landed in the template after that pin, so until the pin is
    # bumped these tests have nothing to run against.
    #
    # Skipped rather than left to raise ImportError: a red suite with an opaque
    # traceback reads as "the adapter is broken", when what is true is "the
    # adapter's pinned dependency is older than this test". Skipped rather than
    # deleted, or silently passing, because the skip message is the record of
    # what has to happen next.
    HAVE_VOICEAUDIT = False


NEEDS_PIN_BUMP = unittest.skipUnless(
    HAVE_VOICEAUDIT,
    "needs research_core.voiceaudit: bump the adapters/wiki/template pin")


def names(findings):
    return set(f.name for f in findings)


@NEEDS_PIN_BUMP
class TestUnreadable(unittest.TestCase):
    """The spans where acting on a finding would do damage."""

    def test_a_quotation_naming_the_wiki_is_not_flagged(self):
        # The fix for a finding is "reword this". Rewording a quotation is
        # fabrication -- so a trigger word inside a citation must never be
        # reported, however genuinely the publisher wrote it.
        wt = ('The mill closed in 1953.<ref>{{Cite|Some Source'
              '|quote=the wiki of record for this corpus}}</ref>')
        self.assertEqual(scan_page(wt), [])

    def test_retracted_text_in_guillemets_is_not_flagged(self):
        # Guillemet text is a withdrawn quotation kept byte-for-byte. Editing it
        # destroys the provenance the retraction exists to preserve.
        wt = "Withdrawn, wrong attribution: ‹ this page rests on one publisher ›"
        self.assertEqual(scan_page(wt), [])

    def test_html_comments_are_not_flagged(self):
        self.assertEqual(scan_page("<!-- this page needs a second publisher -->"), [])

    def test_nowiki_is_not_flagged(self):
        self.assertEqual(scan_page("<nowiki>{{Claim|the corpus}}</nowiki>"), [])

    def test_an_inline_needs_a_citation_marker_is_not_flagged(self):
        # {{Unsourced}} beside a claim is an inline gap marker doing the job
        # CLAUDE.md gives a red link -- marking something a contributor can
        # close. The word is the template's, not the agent's prose, so there is
        # nothing here to reword.
        wt = "The mill supplied Youbou and Honeymoon Bay.{{Unsourced}}"
        self.assertEqual(scan_page(wt), [])

    def test_an_unsourced_marker_with_parameters_is_also_masked(self):
        wt = "A claim.{{Unsourced|reason=no capture names the town}}"
        self.assertEqual(scan_page(wt), [])

    def test_the_ordinary_word_unsourced_is_still_flagged(self):
        # Masking the template must not blind the check to the page calling its
        # own prose unsourced.
        wt = "where before it was an unsourced arithmetic claim"
        self.assertIn("meta-unsourced", names(scan_page(wt)))

    def test_self_closing_ref_is_covered(self):
        self.assertEqual(unreadable_spans('a<ref name="x" />b'), [(1, 17)])

    def test_prose_outside_a_ref_is_still_flagged(self):
        wt = 'A.<ref>{{Cite|S|quote=irrelevant}}</ref>\n\nThe corpus knows.'
        found = scan_page(wt)
        self.assertEqual([f.name for f in found], ["names-corpus"])
        self.assertEqual(found[0].line, 3)
        self.assertEqual(wt[found[0].start:found[0].end], "corpus")


@NEEDS_PIN_BUMP
class TestSurfaces(unittest.TestCase):
    def test_a_bare_ordinal_heading_is_an_error_because_it_is_a_heading(self):
        # In running prose these words are only a warning -- two writers may
        # legitimately count something differently. A section heading organised
        # by source-order is the page describing its own research, so the same
        # words are an error here. This is the surface carrying the severity.
        wt = "== A second publisher, for the closure ==\n\nProse."
        found = [f for f in scan_page(wt) if f.name == "source-ordinal"]
        self.assertEqual([(f.where, f.severity) for f in found], [(HEADING, ERROR)])

    def test_the_same_heading_words_in_prose_are_only_a_warning(self):
        found = [f for f in scan_page("counted by a second publisher elsewhere")
                 if f.name == "source-ordinal"]
        self.assertEqual([f.severity for f in found], ["warn"])

    def test_note_parameter_is_page_surface(self):
        wt = "{{Relationship|predicate=owns|object=Mill|note=the wiki has no page for it}}"
        found = [f for f in scan_page(wt) if f.name == "names-wiki"]
        self.assertEqual([f.where for f in found], [NOTE])

    def test_a_wikilink_pipe_does_not_truncate_a_note(self):
        # A piped link has a pipe in it; a lazy [^|}]* stops there and loses
        # everything narrated after the link. Two spans match here -- "rests on"
        # and "one publisher" -- and both sit after the link.
        wt = ("{{Relationship|predicate=owns|object=Mill"
              "|note=see [[Port Alberni|the town]], though this page rests on one publisher}}")
        found = [f for f in scan_page(wt) if f.name == "rests-on"]
        self.assertEqual(len(found), 2)
        self.assertEqual(set(f.where for f in found), {NOTE})

    def test_prose_is_the_default(self):
        self.assertEqual([f.where for f in scan_page("The corpus did not have it.")],
                         ["prose"])

    def test_heading_spans_exclude_the_equals_signs(self):
        wt = "== Ownership =="
        (a, b), = heading_spans(wt)
        self.assertEqual(wt[a:b], "Ownership")

    def test_note_spans_stop_at_the_next_parameter(self):
        wt = "{{Relationship|note=first|sources=S}}"
        (a, b), = note_spans(wt)
        self.assertEqual(wt[a:b], "first")

    def test_the_surface_labels_are_the_ones_voiceaudit_rates(self):
        # Not a tautology: these are the keys voiceaudit's severity maps use.
        # A local copy of either string would fall back to the default severity
        # rather than raise, so the surface rule would fail silently.
        from research_core.voiceaudit import HEADING as CORE_H, NOTE as CORE_N
        self.assertEqual((HEADING, NOTE), (CORE_H, CORE_N))

    def test_surface_of_an_offset_outside_everything(self):
        label = surface("plain prose only")
        self.assertEqual(label(3), "prose")


@NEEDS_PIN_BUMP
class TestRealPageShape(unittest.TestCase):
    def test_a_published_page_extract(self):
        # Trimmed from Somass Sawmill closure (2017) as it stood before this
        # check existed: an error in the heading, warns in the prose, and a
        # quotation that must survive untouched.
        wt = (
            "In 2017, Western Forest Products announced the closure"
            "<ref>{{Cite|Wikipedia|quote=WFP closed their mills in Port Alberni}}</ref>.\n"
            "\n== A second publisher — for the closure, but not for the year ==\n"
            "\nThe closure year on this page still rests on a single publisher.\n"
        )
        found = scan_page(wt)
        self.assertIn("source-ordinal", names(found))
        self.assertEqual([f.where for f in found if f.severity == ERROR], [HEADING])
        self.assertIn("rests-on", names(found))
        # Nothing inside the citation.
        for f in found:
            self.assertNotIn("WFP closed", wt[f.start:f.end])


if __name__ == "__main__":
    unittest.main()
