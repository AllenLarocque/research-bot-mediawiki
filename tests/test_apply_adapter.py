#!/usr/bin/env python3
"""Tests for research_mediawiki.apply's profile threading.

apply.py's main() calls page_sentences(wt) and (before this fix) never
loaded a domain profile, so a domain's abbreviations vocabulary could never
reach the sentence splitter that decides where sentence #N's boundary falls
-- which matters because inserts (refs, {{Inference}}, {{Unsourced}}) are
positioned at a sentence's END offset.

Two things make apply.py awkward to import directly:

  * `main()` is called unconditionally at module scope (no `if __name__ ==
    "__main__"` guard), so importing the module RUNS it -- sys.argv and every
    module-level side effect it triggers must be under control BEFORE the
    import statement executes, not after.
  * It calls research_mediawiki.wiki functions that hit a real MediaWiki
    over the network.

`--dry` in sys.argv (read into the module-level DRY constant at import time)
makes main() print the retrofitted wikitext and ledger and return BEFORE any
wiki.edit/purge/render or verify.* call, so only wiki.ensure_login,
wiki.list_category and wiki.get need stubbing -- done by swapping in a fake
research_mediawiki.wiki module (both in sys.modules and as the
research_mediawiki package's `.wiki` attribute, restored in tearDown, since
`from research_mediawiki import wiki` can resolve via either path depending
on what has already been imported elsewhere in this process) before
triggering the import.

research_mediawiki.profileload.PROFILE is a load-once-at-import singleton
resolved from RESEARCH_PROFILE; see tests/test_weakcites_cli_adapter.py for
why both this file and that one write byte-identical profile content.
"""
import contextlib
import importlib
import io
import json
import os
import shutil
import sys
import tempfile
import types
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "template"))

import research_mediawiki  # noqa: E402  (package object, for attribute juggling)
from research_core import paths as core_paths  # noqa: E402
from research_core import srccache  # noqa: E402

_UNSET = object()

TITLE = "Test Entity"
WT = "The township office building sits in Twp. It closed for good in 1975."


class TestMainThreadsProfileToPageSentences(unittest.TestCase):
    def setUp(self):
        self.profile_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.profile_dir)
        self.dossier_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dossier_dir)
        self.cache_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.cache_dir)
        self.spec_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.spec_dir)

        profile_path = os.path.join(self.profile_dir, "profile.toml")
        with open(profile_path, "w") as fh:
            fh.write('name = "x"\nabbreviations = ["Twp."]\n')
        os.environ.setdefault("RESEARCH_PROFILE", profile_path)

        with open(os.path.join(self.cache_dir, "manifest.json"), "w") as fh:
            fh.write("{}")

        spec = {"title": TITLE, "inference": [{"sent": 1, "note": "why"}]}
        self.spec_path = os.path.join(self.spec_dir, "spec.json")
        with open(self.spec_path, "w") as fh:
            json.dump(spec, fh)

    def _run(self):
        stub_wiki = types.ModuleType("research_mediawiki.wiki")
        stub_wiki.ensure_login = lambda: None
        stub_wiki.list_category = lambda cat: []
        stub_wiki.get = lambda t: WT

        orig_wiki_module = sys.modules.get("research_mediawiki.wiki", _UNSET)
        orig_wiki_attr = getattr(research_mediawiki, "wiki", _UNSET)
        orig_apply_module = sys.modules.get("research_mediawiki.apply", _UNSET)
        orig_dossiers = core_paths.DOSSIERS
        orig_cache = srccache.CACHE
        orig_argv = sys.argv

        sys.modules["research_mediawiki.wiki"] = stub_wiki
        research_mediawiki.wiki = stub_wiki
        sys.modules.pop("research_mediawiki.apply", None)
        core_paths.DOSSIERS = self.dossier_dir
        srccache.CACHE = self.cache_dir
        sys.argv = ["apply.py", self.spec_path, "--dry"]

        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                importlib.import_module("research_mediawiki.apply")
        finally:
            sys.argv = orig_argv
            srccache.CACHE = orig_cache
            core_paths.DOSSIERS = orig_dossiers
            sys.modules.pop("research_mediawiki.apply", None)
            if orig_apply_module is not _UNSET:
                sys.modules["research_mediawiki.apply"] = orig_apply_module
            if orig_wiki_module is _UNSET:
                sys.modules.pop("research_mediawiki.wiki", None)
            else:
                sys.modules["research_mediawiki.wiki"] = orig_wiki_module
            if orig_wiki_attr is _UNSET:
                if hasattr(research_mediawiki, "wiki"):
                    del research_mediawiki.wiki
            else:
                research_mediawiki.wiki = orig_wiki_attr
        return buf.getvalue()

    def test_profile_naming_twp_keeps_the_sentence_whole(self):
        # sents[1] is the {{Inference}} marker's insertion anchor (its end
        # offset, walked back past the terminating period). If "Twp." reaches
        # the splitter, sentence #1 is the WHOLE two-clause sentence and the
        # marker lands after "1975"; if not, sentence #1 is only the first
        # clause and the marker lands right after "Twp" instead.
        out = self._run()
        self.assertIn("1975{{Inference", out)
        self.assertNotIn("Twp{{Inference", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
