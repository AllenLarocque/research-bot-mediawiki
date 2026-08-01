#!/usr/bin/env python3
"""Tests for research_mediawiki.weakcites_cli's profile threading.

weakcites_cli.main() calls page_sentences(wt) and (before this fix) never
loaded a domain profile at all, so a domain's abbreviations vocabulary could
never reach the sentence splitter for this CLI.

research_mediawiki.profileload.PROFILE is a load-once-at-import singleton
(see profileload.py's own docstring), resolved from the RESEARCH_PROFILE env
var. It must be set to a profile.toml carrying "Twp." BEFORE the first import
of research_mediawiki.profileload anywhere in this process -- so that env var
is set at module scope here, before weakcites_cli (which will import
profileload once fixed) is imported. tests/test_apply_adapter.py needs the
same singleton and writes byte-identical profile content for the same reason,
so whichever of the two test modules imports profileload first "wins" the
race harmlessly.

wiki.py talks to a real MediaWiki over the network; ensure_login/list_category/
get are monkeypatched directly on the already-imported wiki module (weakcites_cli
imports wiki as a module object, so wiki.get etc. are looked up at call time --
a plain attribute monkeypatch, restored in tearDown, is enough; no mocking
framework needed).
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))

with tempfile.TemporaryDirectory() as _profile_dir:
    _profile_path = os.path.join(_profile_dir, "profile.toml")
    with open(_profile_path, "w") as _fh:
        _fh.write('name = "x"\nabbreviations = ["Twp."]\n')
    os.environ.setdefault("RESEARCH_PROFILE", _profile_path)
    # profileload reads and closes this file during the import below; the
    # directory is not needed once these two imports return, so it is
    # cleaned up (by the `with` above) before any test method runs.
    from research_mediawiki import weakcites_cli
    from research_mediawiki import wiki


class TestMainThreadsProfileToPageSentences(unittest.TestCase):
    TITLE = "Test Entity"
    # A quote with no words in common with either half of the claim, so
    # is_weak flags it regardless of how the sentence gets split -- the
    # thing under test is WHICH text gets printed as the claim, not whether
    # it gets flagged.
    WIKITEXT = ('The township office building sits in Twp. It closed for '
                'good in 1975.<ref>{{Cite|Src|quote=completely unrelated '
                'archival material}}</ref>')

    def setUp(self):
        self._orig_ensure_login = wiki.ensure_login
        self._orig_list_category = wiki.list_category
        self._orig_get = wiki.get
        wiki.ensure_login = lambda: None
        wiki.list_category = (
            lambda cat: [self.TITLE] if cat == "Category:Entities" else [])
        wiki.get = lambda t: self.WIKITEXT
        self.addCleanup(setattr, wiki, "ensure_login", self._orig_ensure_login)
        self.addCleanup(setattr, wiki, "list_category", self._orig_list_category)
        self.addCleanup(setattr, wiki, "get", self._orig_get)

    def _run(self):
        old_argv = sys.argv
        sys.argv = ["weakcites_cli.py"]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                weakcites_cli.main()
        finally:
            sys.argv = old_argv
        return buf.getvalue()

    def test_the_profile_naming_twp_keeps_the_claim_sentence_whole(self):
        out = self._run()
        self.assertIn(
            "The township office building sits in Twp. It closed for good "
            "in 1975.", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
