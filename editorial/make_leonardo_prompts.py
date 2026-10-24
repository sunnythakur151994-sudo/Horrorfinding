#!/usr/bin/env python3
"""
Generate a paste-ready Leonardo AI prompt for EVERY story.

Leonardo AI is not connected to this environment (no API key / connector), so
this script gives you the exact prompts to run there. Drop the downloaded
images into assets/ with the suggested filename, add "art": "<file>" to that
story object, and run site/build.py — the site picks it up automatically
(cards, reader hero and the in-page Cinema mode all use the same image).

    node tools/dump_index.js                   # metadata from the built site
    python3 editorial/make_leonardo_prompts.py ->  editorial/LEONARDO_PROMPTS.md
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "editorial" / "stories-index.json"
OUT = ROOT / "editorial" / "LEONARDO_PROMPTS.md"

STYLE = ("cinematic Indian folk-horror still, 35mm film grain, night scene, low-key amber "
         "lantern light and deep teal shadows, humid haze, no text, no watermark, no gore, "
         "no visible mutilation, painterly photoreal")

SCENE = {
    "village": "a rural Indian village at night — mud walls, bamboo fence, one lit window",
    "ancient": "a mythic Indian temple tableau — carved stone, oil lamps, storm sky",
    "case": "a real Indian heritage building at night — arches, scaffolding, single torch beam",
    "heritage": "a well-known Indian monument at dusk — sandstone ruins, mist, birds in flight",
    "tantra": "a dark ritual site in rural India seen from outside the circle — old banyan roots, "
              "a clay oil lamp, red thread knots, scattered coins, no people, no symbols",
}

CAT_TITLE = {
    "village": "Gaon ki ghatnayein",
    "ancient": "Puraani kahaniyan",
    "case": "Case files",
    "heritage": "Heritage files",
    "tantra": "Kala jadu · puraana tantra",
}


def load():
    if not INDEX.exists():
        raise SystemExit("Run `node tools/dump_index.js` first.")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def main():
    rows = load()
    lines = [
        "# Leonardo AI prompt pack — Horror Findings Around India",
        "",
        "Leonardo AI is **not** connected to this workspace, so these are copy-paste prompts.",
        "Workflow: Leonardo → *Image Generation* → model **Leonardo Phoenix** or **Vision XL**,",
        "aspect ratio **16:9**, style *Cinematic*; generate, download, rename exactly as shown,",
        "place in `assets/`, then add `art: \"<file>\"` to that story object and run",
        "`node tools/dump_index.js && python3 site/build.py`.",
        "",
        f"Total stories: **{len(rows)}** — one prompt each.",
        "",
    ]
    cur = None
    for r in rows:
        cat = r["cat"]
        if cat != cur:
            label = CAT_TITLE.get(cat, cat)
            count = sum(1 for x in rows if x["cat"] == cat)
            lines += ["", f"## {label} ({count})", ""]
            cur = cat
        fname = r["art"] if r["art"].endswith((".webp", ".png", ".jpg")) else r["id"] + "-leonardo.webp"
        prompt = (
            f"{r['title']}. {r['card']} Scene: {SCENE.get(cat, SCENE['heritage'])}. "
            f"Location feel: {r['regionLabel'] or 'India'} ({r['era']}). {STYLE}."
        )
        lines += [
            f"### {r['no']} · {r['id']} — {r['title']}",
            f"- **File name:** `assets/{fname}`",
            f"- **Prompt:** {prompt}",
            "",
        ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT, len(rows), "prompts")


if __name__ == "__main__":
    main()
