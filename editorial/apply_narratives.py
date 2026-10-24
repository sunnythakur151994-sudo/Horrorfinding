#!/usr/bin/env python3
"""
Convert the narrative manuscript into site/stories.js for the site.

Sources (in order):
  1. uploads/narratives.txt   — @@ id blocks  (markdown: paragraphs, ### headings, [IMAGE:..])
  2. uploads/stories.js       — fallback if narratives.txt is missing

Output: site/stories.js  (const STORIES = [ ... ])

Fix applied here: in the supplied manuscript, a "### Heading" line was merged
into the following paragraph (writer wrote "### Heading\nText" with no blank
line). This script splits them back into <h3>Heading</h3><p>Text</p>
instead of leaving the text inside the heading.

Usage: python3 editorial/apply_narratives.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_TXT = ROOT / "uploads" / "narratives.txt"
SRC_JS = ROOT / "uploads" / "stories.js"
OUT = ROOT / "site" / "stories.js"

DISCLOSURE = (
    "<p><em>Yeh lok-katha se prerit rachnatmak punarkathan hai. \u201cMain\u201d, "
    "samvaad aur vyaktigat drishya kalpanik hain; tathya aur seemaayein ant ke "
    "\u201cSach kya hai?\u201d mein hain.</em></p>"
)


def parse_manuscript(text: str) -> dict:
    """@@ id blocks -> {id: {'title': str|None, 'images': [...], 'body': html}}"""
    blocks = {}
    current = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("@@"):
            current = line[2:].strip()
            blocks[current] = {"body": [], "images": []}
            continue
        if current is None:
            continue

        img = re.match(r"^\[IMAGE:([^|\]]+)\|([^|\]]*)\|([^\]]*)\]$", line.strip())
        if img:
            src, alt, cap = (m.strip() for m in img.groups())
            blocks[current]["images"].append(src)
            blocks[current]["body"].append(
                '<figure><img src="{{IMG:%s}}" alt="%s" loading="lazy">'
                "<figcaption>%s</figcaption></figure>" % (src, esc(alt), esc(cap))
            )
            continue

        if not line.strip():
            continue

        if line.startswith("### "):
            blocks[current]["body"].append("<h3>%s</h3>" % esc(line[4:].strip()))
            continue

        blocks[current]["body"].append("<p>%s</p>" % esc(line.strip()))

    return blocks


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def first_paragraph_is_lead(html_parts):
    """Tag the opening paragraph as the lead (drop-cap in the reader)."""
    for i, part in enumerate(html_parts):
        if part.startswith("<p>"):
            html_parts[i] = part.replace("<p>", '<p class="lead">', 1)
            return


def build_from_manuscript(records):
    blocks = parse_manuscript(SRC_TXT.read_text(encoding="utf-8"))
    out = []
    for rec in records:
        b = blocks.get(rec["id"])
        if not b:
            out.append(rec)
            continue
        parts = [p for p in b["body"] if not p.startswith("<h3>") or "</h3>" in p]
        # insert the fictional-narration disclosure right after the opening paragraph
        lead_idx = next((i for i, p in enumerate(parts) if p.startswith("<p>")), None)
        if lead_idx is not None:
            parts.insert(lead_idx + 1, DISCLOSURE)
        first_paragraph_is_lead(parts)
        new = dict(rec)
        new["body"] = "\n".join(parts)
        out.append(new)
    return out


def main():
    if not SRC_JS.exists():
        sys.exit("Missing %s" % SRC_JS)
    raw = SRC_JS.read_text(encoding="utf-8")
    records = json.loads(raw[raw.index("["): raw.rindex("]") + 1])
    print("records from stories.js:", len(records))

    if SRC_TXT.exists():
        records = build_from_manuscript(records)
        print("manuscript applied:", SRC_TXT.name)
    else:
        print("manuscript missing — keeping stories.js bodies")

    # sanity: no heading may contain a paragraph
    bad = [r["id"] for r in records
           if any("\n" in m for m in re.findall(r"<h3>(.*?)</h3>", r["body"], re.S))]
    if bad:
        sys.exit("Merged heading/paragraph still present in: %s" % bad)

    js = ("/* Narrative edition: first-person scenes are fictional retellings. */\n"
          "const HERITAGE = " + json.dumps(records, ensure_ascii=False, indent=2) + ";\n")
    OUT.write_text(js, encoding="utf-8")
    words = sum(len(re.sub(r"<[^>]+>", " ", r["body"]).split()) for r in records)
    print("wrote %s — %d stories, %d words" % (OUT, len(records), words))


if __name__ == "__main__":
    main()
