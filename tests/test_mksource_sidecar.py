#!/usr/bin/env python3
"""Tests for the snapshot sidecar mksource writes beside each capture.

The sidecar is the only record of which URL produced a snapshot. Without it,
research_core.citecheck cannot tell an exactly-attributed quote from a
misattributed one, and falls back to comparing domains — which cannot see a
swap between two pages on the same host.

mksource.main fetches over the network, exits on a short page and writes into
the dossier tree, so the sidecar lives in its own function and is tested here
directly.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "template"))
from research_mediawiki.mksource import write_sidecar


class TestWriteSidecar(unittest.TestCase):
    URL = "https://example.org/gazette-1911"
    BODY = b"<html><body><p>the depot opened in 1913</p></body></html>"

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        self.snap = os.path.join(self.dir, "gazette_1911.html")
        with open(self.snap, "wb") as fh:
            fh.write(self.BODY)

    def read(self):
        with open(self.snap + ".meta.json", encoding="utf-8") as fh:
            return json.load(fh)

    def test_writes_beside_the_snapshot(self):
        path = write_sidecar(self.snap, self.URL, "Fairview Gazette 1911")
        self.assertEqual(path, self.snap + ".meta.json")
        self.assertTrue(os.path.isfile(path))

    def test_records_the_url_and_title(self):
        write_sidecar(self.snap, self.URL, "Fairview Gazette 1911")
        meta = self.read()
        self.assertEqual(meta["url"], self.URL)
        self.assertEqual(meta["title"], "Fairview Gazette 1911")

    def test_hash_is_of_the_snapshot_as_written(self):
        write_sidecar(self.snap, self.URL, "t")
        self.assertEqual(self.read()["sha256"],
                         hashlib.sha256(self.BODY).hexdigest())

    def test_hash_changes_when_the_snapshot_does(self):
        # The point of recording it: a capture edited after the fact no longer
        # matches its own record.
        write_sidecar(self.snap, self.URL, "t")
        before = self.read()["sha256"]
        with open(self.snap, "ab") as fh:
            fh.write(b"<!-- tampered -->")
        write_sidecar(self.snap, self.URL, "t")
        self.assertNotEqual(before, self.read()["sha256"])

    def test_fetched_at_is_iso_8601_utc(self):
        write_sidecar(self.snap, self.URL, "t")
        stamp = self.read()["fetched_at"]
        self.assertTrue(stamp.endswith("Z"), stamp)
        self.assertRegex(stamp, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_an_explicit_timestamp_is_used_verbatim(self):
        write_sidecar(self.snap, self.URL, "t", fetched_at="2026-08-01T00:00:00Z")
        self.assertEqual(self.read()["fetched_at"], "2026-08-01T00:00:00Z")

    def test_a_missing_snapshot_raises_rather_than_writing_a_hashless_record(self):
        with self.assertRaises(OSError):
            write_sidecar(os.path.join(self.dir, "absent.html"), self.URL, "t")


if __name__ == "__main__":
    unittest.main()
