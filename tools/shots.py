#!/usr/bin/env python3
"""
Shot registry for the story galleries.

Every story can have up to 5 images ("shots"). They live in assets/ as
<id>-1.webp ... <id>-5.webp and are registered in site/shots.json:

    { "v-nuh-kuaan": [
        {"f":"v-nuh-kuaan-1.webp","cap":"Kuaan ka kinara, aadhi raat","credit":"AI ART"},
        ... ] }

site/build.py injects that map as `const SHOTS` and merges it into STORIES, so
the card uses shot 1, the reader shows the full strip, and Cinema mode walks
through all of them.

Usage
  python3 tools/shots.py add <story-id> <file1> [file2 ...]   # register (converts png->webp)
  python3 tools/shots.py list                                 # coverage report
  python3 tools/shots.py pending [--cat village]              # stories still without shots
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SHOTS = ROOT / "site" / "shots.json"
INDEX = ROOT / "editorial" / "stories-index.json"


def load():
    if SHOTS.exists():
        return json.loads(SHOTS.read_text(encoding="utf-8"))
    return {}


def save(d):
    SHOTS.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def to_webp(path: pathlib.Path) -> pathlib.Path:
    """Convert any png/jpg to webp next to it; return the webp path."""
    if path.suffix.lower() == ".webp":
        return path
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    out = path.with_suffix(".webp")
    im.save(out, "WEBP", quality=82, method=6)
    path.unlink()
    return out


def cmd_add(args):
    if len(args) < 2:
        sys.exit("usage: shots.py add <story-id> <file...>")
    sid, files = args[0], args[1:]
    d = load()
    entry = d.get(sid, [])
    for f in files:
        p = pathlib.Path(f)
        if not p.exists():
            p = ASSETS / f
        if not p.exists():
            sys.exit(f"missing file: {f}")
        w = to_webp(p)
        entry.append({"f": w.name, "cap": "", "credit": "AI ART"})
    d[sid] = entry
    save(d)
    print(f"{sid}: {len(entry)} shots")


def cmd_list():
    rows = json.loads(INDEX.read_text(encoding="utf-8"))
    d = load()
    done = [r for r in rows if r["id"] in d]
    print(f"stories with shots: {len(done)} / {len(rows)}   images: {sum(len(v) for v in d.values())}")
    by = {}
    for v in d.values():
        by[len(v)] = by.get(len(v), 0) + 1
    print("shot-count histogram:", dict(sorted(by.items())))
    for r in rows:
        if r["id"] in d:
            print(f"  {r['no']:>5}  {r['id']:<28} {len(d[r['id']])} shots")


def cmd_pending(args):
    cat = None
    if "--cat" in args:
        cat = args[args.index("--cat") + 1]
    rows = json.loads(INDEX.read_text(encoding="utf-8"))
    d = load()
    for r in rows:
        if cat and r["cat"] != cat:
            continue
        if r["id"] not in d:
            print(f"{r['no']:>5}  {r['id']:<28} {r['title']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        cmd_add(sys.argv[2:])
    elif cmd == "list":
        cmd_list()
    elif cmd == "pending":
        cmd_pending(sys.argv[2:])
    else:
        sys.exit(__doc__)
