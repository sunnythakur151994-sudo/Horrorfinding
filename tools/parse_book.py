#!/usr/bin/env python3
"""
Parse the two uploaded PDFs into the site's data files.

  uploads/Raat_Ke_Us_Paar_60_Horror_Stories_Under_10MB.pdf  -> site/data-book.js
  uploads/Gaurav_Tiwari_Zindagi_Aur_Tahqiqaat.pdf           -> site/data-gaurav.js
  images                                                    -> assets/book/*.webp, assets/gaurav/*.webp

Book text is copied verbatim (Roman Hindi); only structure is added (<p>, <h3>,
verdict = "JAANCH MEIN KYA MILA?", sources). Nothing is rewritten.
"""
import json, pathlib, re
import pymupdf
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
UP = ROOT / "uploads"
BOOK_PDF = UP / "Raat_Ke_Us_Paar_60_Horror_Stories_Under_10MB.pdf"
GT_PDF = UP / "Gaurav_Tiwari_Zindagi_Aur_Tahqiqaat.pdf"

CLUSTERS = [
    (1, 12, "india", "Bharat", "India ki jagahen — Rajasthan se Assam tak"),
    (13, 17, "japan", "Japan", "Japan ki kahaniyan aur kaidan"),
    (18, 24, "seasia", "Asia–Pacific", "Thailand, Malaysia, Indonesia, Singapore, Philippines"),
    (25, 33, "britain", "Britain aur Ireland", "England, Scotland aur Ireland ke purane ghar"),
    (34, 38, "europe", "Europe", "Germany, Italy, Romania, France, Spain"),
    (39, 50, "namerica", "North America", "USA aur Canada"),
    (51, 55, "latam", "Latin America", "Mexico, Venezuela, Colombia"),
    (56, 57, "africa", "Africa", "Cape Town aur Southern Africa"),
    (58, 60, "oceania", "Oceania", "Australia aur New Zealand"),
]


def cluster_of(n):
    for a, b, key, label, blurb in CLUSTERS:
        if a <= n <= b:
            return key, label, blurb
    raise ValueError(n)


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def webp(src_bytes, out_path, max_w=900, q=74):
    import io
    im = Image.open(io.BytesIO(src_bytes)).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, "WEBP", quality=q, method=6)
    return out_path


def parse_credits(doc):
    """credits pages: 'NN. Title' + 'Photo / archival image | Author | LICENSE' | 'AI illustration | ...'"""
    text = "\n".join(doc[i].get_text() for i in range(65, doc.page_count))
    creds = {}
    for m in re.finditer(r"^(\d\d)\.\s+(.+?)\n(Photo / archival image|AI illustration)\s*\|\s*(.+?)\n", text, re.M):
        n = int(m.group(1))
        kind = m.group(3)
        rest = m.group(4).strip()
        parts = [p.strip() for p in rest.split("|")]
        creds[n] = {"kind": kind, "author": parts[0], "license": parts[1] if len(parts) > 1 else ""}
    return creds


def parse_book():
    doc = pymupdf.open(BOOK_PDF)
    creds = parse_credits(doc)
    assets = ROOT / "assets" / "book"
    stories = []
    for pg in range(5, 65):
        page = doc[pg]
        lines = [" ".join(b[4].split()) for b in page.get_text("blocks") if b[4].strip()]
        n = pg - 4
        # strip running head / page number
        head = lines[:3]
        lines = [l for l in lines
                 if l != "RAAT KE US PAAR" and "60 kahaniyan" not in l and l != str(pg + 1)]
        lines = [l for l in lines if not l.startswith("Tasveer ka source")]
        body_lines = [l for l in lines if not re.match(r"^KAHANI \d\d / 60$", l)]
        title = body_lines[0]
        rest = body_lines[1:]
        # location = first line that looks like a place (has a comma or country)
        location = rest[0]
        rest = rest[1:]
        # image caption (label of the photo / illustration)
        cap = ""
        if rest and re.search(r"(photo|illustration|artwork|image)", rest[0], re.I) and len(rest[0]) < 200:
            cap = rest.pop(0)
        # split body / jaanch / sources
        try:
            j = next(i for i, l in enumerate(rest) if l.startswith("JAANCH MEIN KYA MILA"))
        except StopIteration:
            j = len(rest)
        body = rest[:j]
        tail = rest[j + 1:]
        note, sources = [], []
        for l in tail:
            if l.startswith("Source ") or l.startswith("Tasveer ka source"):
                if l.startswith("Source "):
                    sources.append(re.sub(r"^Source \d+:\s*", "", l))
            else:
                note.append(l)
        # subheads inside body: short line without a closing full stop
        paras = []
        for l in body:
            if len(l) < 70 and not l.endswith((".", "!", "?", "”")) and len(l.split()) <= 9:
                paras.append(("h", l))
            else:
                paras.append(("p", l))
        # image
        imgs = page.get_images(full=True)
        img_name = f"book/k{n:02d}.webp"
        if imgs:
            info = doc.extract_image(imgs[0][0])
            webp(info["image"], ROOT / "assets" / img_name)
        c = creds.get(n, {"kind": "Photo / archival image", "author": "", "license": ""})
        is_ai = c["kind"].startswith("AI")
        credit = ("AI ILLUSTRATION · " + c["author"]) if is_ai else ("ASLI TASVEER · " + c["author"] + (" · " + c["license"] if c["license"] else ""))
        card = re.sub(r"\s+", " ", body[0] if body else title)
        if len(card) > 165:
            card = card[:162].rsplit(" ", 1)[0] + "…"
        html_body = []
        for kind, txt in paras:
            esc = (txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            if kind == "h":
                html_body.append(f"<h3>{esc}</h3>")
            else:
                html_body.append(f"<p>{esc}</p>")
        if html_body:
            html_body[0] = html_body[0].replace("<p>", '<p class="lead">', 1)
        zone, zlabel, _ = cluster_of(n)
        stories.append({
            "id": f"k{n:02d}",
            "no": f"{n:02d}",
            "title": title,
            "location": location,
            "regionLabel": location,
            "zone": zone,
            "zoneLabel": zlabel,
            "card": card,
            "era": f"KAHANI {n:02d} / 60",
            "img": img_name,
            "imgAlt": cap or title,
            "label": credit,
            "credit": credit,
            "isAI": is_ai,
            "body": "\n".join(html_body) if html_body else "<p>—</p>",
            "verdict": "<strong>JAANCH MEIN KYA MILA?</strong> " + " ".join(
                t.replace("&", "&amp;").replace("<", "&lt;") for t in note),
            "sources": sources,
        })
        print(f"  {n:02d} {title} | {len(body)} paras | {len(note)} note lines | {len(sources)} sources | {credit[:40]}")
    return stories


GAURAV_CHAPTERS = [
    ("g-01", "Shuruaat", "Florida se India", "03"),
    ("g-02", "India, 2009 ke baad", "Darr ke ghar tak pahunchna", "04"),
    ("g-03", "Bhangarh", "Jahaan darr ko jawaab nahi mila", "05"),
    ("g-04", "Unke apne bataaye kisse", "Kuldhara aur Mumbai", "06"),
    ("g-05", "Camera ke saath duniya", "Australia tak pahunchta safar", "07"),
    ("g-06", "Old Geelong Gaol", "Tasveer mein khada kaun tha?", "08"),
    ("g-07", "Geelong ka doosra pehlu", "Har recording Gaurav ki nahi thi", "09"),
    ("g-08", "Australia ki case trail", "Aradale aur saat aur darwaaze", "10"),
    ("g-09", "July 2016", "Aakhri din: khabar aur afwaah", "11"),
    ("g-10", "Jo bach gaya", "Kaam, yaadein aur tasveeron ka record", "12"),
]


def parse_gaurav():
    doc = pymupdf.open(GT_PDF)
    images = {}
    for pg in range(doc.page_count):
        key = {0: "hero", 6: "cast", 7: "geelong", 8: "kitchen"}.get(pg)
        if not key:
            continue
        ims = doc[pg].get_images(full=True)
        if not ims:
            continue
        info = doc.extract_image(ims[0][0])
        name = f"gaurav/{key}.webp"
        webp(info["image"], ROOT / "assets" / name, max_w=1000, q=80)
        images[key] = name

    chapters = []
    for cid, kicker, title, page_no in GAURAV_CHAPTERS:
        pg = int(page_no) - 1
        page = doc[pg]
        lines = [" ".join(b[4].split()) for b in page.get_text("blocks") if b[4].strip()]
        lines = [l for l in lines
                 if l != "GAURAV TIWARI / RESEARCH NARRATIVE" and "Public-source edition" not in l]
        while lines and (re.match(r"^\d\d$", lines[0]) or re.match(r"^\d\d\s*/\s*", lines[0])):
            lines.pop(0)
        # drop everything up to and including the exact title line
        try:
            ti = lines.index(title)
            lines = lines[ti + 1:]
        except ValueError:
            pass
        # subtitle line (location / date line), then the image caption line
        sub = ""
        if lines and len(lines[0]) < 60 and not lines[0].endswith("."):
            sub = lines.pop(0)
        elif lines and len(lines[0]) < 90 and not lines[0].endswith("."):
            lines.pop(0)          # short header fragment; chapter subtitle is used instead
        imgcap = ""
        meta = re.compile(r"(Source|Photographer|caption|Photo|published|capture attribution|published still|published group image)")
        while lines and len(lines[0]) < 300 and meta.search(lines[0]) and not lines[0].endswith((",", "aur", "ke")):
            imgcap = (imgcap + " " + lines.pop(0)).strip()
        paras, notes, sources = [], [], []
        for l in lines:
            if l.startswith("SOURCE LINKS"):
                sources = [s2.strip() for s2 in l.replace("SOURCE LINKS /", "").split("  ") if s2.strip()]
                continue
            if re.match(r"^(Record ka nateeja|Date note|Book note|Research boundary|Original image dekhein|Ek zaroori distinction|Note):", l):
                notes.append(l)
            else:
                paras.append(l)
        chapters.append({"id": cid, "kicker": kicker, "title": title,
                         "sub": (sub if sub and len(sub) < 60 else ""),
                         "imgcap": imgcap, "paras": paras, "notes": notes,
                         "sources": sources,
                         "img": images.get({3: "hero", 7: "cast", 8: "geelong", 9: "kitchen"}.get(int(page_no), ""))})
        print(f"  GT {cid} {title} | {len(paras)} paras | {len(notes)} notes | sub={sub[:40]}")
    return chapters, images


def write(book, gt):
    out = ["/* RAAT KE US PAAR — 60 kahaniyan. Text verbatim from the uploaded book; structure added in tools/parse_book.py */",
           "const BOOK = " + json.dumps(book, ensure_ascii=False, indent=1) + ";",
           "const BOOK_CLUSTERS = " + json.dumps([
               {"key": k, "label": lab, "blurb": bl} for _, _, k, lab, bl in CLUSTERS], ensure_ascii=False) + ";"]
    (ROOT / "site" / "data-book.js").write_text("\n".join(out), encoding="utf-8")
    g = ["/* GAURAV TIWARI — research narrative, text verbatim from the uploaded PDF */",
         "const GAURAV = " + json.dumps(gt, ensure_ascii=False, indent=1) + ";"]
    (ROOT / "site" / "data-gaurav.js").write_text("\n".join(g), encoding="utf-8")
    print("wrote data-book.js and data-gaurav.js")


if __name__ == "__main__":
    print("book:")
    book = parse_book()
    print("gaurav:")
    gt, images = parse_gaurav()
    write(book, gt)
