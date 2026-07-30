#!/usr/bin/env python3
"""Minimal MediaWiki bot client (stdlib only) for the ForestWiki research agent.

Stdlib only by design: the ForestWiki container has no `requests` and PEP-668
blocks pip installs.

Environment:
  MW_API                       e.g. http://mediawiki/api.php
  MW_RESEARCH_BOT_USER         bot account name (the "@research" suffix is added)
  MW_RESEARCH_BOT_APP_PASS     bot application password
  MW_COOKIE_JAR                optional; defaults to ~/.forestwiki_cookies.txt

Env is read lazily so this module can be imported (and its pure helpers tested)
without credentials present.
"""
import os
import sys
import json
import urllib.parse
import urllib.request
import http.cookiejar

DEFAULT_COOKIES = os.path.expanduser("~/.forestwiki_cookies.txt")

_opener = None
_cj = None


def _api():
    api = os.environ.get("MW_API")
    if not api:
        raise RuntimeError("MW_API is not set")
    return api


def _creds():
    user = os.environ.get("MW_RESEARCH_BOT_USER")
    pw = os.environ.get("MW_RESEARCH_BOT_APP_PASS")
    if not user or not pw:
        raise RuntimeError("MW_RESEARCH_BOT_USER / MW_RESEARCH_BOT_APP_PASS are not set")
    return user + "@research", pw


def _get_opener():
    global _opener, _cj
    if _opener is None:
        _cj = http.cookiejar.MozillaCookieJar(os.environ.get("MW_COOKIE_JAR", DEFAULT_COOKIES))
        try:
            _cj.load(ignore_discard=True)
        except Exception:
            pass
        _opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))
        _opener.addheaders = [("User-Agent", "ForestWiki-Claude-Researcher/1.0")]
    return _opener


def parse_response(raw: str) -> dict:
    """Tolerant JSON parse.

    MediaWiki sometimes appends trailing bytes (whitespace, HTML comments,
    debug output) after the JSON body, which makes json.loads raise
    "Extra data". raw_decode reads the first complete JSON value and ignores
    whatever follows.
    """
    return json.JSONDecoder().raw_decode(raw.lstrip())[0]


def _req(params, post=None):
    params = {**params, "format": "json"}
    url = _api() + "?" + urllib.parse.urlencode(params)
    data = urllib.parse.urlencode(post).encode() if post else None
    with _get_opener().open(urllib.request.Request(url, data=data), timeout=30) as r:
        raw = r.read().decode("utf-8", "replace")
    return parse_response(raw)


def is_logged_in():
    r = _req({"action": "query", "meta": "userinfo"})
    return r.get("query", {}).get("userinfo", {}).get("id", 0) != 0


def login():
    user, pw = _creds()
    t = _req({"action": "query", "meta": "tokens", "type": "login"})
    lt = t["query"]["tokens"]["logintoken"]
    r = _req({"action": "login"}, {"lgname": user, "lgpassword": pw, "lgtoken": lt})
    if r.get("login", {}).get("result") != "Success":
        raise RuntimeError("LOGIN FAILED: " + json.dumps(r))
    _cj.save(ignore_discard=True)
    return r


def ensure_login():
    """Idempotent: reuses an existing bot-password session rather than re-logging in."""
    if is_logged_in():
        return
    login()


def csrf():
    return _req({"action": "query", "meta": "tokens"})["query"]["tokens"]["csrftoken"]


def get(page):
    """Return page wikitext, or None if the page does not exist."""
    r = _req({"action": "parse", "page": page, "prop": "wikitext"})
    if "error" in r:
        return None
    return r["parse"]["wikitext"]["*"]


def exists(page):
    return get(page) is not None


def edit(page, text, summary):
    """Edit a page. Always tagged ai-contributed; never sets the bot flag."""
    tok = csrf()
    return _req({"action": "edit"}, {
        "title": page,
        "text": text,
        "summary": summary,
        "tags": "ai-contributed",
        "token": tok,
    })


def purge(page):
    """Force a re-parse. Needed before trusting Cargo-backed output (Cargo lag)."""
    return _req({"action": "purge", "titles": page}, post={})


def render(page):
    """Return rendered html, categories and any template/parser error markers."""
    r = _req({"action": "parse", "page": page, "prop": "text|categories"})
    if "error" in r:
        return {"error": r["error"]}
    html = r["parse"]["text"]["*"]
    low = html.lower()
    markers = [m for m in ("cargo-error", "scribunto-error", 'strong class="error"',
                           "cite_error", "cite error") if m in low]
    return {
        "categories": [c["*"] for c in r["parse"].get("categories", [])],
        "error_markers": markers,
        "html": html,
    }


def parse_text(wikitext, title="Sandbox"):
    """Render arbitrary wikitext without saving it (for template render-checks)."""
    r = _req({"action": "parse", "text": wikitext, "title": title,
              "contentmodel": "wikitext", "prop": "text|categories"})
    if "error" in r:
        return {"error": r["error"]}
    return {
        "html": r["parse"]["text"]["*"],
        "categories": [c["*"] for c in r["parse"].get("categories", [])],
    }


def list_category(cat):
    """All page titles in a category, following continuation."""
    out, cont = [], None
    while True:
        p = {"action": "query", "list": "categorymembers",
             "cmtitle": cat, "cmlimit": "500"}
        if cont:
            p["cmcontinue"] = cont
        r = _req(p)
        out += [m["title"] for m in r["query"]["categorymembers"]]
        cont = r.get("continue", {}).get("cmcontinue")
        if not cont:
            return out


def _main():
    cmd = sys.argv[1]
    if cmd == "login":
        print(json.dumps(login().get("login")))
    elif cmd == "get":
        print(get(sys.argv[2]))
    elif cmd == "edit":
        ensure_login()
        with open(sys.argv[3]) as f:
            text = f.read()
        summary = sys.argv[4] if len(sys.argv) > 4 else \
            "Create/update page (AI-drafted, awaiting verification)"
        print(json.dumps(edit(sys.argv[2], text, summary)))
    elif cmd == "render":
        r = render(sys.argv[2])
        r.pop("html", None)
        print(json.dumps(r, indent=2))
    elif cmd == "exists":
        print("YES" if exists(sys.argv[2]) else "NO")
    elif cmd == "category":
        for t in list_category(sys.argv[2]):
            print(t)
    else:
        print("usage: wiki.py {login|get|edit|render|exists|category} ...", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    _main()
