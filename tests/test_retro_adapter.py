#!/usr/bin/env python3
"""Tests for research_mediawiki.retro.page_sentences's profile threading.

page_sentences(wt) parses the narrative region of a wiki page and splits it
into sentences via research_core.textutil.split_sentences, but (before this
fix) never passed a profile down to it, so a domain's abbreviations vocabulary
could never affect where a page's sentences break.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))

from research_mediawiki.retro import page_sentences
from research_core.profile import load


class TestPageSentencesUsesProfile(unittest.TestCase):
    """"Twp." (multi-letter, absent from the general base) is the one
    abbreviation whose effect on splitting is observable here -- see
    tests/test_textutil.py::TestSplitSentencesUsesProfile in the template repo
    for why H.R.-shaped abbreviations cannot demonstrate this seam."""

    WT = "The township office building sits in Twp. It closed for good in 1975."

    def test_general_profile_does_not_know_the_abbreviation(self):
        sents = page_sentences(self.WT)
        self.assertEqual(len(sents), 2)

    def test_a_profile_supplying_the_abbreviation_prevents_the_split(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "profile.toml")
            with open(path, "w") as fh:
                fh.write('name = "x"\nabbreviations = ["Twp."]\n')
            sents = page_sentences(self.WT, load(path))
            self.assertEqual(len(sents), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
