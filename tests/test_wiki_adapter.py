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


class TestEditRequiresLoginAndFailsLoudly(unittest.TestCase):
    """edit() used to hand an error dict back to callers who only print it.

    Unauthenticated, csrf() returns MediaWiki's anonymous token — well-formed,
    accepted, then rejected at edit time. edit() returned the error object and
    nothing raised, so callers like mksource printed one line and carried on
    writing caches and manifests as though the page had been saved. An agent
    auditing the corpus on 2026-08-02 lost an edit this way and only noticed
    because the page did not change.
    """

    def setUp(self):
        from research_mediawiki import wiki
        self.wiki = wiki
        self.calls = []
        self._orig = (wiki.ensure_login, wiki.csrf, wiki._req)
        wiki.ensure_login = lambda: self.calls.append("ensure_login")
        wiki.csrf = lambda: (self.calls.append("csrf"), "TOKEN+\\")[1]
        self.addCleanup(self._restore)

    def _restore(self):
        self.wiki.ensure_login, self.wiki.csrf, self.wiki._req = self._orig

    def _reply(self, payload):
        def fake(params, post=None):
            self.calls.append("req:" + params.get("action", "?"))
            return payload
        self.wiki._req = fake

    def test_logs_in_before_asking_for_a_token(self):
        self._reply({"edit": {"result": "Success"}})
        self.wiki.edit("P", "t", "s")
        self.assertLess(self.calls.index("ensure_login"), self.calls.index("csrf"))

    def test_returns_the_response_on_success(self):
        self._reply({"edit": {"result": "Success"}})
        self.assertEqual(self.wiki.edit("P", "t", "s")["edit"]["result"], "Success")

    def test_raises_when_the_api_returns_an_error(self):
        self._reply({"error": {"code": "permissiondenied", "info": "no"}})
        with self.assertRaises(RuntimeError) as cm:
            self.wiki.edit("P", "t", "s")
        self.assertIn("permissiondenied", str(cm.exception))

    def test_raises_when_the_result_is_not_success(self):
        self._reply({"edit": {"result": "Failure"}})
        with self.assertRaises(RuntimeError):
            self.wiki.edit("P", "t", "s")

    def test_raises_on_a_response_with_no_edit_block_at_all(self):
        self._reply({})
        with self.assertRaises(RuntimeError):
            self.wiki.edit("P", "t", "s")
