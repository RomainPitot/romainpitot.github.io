"""Local editor for the portfolio (no dependency, localhost only).

    python tools/editor.py          then open http://localhost:8780

Edit project texts, links, challenges, retrospectives and images in a form.
Changes are saved to content/overrides.json (merged by build.py), the site is
rebuilt on demand, and "Publish" commits and pushes to GitHub Pages.
The to-do panel lists what is still missing (challenge, retrospective, real
screenshot) so nothing is forgotten.
"""
import base64
import http.server
import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
OVERRIDES = os.path.join(ROOT, "content", "overrides.json")
IMG_DIR = os.path.join(ROOT, "assets", "img", "projects")
PORT = 8780

EDITABLE = ["title", "shortDesc", "description", "role", "status", "year", "duration", "teamSize",
            "note", "highlights", "keySystems", "technologies", "links", "challenges", "retro",
            "facts", "image", "gallery"]


def load_build():
    """Fresh import of build.py so each call sees the latest overrides."""
    for m in ("build", "content_extra"):
        sys.modules.pop(m, None)
    import build
    return build


def read_overrides():
    if os.path.exists(OVERRIDES):
        with open(OVERRIDES, encoding="utf-8") as f:
            return json.load(f)
    return {"projects": {}}


def write_overrides(data):
    os.makedirs(os.path.dirname(OVERRIDES), exist_ok=True)
    with open(OVERRIDES, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def projects_payload():
    b = load_build()
    out = []
    for p in b.PROJECTS:
        item = {k: p.get(k) for k in EDITABLE}
        item["id"] = p["id"]
        item["category"] = p["category"]
        item["challenges"] = [list(c) for c in (p.get("challenges") or [])]
        item["facts"] = [list(c) for c in (p.get("facts") or [])]
        item["retro"] = p.get("retro") or {"constraint": "", "built": "", "redo": ""}
        item["links"] = p.get("links") or {}
        item["gallery"] = p.get("gallery") or []
        item["cover"] = b.project_cover_src(p)
        item["todo"] = [t for t, bad in (
            ("Add a technical challenge", not p.get("challenges")),
            ("Add the jam retrospective", p["category"] == "Game Jam" and not p.get("retro")),
            ("Add a real screenshot (cover is generated)", not p.get("image")),
        ) if bad]
        out.append(item)
    return out


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout + r.stderr).strip(), r.returncode


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/editor"):
            with open(os.path.join(HERE, "editor.html"), "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/projects":
            self._json(projects_payload())
        elif path == "/api/status":
            out, _ = run(["git", "status", "--short"])
            self._json({"changes": out})
        else:
            super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        try:
            data = self._body()
            if path == "/api/save":
                pid = data["id"]
                clean = {k: v for k, v in data["fields"].items() if k in EDITABLE}
                ov = read_overrides()
                ov.setdefault("projects", {}).setdefault(pid, {}).update(clean)
                write_overrides(ov)
                self._json({"ok": True})
            elif path == "/api/upload":
                name = re.sub(r"[^a-z0-9._-]", "-", data["name"].lower())
                if not re.search(r"\.(jpg|jpeg|png|webp)$", name):
                    raise ValueError("Only jpg, png or webp images")
                raw = base64.b64decode(data["data"].split(",")[-1])
                if len(raw) > 4_000_000:
                    raise ValueError("Image is over 4 MB: shrink it first")
                os.makedirs(IMG_DIR, exist_ok=True)
                with open(os.path.join(IMG_DIR, name), "wb") as f:
                    f.write(raw)
                self._json({"ok": True, "name": name})
            elif path == "/api/build":
                out, code = run([sys.executable, os.path.join(HERE, "build.py")])
                self._json({"ok": code == 0, "log": out[-1500:]})
            elif path == "/api/publish":
                msg = (data.get("message") or "content: edits from the editor").strip()
                run([sys.executable, os.path.join(HERE, "build.py")])
                branch, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
                run(["git", "add", "-A"])
                out1, c1 = run(["git", "commit", "-m", msg])
                out2, c2 = run(["git", "push", "origin", branch])
                self._json({"ok": c2 == 0, "log": ("%s\n%s" % (out1, out2))[-1500:], "branch": branch})
            else:
                self._json({"ok": False, "error": "unknown route"}, 404)
        except Exception as e:  # report to the UI instead of dying silently
            self._json({"ok": False, "error": str(e)}, 400)


if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("Editor: http://localhost:%d   (Ctrl+C to stop)" % PORT)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
