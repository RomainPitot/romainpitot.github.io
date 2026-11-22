"""Generates proto/*.html (unlisted design prototypes) from tools/protos/*.html,
injecting the real project data in place of __DATA__."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import build

data = [{"id": p["id"], "title": p["title"], "year": p["year"], "cat": p["category"], "status": p["status"],
         "desc": p["shortDesc"], "cover": "../assets/img/projects/" + build.project_cover_src(p),
         "tech": p["technologies"][:3]} for p in build.PROJECTS]
blob = json.dumps(data, ensure_ascii=False)
os.makedirs(os.path.join(ROOT, "proto"), exist_ok=True)
src = os.path.join(HERE, "protos")
for f in sorted(os.listdir(src)):
    t = open(os.path.join(src, f), encoding="utf-8").read().replace("__DATA__", blob)
    open(os.path.join(ROOT, "proto", f), "w", encoding="utf-8", newline="\n").write(t)
    print("wrote proto/" + f)
