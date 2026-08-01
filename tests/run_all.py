#!/usr/bin/env python3
"""Run every test module. Exit non-zero if any fail.

Also runs the differential harnesses (verify_differential.py,
webarchive_differential.py, prose_differential.py). These are deliberately
plain scripts, not unittest.TestCase modules -- unittest's discover(pattern=
"test_*.py") never picks them up, so on their own they are invisible to CI.
They earn their keep, though: each loads the ORIGINAL pre-refactor script
from /dossiers/_skillset/forestwiki-research/scripts/ by file path (unmodified)
and diffs its behaviour against the new research_core/research_mediawiki code, which a unittest
case asserting fixed expected values cannot do. So they run here explicitly,
as subprocesses (each already has its own pass/fail via sys.exit), gated on
whether the specific original file each one depends on is actually present --
this repo's tests must stay green on a checkout with no /dossiers volume
mounted at all.
"""
import os
import re
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "template"))

DIFFERENTIAL_HARNESSES = [
    "verify_differential.py",
    "webarchive_differential.py",
    "prose_differential.py",
]


def _original_path_of(harness):
    """Extract the ORIGINAL_PATH constant from a harness's source, without
    importing it -- importing is exactly what we must not do before knowing
    the path exists, since two of the three call load_original(...) at
    module scope and would raise FileNotFoundError on import alone.
    """
    with open(os.path.join(HERE, harness), encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r'ORIGINAL_PATH\s*=\s*"([^"]+)"', text)
    if not m:
        raise RuntimeError("%s has no ORIGINAL_PATH constant to gate on" % harness)
    return m.group(1)


def run_differential_harnesses():
    """Run each harness in DIFFERENTIAL_HARNESSES if its /dossiers original is
    present, otherwise print a loud, specific skip reason. Returns True iff
    every harness that actually ran passed (a harness that was skipped does
    not count against the result).
    """
    all_ok = True
    print("\n" + "=" * 70)
    print("Differential harnesses (compare new code against /dossiers originals)")
    print("=" * 70)
    for harness in DIFFERENTIAL_HARNESSES:
        if not os.path.isfile(os.path.join(HERE, harness)):
            print("\n[SKIP] %s -- harness script not carried into this repo "
                  "(differential harnesses stayed with the source repo)" % harness)
            continue
        original = _original_path_of(harness)
        if not os.path.isfile(original):
            print("\n[SKIP] %s -- original not found at %s "
                  "(no /dossiers volume mounted, or skillset not checked out here)"
                  % (harness, original))
            continue
        print("\n[RUN] %s (original: %s)" % (harness, original))
        proc = subprocess.run([sys.executable, os.path.join(HERE, harness)],
                               cwd=ROOT)
        if proc.returncode != 0:
            print("[FAIL] %s exited %d" % (harness, proc.returncode))
            all_ok = False
        else:
            print("[OK] %s" % harness)
    return all_ok


def main():
    loader = unittest.TestLoader()
    suite = loader.discover(HERE, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    differential_ok = run_differential_harnesses()

    return 0 if (result.wasSuccessful() and differential_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
