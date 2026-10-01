#!/usr/bin/env python3
"""
OmniTech Arena -- load one game into a CTFd server through the CTFd API.

Adds challenges, flags, hints, tags, files and unlock requirements. Nothing that
is already on the server is deleted, so games can be added one at a time.

  1. In CTFd (as admin): Settings -> Access Tokens -> Generate.
  2. pip install requests
  3. python tools/deploy.py tracks/<track>/<game-folder> --url http://localhost:8000 --token ctfd_xxx

The game folder must contain challenges.json and a files/ folder.
Run it ONCE per game -- running it twice creates duplicate challenges.
Add --hidden to load a game hidden and reveal it later in Admin -> Challenges.
"""
import argparse, json, os, sys
import requests


def main():
    ap = argparse.ArgumentParser(description="Load an OmniTech Arena game into CTFd")
    ap.add_argument("game", nargs="?", default=os.path.dirname(os.path.abspath(__file__)),
                    help="Path to the game folder (contains challenges.json and files/)")
    ap.add_argument("--url", required=True, help="Base URL of your CTFd, e.g. http://localhost:8000")
    ap.add_argument("--token", required=True, help="Admin access token from CTFd Settings -> Access Tokens")
    ap.add_argument("--hidden", action="store_true", help="Create challenges hidden (reveal them later)")
    a = ap.parse_args()

    game = os.path.abspath(a.game)
    cj = os.path.join(game, "challenges.json")
    if not os.path.exists(cj):
        sys.exit(f"No challenges.json in {game}")

    base = a.url.rstrip("/") + "/api/v1"
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {a.token}"})

    def api(method, path, **kw):
        if "json" in kw:
            kw.setdefault("headers", {})["Content-Type"] = "application/json"
        r = s.request(method, base + path, **kw)
        if not r.ok:
            sys.exit(f"ERROR {method} {path}: {r.status_code} {r.text[:300]}")
        return r.json().get("data")

    challenges = json.load(open(cj))
    ids = {}
    for c in challenges:
        body = {"name": c["name"], "category": c["category"], "description": c["description"],
                "value": c["value"], "type": "standard", "state": "hidden" if a.hidden else "visible"}
        if c.get("max_attempts"):
            body["max_attempts"] = c["max_attempts"]
        cid = api("POST", "/challenges", json=body)["id"]
        ids[c["name"]] = cid
        for ftype, content, data in c["flags"]:
            api("POST", "/flags", json={"challenge": cid, "type": ftype, "content": content, "data": data})
        for content, cost in c.get("hints", []):
            api("POST", "/hints", json={"challenge": cid, "content": content, "cost": cost})
        for t in c.get("tags", []):
            api("POST", "/tags", json={"challenge": cid, "value": t})
        for fn in c.get("files", []):
            with open(os.path.join(game, "files", fn), "rb") as fh:
                api("POST", "/files", files={"file": (fn, fh)}, data={"challenge": cid, "type": "challenge"})
        print(f"  + {c['category']:<46} {c['name']}")
    for c in challenges:
        if c.get("requires"):
            api("PATCH", f"/challenges/{ids[c['name']]}",
                json={"requirements": {"prerequisites": [ids[n] for n in c["requires"]]}})
    print(f"\nDone: {len(challenges)} challenges loaded.")


if __name__ == "__main__":
    main()
