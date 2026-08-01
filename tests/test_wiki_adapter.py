#!/usr/bin/env python3
"""Tests for wiki.py response parsing tolerance.

Stdlib unittest (no pytest in the ForestWiki container; PEP-668 blocks pip).
Run: python3 tests/test_wiki_adapter.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))
from research_mediawiki.wiki import parse_response


class TestParseResponse(unittest.TestCase):
    def test_parse_response_tolerates_trailing_bytes(self):
        # The "Extra data" bug hit on multi-relationship pages: MediaWiki
        # occasionally appends whitespace/HTML comments after the JSON body.
        raw = '{"edit":{"result":"Success"}}\n\n<!--x-->'
        self.assertEqual(parse_response(raw)["edit"]["result"], "Success")

    def test_parse_response_plain_json(self):
        self.assertEqual(parse_response('{"a":1}'), {"a": 1})

    def test_parse_response_tolerates_leading_whitespace(self):
        self.assertEqual(parse_response('\n  {"a":1}'), {"a": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
