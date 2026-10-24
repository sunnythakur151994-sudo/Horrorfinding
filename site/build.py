#!/usr/bin/env python3
"""
Build script for HORROR FINDINGS AROUND INDIA.

Reads  site/template.html + site/stories.js
Inlines every {{IMG:file.webp}} as a base64 data URI
Writes /home/user/index.html  (single self-contained file, works offline)

Usage:  python3 site/build.py
"""
import base64, io, json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
TEMPLATE = ROOT / "site" / "template.html"
STORIES = ROOT / "site" / "stories.js"
DATA = [ROOT / "site" / n for n in ("data-book.js", "data-gaurav.js")]
OUT = ROOT / "index.html"

MAX_W = 1200
QUALITY = 78


def encode(name: str, max_w: int = MAX_W, quality: int = QUALITY) -> str:
    path = ASSETS / name
    if not path.exists():
        sys.exit(f"Missing asset: {path}")
    raw = path.read_bytes()
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=quality, method=6)
        raw = buf.getvalue()
        mime = "image/webp"
    except ImportError:
        mime = "image/webp"
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    stories = "\n".join(f.read_text(encoding="utf-8") for f in DATA)

    def sub(match):
        return encode(match.group(1))

    # ---- per-story image galleries (assets/<id>-N.webp, registered in site/shots.json) ----
    shots_file = ROOT / "site" / "shots.json"
    shots = {}
    if shots_file.exists():
        raw = json.loads(shots_file.read_text(encoding="utf-8"))
        for sid, arr in raw.items():
            keep = [x for x in arr if (ASSETS / x["f"]).exists()]
            if keep:
                shots[sid] = keep
    shots_js = "const SHOTS = " + json.dumps(shots, ensure_ascii=False) + ";\n"

    # every image the page can possibly show
    names = set(re.findall(r"\{\{IMG:([^}]+)\}\}", html + stories))
    names |= {n for n in re.findall(r'"([A-Za-z0-9_./\-]+\.(?:webp|png|jpg|jpeg))"', stories)
              if (ASSETS / n).exists()}
    names |= set(re.findall(r'"([a-z0-9\-]+\.webp)"', html))
    names |= {x["f"] for arr in shots.values() for x in arr}

    html = re.sub(r"\{\{IMG:([^}]+)\}\}", sub, html)
    # stories keep {{IMG:..}} markers; they are resolved at runtime from the IMG map,
    # which avoids duplicating megabytes of base64 inside story bodies.

    # page weight: the hero (shot 1) gets full size, gallery shots 2-5 stay light
    def size_for(name: str):
        if name.startswith("book/"):
            return 800, 58
        if name.startswith("gaurav/"):
            return 1000, 78
        stem = name.rsplit(".", 1)[0]
        if stem.rsplit("-", 1)[-1].isdigit() and not stem.endswith("-1"):
            return 640, 60
        return MAX_W, QUALITY

    img_map = "const IMG = {\n" + ",\n".join(
        '  ' + repr(n).replace("'", '"') + ': ' + repr(encode(n, *size_for(n))) for n in sorted(names)
    ) + "\n};\n"

    merge = r"""
/* ---- assemble: one category per region cluster, numbering + art from the book ---- */
const STORIES = (function(){
  var out = [];
  var cl = (typeof BOOK_CLUSTERS !== "undefined") ? BOOK_CLUSTERS : [];
  var byKey = {};
  cl.forEach(function(c){ byKey[c.key] = c; });
  BOOK.forEach(function(s){
    var c = byKey[s.zone] || {label:s.zoneLabel || s.zone, blurb:""};
    s.cat = s.zone;
    s.zoneLabel = c.label;
    s.regionLabel = s.regionLabel || s.location || "";
    s.art = s.art || s.img;
    s.tag = "RAAT KE US PAAR";
    var raw = s.body || "";
    var words = raw.replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
    s.words = words;
    s.read = Math.max(2, Math.round(words / 140)) + " min";
    s.idx = out.length;
    out.push(s);
  });
  return out;
})();
"""

    # ---- pre-rendered narration (audio/) and films (video/) --------------
    # Files stay as real files on disk (keeps index.html light). The page plays
    # them from ./audio and ./video, and falls back to the browser voice or the
    # animated in-page film when a file is missing (e.g. inside a sandboxed preview).

    audio_json = ROOT / "audio" / "manifest.json"
    audio_js = "const AUDIO = {};\nconst FILMS = {};\n"
    imgdata_js = ""
    if audio_json.exists():
        data = json.loads(audio_json.read_text(encoding="utf-8"))
        audio_js = ("const AUDIO = " + json.dumps(data.get("audio", {}), ensure_ascii=False) + ";\n"
                    + "const FILMS = " + json.dumps(data.get("films", {}), ensure_ascii=False) + ";\n")

    bundle = img_map + audio_js + shots_js + imgdata_js + stories + merge
    html = html.replace('<script src="stories.js"></script>', "<script>\n" + bundle + "\n</script>")

    leftovers = re.findall(r"\{\{IMG:[^}]+\}\}", html)
    # story bodies legitimately keep the markers (resolved at runtime); only the
    # static markup must be fully substituted.
    static_left = [m for m in leftovers if m not in bundle]
    if static_left:
        sys.exit(f"Unreplaced image placeholders in markup: {static_left}")

    OUT.write_text(html, encoding="utf-8")
    size = OUT.stat().st_size / (1024 * 1024)
    print(f"Built {OUT}  ({size:.2f} MB)")


if __name__ == "__main__":
    main()
