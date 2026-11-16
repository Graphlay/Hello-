#!/usr/bin/env python3
"""Search and download free sound effects and music for edits.

Sources
  openverse  Openverse (api.openverse.org) - CC-licensed audio, no key needed.
  freesound  Freesound (freesound.org)     - needs a free API key in FREESOUND_API_KEY
                                              (get one at https://freesound.org/apiv2/apply).

Examples
  python3 tools/sfx.py search whoosh                      # SFX from Openverse
  python3 tools/sfx.py search "lofi chill" --music        # music from Openverse
  python3 tools/sfx.py search whoosh --source freesound
  python3 tools/sfx.py download openverse:<id>            # saves to assets/sfx/
  python3 tools/sfx.py download freesound:<id> --music    # saves to assets/music/

Every download is logged to assets/<sfx|music>/licenses.md with title, author,
licence and source link, so attribution is always on hand.
Results default to licences that allow commercial use.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "ai-video-workspace/1.0"
OPENVERSE = "https://api.openverse.org/v1/audio/"
FREESOUND = "https://freesound.org/apiv2/"


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def freesound_headers():
    key = os.environ.get("FREESOUND_API_KEY")
    # Without a key the request is still sent: a cloud proxy may inject the key itself.
    return {"Authorization": f"Token {key}"} if key else {}


# ---------- search ----------

def fs_license(url):
    parts = url.rstrip("/").split("/")
    if "creativecommons" not in url or len(parts) < 2:
        return url
    kind = parts[-2]
    return "CC0" if kind == "zero" else f"CC {kind.upper()} {parts[-1]}"


def search_openverse(q, music, n, any_license):
    params = {"q": q, "page_size": n, "category": "music" if music else "sound_effect"}
    if not any_license:
        params["license_type"] = "commercial"
    data = get_json(OPENVERSE + "?" + urllib.parse.urlencode(params))
    return [
        {
            "id": f"openverse:{r['id']}",
            "title": r.get("title") or "",
            "author": r.get("creator") or "",
            "license": f"CC {r.get('license', '').upper()} {r.get('license_version') or ''}".strip(),
            "duration": (r.get("duration") or 0) / 1000,
            "page": r.get("foreign_landing_url") or "",
        }
        for r in data.get("results", [])
    ]


def search_freesound(q, music, n, any_license):
    params = {
        "query": q,
        "page_size": n,
        "fields": "id,name,username,license,duration,url",
        "filter": "duration:[0 TO 600]" if music else "duration:[0 TO 30]",
    }
    if not any_license:
        params["filter"] += ' license:("Creative Commons 0" OR "Attribution")'
    data = get_json(FREESOUND + "search/text/?" + urllib.parse.urlencode(params), freesound_headers())
    return [
        {
            "id": f"freesound:{r['id']}",
            "title": r["name"],
            "author": r["username"],
            "license": fs_license(r["license"]),
            "duration": r.get("duration") or 0,
            "page": r["url"],
        }
        for r in data.get("results", [])
    ]


# ---------- download ----------

def details(item_id):
    src, _, ident = item_id.partition(":")
    if src == "openverse":
        r = get_json(OPENVERSE + urllib.parse.quote(ident) + "/")
        return {
            "url": r["url"], "ext": r.get("filetype") or "mp3", "title": r.get("title") or ident,
            "author": r.get("creator") or "unknown",
            "license": f"CC {r.get('license', '').upper()} {r.get('license_version') or ''}".strip(),
            "page": r.get("foreign_landing_url") or "", "attribution": r.get("attribution") or "",
        }
    if src == "freesound":
        r = get_json(FREESOUND + f"sounds/{urllib.parse.quote(ident)}/?fields=id,name,username,license,url,previews",
                     freesound_headers())
        return {
            "url": r["previews"]["preview-hq-mp3"], "ext": "mp3", "title": r["name"],
            "author": r["username"], "license": fs_license(r["license"]), "page": r["url"], "attribution": "",
        }
    sys.exit(f"Unknown id '{item_id}'. Use openverse:<id> or freesound:<id> from a search.")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50] or "audio"


def download(item_id, music, out_dir=None):
    d = details(item_id)
    folder = out_dir or os.path.join(ROOT, "assets", "music" if music else "sfx")
    os.makedirs(folder, exist_ok=True)
    src, _, ident = item_id.partition(":")
    path = os.path.join(folder, f"{slug(d['title'])}_{src}-{ident[:8]}.{d['ext'].lstrip('.')}")
    req = urllib.request.Request(d["url"], headers={"User-Agent": UA, **(freesound_headers() if src == "freesound" else {})})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    with open(os.path.join(folder, "licenses.md"), "a") as log:
        log.write(f"- **{os.path.basename(path)}** — \"{d['title']}\" by {d['author']} — {d['license']} — {d['page']}"
                  + (f"\n  - Attribution: {d['attribution']}" if d["attribution"] else "") + "\n")
    print(f"Saved {os.path.relpath(path, ROOT)}  ({d['license']}, by {d['author']})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="search for audio")
    s.add_argument("query")
    s.add_argument("--source", choices=["openverse", "freesound"], default="openverse")
    s.add_argument("--music", action="store_true", help="music instead of sound effects")
    s.add_argument("-n", type=int, default=10, help="number of results")
    s.add_argument("--any-license", action="store_true", help="include non-commercial licences")
    s.add_argument("--json", action="store_true")
    d = sub.add_parser("download", help="download by id from a search")
    d.add_argument("ids", nargs="+")
    d.add_argument("--music", action="store_true", help="save to assets/music instead of assets/sfx")
    d.add_argument("--out", help="custom output folder")
    a = p.parse_args()

    try:
        if a.cmd == "search":
            fn = search_openverse if a.source == "openverse" else search_freesound
            res = fn(a.query, a.music, a.n, a.any_license)
            if a.json:
                print(json.dumps(res, indent=2))
            elif not res:
                print("No results.")
            for r in [] if a.json else res:
                print(f"{r['id']:<50} {r['duration']:6.1f}s  {r['license']:<14} {r['title'][:40]} — {r['author'][:20]}")
        else:
            for i in a.ids:
                download(i, a.music, a.out)
    except urllib.error.HTTPError as e:
        hint = " (Freesound needs FREESOUND_API_KEY)" if e.code in (401, 403) and "freesound" in e.url else ""
        sys.exit(f"Error: {e.code} {e.reason} from {urllib.parse.urlparse(e.url).netloc}{hint}")
    except urllib.error.URLError as e:
        sys.exit(f"Error: could not reach the service ({e.reason}). "
                 "If you are in a cloud session, its network may be blocking this host.")


if __name__ == "__main__":
    main()
