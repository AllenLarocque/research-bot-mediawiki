#!/usr/bin/env python3
"""Tests for research_mediawiki.verify — the wikitext/HTML half of the old
verify.py.

Ported from /dossiers/_skillset/forestwiki-research/scripts/test_verify.py.
Everything here needs {{Cite}}, <ref>, {{Relationship}} wikitext, or rendered
redlink HTML; the markdown-ledger and parsed-relationship-dict tests moved to
tests/test_ledger.py instead.

NOTE: the fixtures use double-quoted triple strings because the wikitext
contains ''' bold ''' markup, which would terminate a ''' Python string
(same reason the original test_verify.py gave for this).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))
from research_mediawiki.verify import (missing_templates, extract_cites, parse_relationships,
                                       check_ref_markup, verify_entity)
from research_core.ledger import check_ai_verified

WT = """{{Organization|name=Foo}}
'''Foo''' was founded in 1919<ref>{{Cite|Canadian Encyclopedia — X|quote=launched in 1919}}</ref>.
{{Relationship|predicate=acquired|object=Bar|sources=Wikipedia — Y,SEC — Z|verification=ai-verified}}
{{Relationship|predicate=owned_by|object=Baz|sources=Wikipedia — Y|verification=ai-verified}}
{{Entity footer}}"""


class TestWikitextParsing(unittest.TestCase):
    def test_extract_cites(self):
        self.assertEqual(extract_cites(WT), {"Canadian Encyclopedia — X"})

    def test_parse_relationships_counts_sources(self):
        rels = parse_relationships(WT)
        self.assertEqual(rels[0]["sources"], ["Wikipedia — Y", "SEC — Z"])
        self.assertEqual(rels[0]["verification"], "ai-verified")


class TestAiVerifiedComposition(unittest.TestCase):
    """Confirms adapter parsing + research_core.ledger.check_ai_verified compose
    to the same behaviour the original single-module check_ai_verified had."""

    def test_check_ai_verified_flags_single_source(self):
        errs = check_ai_verified(parse_relationships(WT))
        self.assertTrue(any("owned_by → Baz" in e and "1 source" in e for e in errs))
        self.assertFalse(any("acquired → Bar" in e for e in errs))


class TestRefMarkup(unittest.TestCase):
    """Interleaved refs: two citations inserted at the same offset corrupt each
    other into <<ref>A</ref>ref>B</ref>. Rendered, this leaks literal 'ref>'
    text onto the page, and the {{Cite}} names still resolve, so nothing else
    catches it."""

    def test_flags_interleaved_refs(self):
        wt = "Claim<<ref>{{Cite|A}}</ref>ref>{{Cite|B}}</ref>."
        self.assertTrue(check_ref_markup(wt))

    def test_flags_unbalanced_refs(self):
        self.assertTrue(check_ref_markup("Claim<ref>{{Cite|A}}."))

    def test_flags_duplicate_unsourced(self):
        self.assertTrue(check_ref_markup("Claim{{Unsourced}}{{Unsourced}}."))

    def test_accepts_two_adjacent_refs(self):
        wt = "Claim<ref>{{Cite|A}}</ref><ref>{{Cite|B}}</ref>."
        self.assertEqual(check_ref_markup(wt), [])


class TestLiveWrapper(unittest.TestCase):
    def test_verify_entity_flags_unknown_on_page_and_missing_source(self):
        wt = "Foo did X<ref>{{Cite|Ghost}}</ref>. HQ was Vancouver."  # 'Ghost' not a Source page
        ledger = ('| id | claim | quote | source page | url | tier | status | confidence |\n'
                  '|1|X|"x happened"|Real|u|T2|sourced|high|\n'
                  '|2|HQ Vancouver||—|—|—|unknown|low|')
        errs = verify_entity("Foo", get_page=lambda t: wt,
                             list_sources=lambda: ["Real"],
                             read_ledger=lambda t: ledger)
        self.assertTrue(any("Ghost" in e for e in errs))

    def test_verify_entity_flags_page_with_no_citations(self):
        """A legacy uncited page must NOT pass (this was a false PASS)."""
        wt = "Foo was founded in 1919 and closed in 1998.\n{{Entity footer}}"
        errs = verify_entity("Foo", get_page=lambda t: wt,
                             list_sources=lambda: ["Real"],
                             read_ledger=lambda t: "")
        self.assertTrue(any("no inline citation" in e for e in errs))

    def test_verify_entity_flags_missing_ledger(self):
        wt = "Foo did X<ref>{{Cite|Real|quote=x}}</ref>."
        errs = verify_entity("Foo", get_page=lambda t: wt,
                             list_sources=lambda: ["Real"],
                             read_ledger=lambda t: "")
        self.assertTrue(any("no claim ledger" in e for e in errs))

    def test_verify_entity_passes_a_clean_page(self):
        wt = ("Foo was founded in 1919<ref>{{Cite|Real|quote=launched in 1919}}</ref>.\n"
              "{{Relationship|predicate=acquired|object=Bar|sources=Real,Other|verification=ai-verified}}")
        ledger = ('| id | claim | quote | source page | url | tier | status | confidence |\n'
                  '|1|Founded 1919|"launched in 1919"|Real|u|T2|sourced|high|')
        errs = verify_entity("Foo", get_page=lambda t: wt,
                             list_sources=lambda: ["Real", "Other"],
                             read_ledger=lambda t: ledger)
        self.assertEqual(errs, [])

    # ---- missing_templates ------------------------------------------------
    # A template this wiki lacks renders as literal "Template:Foo" with NO
    # parser error, so nothing else in the pipeline notices it.

    def test_missing_templates_finds_a_redlinked_template(self):
        html = ('<p>the <i>Tyee</i><a href="/index.php?title=Template:%27&amp;action=edit'
                '&amp;redlink=1" class="new">Template:\'</a>s account</p>')
        self.assertEqual(missing_templates(html), ["'"])

    def test_missing_templates_ignores_existing_templates_and_other_redlinks(self):
        html = ('<a href="/index.php?title=Port_Alice&amp;action=edit&amp;redlink=1">Port Alice</a>'
                '<a href="/index.php/Template:Source">Template:Source</a>')
        self.assertEqual(missing_templates(html), [])

    def test_missing_templates_deduplicates_and_sorts(self):
        html = ('<a href="/index.php?title=Template:Zed&amp;redlink=1">z</a>'
                '<a href="/index.php?title=Template:Abc&amp;redlink=1">a</a>'
                '<a href="/index.php?title=Template:Zed&amp;redlink=1">z</a>')
        self.assertEqual(missing_templates(html), ["Abc", "Zed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
