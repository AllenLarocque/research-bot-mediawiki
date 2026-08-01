#!/usr/bin/env python3
"""Resolve the domain profile for wiki-side CLI entry points.

Loaded once at import. A missing profile raises rather than falling back to
general defaults: running domain research with no domain vocabulary produces
plausible wrong answers instead of an error.
"""
import os

from core.scripts.profile import load

_HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROFILE = load(os.environ.get("RESEARCH_PROFILE",
                              os.path.join(_HERE, "profile.toml")))
