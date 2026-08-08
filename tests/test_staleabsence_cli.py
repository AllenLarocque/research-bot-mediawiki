#!/usr/bin/env python3
"""Wikitext-side tests for the stale-absence probe.

The claim-finding and the name heuristic are tested in the template repo against
research_core.staleabsence, which is not allowed to know what a wikilink is.
What is tested here is the part that does: pulling link targets out of a
sentence, which are a better answer than any capitalisation guess.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))

try:
    from research_core.staleabsence import expired
    from research_mediawiki.retro import wikilinks
    from research_mediawiki.staleabsence_cli import (
        claims_on, names_in_sentence, regions,
    )
    HAVE_STALEABSENCE = True
except ImportError as exc:
    # Only a PINNED dependency earns a skip. This repo's suite runs against its
    # own template pin, so a research_core module that landed after that pin
    # genuinely cannot be imported until someone bumps it -- that is a stale
    # pin, not a broken adapter.
    #
    # research_mediawiki is this repo's own code. Missing that is a bug here,
    # and swallowing it would let a module nobody wrote pass as a pin problem.
    # The first draft of this guard did exactly that and reported nine skips
    # for code that did not exist.
    if "research_core" not in str(exc):
        raise
    HAVE_STALEABSENCE = False

NEEDS_PIN_BUMP = unittest.skipUnless(
    HAVE_STALEABSENCE,
    "needs research_core.staleabsence: bump the adapters/wiki/template pin")


@NEEDS_PIN_BUMP
class TestWikilinks(unittest.TestCase):

    def test_a_plain_link(self):
        self.assertEqual(wikilinks("see [[Great Sayward Fire]] for the fire"),
                         ["Great Sayward Fire"])

    def test_a_piped_link_yields_the_target_not_the_label(self):
        # The label is what a reader sees; the target is what exists or does not.
        self.assertEqual(wikilinks("[[Port Alberni|the town]]"), ["Port Alberni"])

    def test_several_links_in_order_without_duplicates(self):
        self.assertEqual(wikilinks("[[A page]] and [[B page]] and [[A page]]"),
                         ["A page", "B page"])

    def test_a_section_anchor_is_dropped(self):
        self.assertEqual(wikilinks("[[Crofton mill#History]]"), ["Crofton mill"])

    def test_text_with_no_links(self):
        self.assertEqual(wikilinks("no links at all here"), [])


@NEEDS_PIN_BUMP
class TestNamesInSentence(unittest.TestCase):
    """What the CLI hands core as extra_names."""

    def test_supplies_link_targets(self):
        got = names_in_sentence("Campbell River",
                                "The [[Great Sayward Fire]] has no page here.")
        self.assertIn("Great Sayward Fire", got)

    def test_never_offers_the_page_itself(self):
        # A page always exists, so listing its own title would report every
        # absence claim on every page as expired.
        got = names_in_sentence("Campbell River",
                                "[[Campbell River]] and [[Sayward]] have no pages here.")
        self.assertNotIn("Campbell River", got)
        self.assertIn("Sayward", got)


@NEEDS_PIN_BUMP
class TestRegions(unittest.TestCase):
    """Which stretches of a page get looked at."""

    PAGE = ("{{AI-contributed}}\n{{Person|name=Robert Sommers}}\n"
            "He was a minister who went to prison.\n"
            "{{Relationship|predicate=held_office|object=BC"
            "|note=The Workers' Unity League has no page here.}}\n"
            "\nWick Gray and David Sturdy have no pages here.\n"
            "{{Entity footer}}")

    def test_narrative_prose_is_covered(self):
        self.assertTrue(any("went to prison" in r
                            for r in regions("Robert Sommers", self.PAGE)))

    def test_a_row_note_is_covered(self):
        self.assertTrue(any("Workers' Unity League" in r
                            for r in regions("Robert Sommers", self.PAGE)))

    def test_prose_BELOW_the_relationship_rows_is_covered(self):
        # narrative_span stops at the first {{Relationship}}, so page_sentences
        # cannot see this line -- and a real claim lived there, unnoticed, on
        # Robert Sommers: "Wick Gray, David Sturdy and Judge Arthur Lord have
        # no pages here." Prose below the rows is still page surface.
        self.assertTrue(any("Wick Gray" in r
                            for r in regions("Robert Sommers", self.PAGE)),
                        "prose after the relationship rows was not looked at")

    def test_template_calls_are_not_offered_as_prose(self):
        self.assertFalse(any(r.strip().startswith("{{Entity footer")
                             for r in regions("Robert Sommers", self.PAGE)))

    def test_every_claim_on_the_page_is_found_once(self):
        found = claims_on("Robert Sommers", self.PAGE)
        self.assertEqual(len(found), 2, [c.sentence for c in found])


@NEEDS_PIN_BUMP
class TestEndToEnd(unittest.TestCase):
    """The join, with a stubbed existence check -- no network."""

    PAGE = ("The fire burned 300 square kilometres in 1938. "
            "The [[Great Sayward Fire]] has no page here, a red link.")

    def test_reports_a_claim_whose_link_target_now_exists(self):
        got = expired({"Campbell River": self.PAGE},
                      {"Great Sayward Fire"},
                      extra_names=names_in_sentence)
        self.assertEqual(len(got), 1)
        title, claim, live = got[0]
        self.assertEqual(title, "Campbell River")
        self.assertEqual(live, ["Great Sayward Fire"])

    def test_says_nothing_while_the_claim_is_still_true(self):
        self.assertEqual(
            expired({"Campbell River": self.PAGE}, set(),
                    extra_names=names_in_sentence),
            [])


if __name__ == "__main__":
    unittest.main()
