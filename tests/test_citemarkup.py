#!/usr/bin/env python3
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))
from research_mediawiki.citemarkup import (
    parse_cites, strip_refs, remove_refs, remove_paired_refs, format_cite,
)


class TestParseCites(unittest.TestCase):
    def test_extracts_source_and_quote(self):
        raw = 'The mill closed.<ref>{{Cite|Castlegar News 1975|quote=the mill closed in 1975}}</ref>'
        self.assertEqual(parse_cites(raw), [("Castlegar News 1975", "the mill closed in 1975")])

    def test_extracts_multiple_cites(self):
        raw = ('A.<ref>{{Cite|S1|quote=q one}}</ref> B.<ref>{{Cite|S2|quote=q two}}</ref>')
        self.assertEqual(parse_cites(raw), [("S1", "q one"), ("S2", "q two")])

    def test_quote_may_span_newlines(self):
        raw = '<ref>{{Cite|S|quote=first line\nsecond line}}</ref>'
        self.assertEqual(parse_cites(raw), [("S", "first line\nsecond line")])

    def test_quote_containing_pipe_character(self):
        # Quote can contain literal | as long as it's inside the quote value
        raw = '<ref>{{Cite|Source X|quote=he said "A|B" happened}}</ref>'
        self.assertEqual(parse_cites(raw), [("Source X", 'he said "A|B" happened')])

    def test_two_cites_in_one_ref_not_separated(self):
        # Known limitation: two {{Cite}} blocks in one <ref> are not parsed as
        # separate results; the first absorbs the second into its quote
        raw = '<ref>{{Cite|S1|quote=q1}}{{Cite|S2|quote=q2}}</ref>'
        result = parse_cites(raw)
        # First cite absorbs second into its quote
        self.assertEqual(result, [("S1", "q1}}{{Cite|S2|quote=q2")])

    def test_no_cites_returns_empty(self):
        self.assertEqual(parse_cites("plain prose with no citation"), [])


class TestStripRefs(unittest.TestCase):
    def test_removes_paired_ref(self):
        self.assertEqual(strip_refs("Alpha<ref>{{Cite|S|quote=q}}</ref> beta"), "Alpha beta")

    def test_removes_self_closing_ref(self):
        self.assertEqual(strip_refs('Alpha<ref name="x"/> beta'), "Alpha beta")

    def test_removes_ref_spanning_newlines(self):
        self.assertEqual(strip_refs("Alpha<ref>line\nline</ref> beta"), "Alpha beta")

    def test_leaves_plain_prose_untouched(self):
        self.assertEqual(strip_refs("nothing to strip"), "nothing to strip")

    def test_preserves_leading_and_trailing_whitespace(self):
        # Locks in behaviour: strip_refs should NOT call .strip()
        result = strip_refs("<ref>x</ref> middle <ref>y</ref>")
        self.assertEqual(result, " middle ")


class TestRemovePairedRefs(unittest.TestCase):
    def test_removes_paired_ref(self):
        self.assertEqual(
            remove_paired_refs("Alpha<ref>{{Cite|S|quote=q}}</ref> beta"),
            "Alpha  beta",
        )

    def test_leaves_references_tag_intact(self):
        # Regression: the self-closing pattern <ref[^>]*/> also matches
        # <references/>, which real wiki pages carry. remove_paired_refs must
        # NOT touch it -- only remove_refs/strip_refs (which explicitly also
        # strip self-closing tags) are allowed to remove it.
        self.assertEqual(
            remove_paired_refs("Body text.\n<references/>\nMore text."),
            "Body text.\n<references/>\nMore text.",
        )

    def test_leaves_self_closing_named_ref_intact(self):
        self.assertEqual(
            remove_paired_refs('Alpha<ref name="x"/> beta'),
            'Alpha<ref name="x"/> beta',
        )

    def test_paired_ref_removed_but_self_closing_ones_preserved_together(self):
        text = '<references/>A<ref>{{Cite|S|quote=q}}</ref>B<ref name="x"/>C'
        self.assertEqual(
            remove_paired_refs(text),
            '<references/>A B<ref name="x"/>C',
        )


class TestRemoveRefs(unittest.TestCase):
    def test_removes_paired_ref(self):
        self.assertEqual(remove_refs("Alpha<ref>{{Cite|S|quote=q}}</ref> beta"), "Alpha  beta")

    def test_removes_self_closing_ref(self):
        self.assertEqual(remove_refs('Alpha<ref name="x"/> beta'), "Alpha  beta")

    def test_preserves_newlines_outside_ref(self):
        # Regression: remove_refs must NOT collapse whitespace, unlike
        # strip_refs. Callers doing line-oriented passes (e.g. the heading
        # regex in anchorcheck_cli.sentence_text) depend on line structure
        # surviving ref removal.
        result = remove_refs("== Heading text <ref>\nmulti\nline\nref\n</ref> continues ==\nBody")
        self.assertEqual(result, "== Heading text   continues ==\nBody")
        self.assertIn("\n", result)

    def test_strip_refs_still_collapses_whitespace(self):
        # strip_refs is remove_refs plus whitespace collapse; this must not
        # change now that remove_refs exists underneath it.
        result = strip_refs("== Heading text <ref>\nmulti\nline\nref\n</ref> continues ==\nBody")
        self.assertNotIn("\n", result)
        self.assertEqual(result, "== Heading text continues == Body")


class TestFormatCite(unittest.TestCase):
    def test_roundtrips_through_parse(self):
        out = format_cite("Daily Colonist 1959", "the strike began in September")
        self.assertEqual(parse_cites(out), [("Daily Colonist 1959", "the strike began in September")])

    def test_roundtrips_quote_with_equals_and_braces(self):
        # Quote can contain = and }} as long as they're not followed by </ref>
        quote = 'She said "a=b" and wrote: var x = {key: value}}'
        out = format_cite("Source", quote)
        self.assertEqual(parse_cites(out), [("Source", quote)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
