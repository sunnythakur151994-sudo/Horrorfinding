#!/usr/bin/env python3
"""
Parse the "RESEARCH SPECIAL" pages (74-86) of
uploads/Raat_Ke_Us_Paar_60_Stories_With_Entity_Research.pdf
into site/data-research.js

Text stays verbatim. Only structure is added: chapters, their paragraphs, the
three tables (hand-mapped from the page blocks), and the 23 references with the
DOI/PubMed URL that the book itself links to.

Run: python3 tools/parse_research.py
"""
import json, pathlib, re
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "uploads" / "Raat_Ke_Us_Paar_60_Stories_With_Entity_Research.pdf"
OUT = ROOT / "site" / "data-research.js"

# page numbers are 1-based, as printed in the book
CHAPTERS = [
    (74, "intro", "", "Ek jaise encounters, alag duniya?", (0, 0)),
    (75, "c01", "01 / WORLDWIDE COMMON PATTERNS", "Ek ehsaas, kai naam", (265, 530)),
    (76, "c02", "02 / MATCH KO SAMJHNA", "\u201cSame\u201d ke chaar alag matlab", (168, 385)),
    (77, "c03", "03 / DMT STUDIES", "Entities par asal research kya hai?", (0, 0)),
    (78, "c04", "04 / VISUALS AUR PRESENCE", "Dimaag ek duniya kaise mehsoos karata hai?", (0, 0)),
    (79, "c05", "05 / \u201cDOOSRI ZINDAGI\u201d", "Kuch minute, lekin saalon ka ehsaas", (0, 0)),
    (80, "c06", "06 / BODY AUR DEATH", "Kya body ka DMT portal kholta hai?", (0, 0)),
    (81, "c07", "07 / DIMENSIONS AUR 2026 UPDATES", "Nayi research kahan tak pahunchi?", (0, 0)),
    (82, "c08", "08 / SHARED ENCOUNTER KA TEST", "Kaunsa evidence baat badal sakta hai?", (0, 0)),
    (83, "c09", "09 / EVIDENCE SUMMARY", "Abhi hum kya keh sakte hain?", (168, 505)),
]

# tables, verbatim from the pages (cells re-joined where the PDF merged columns)
TABLES = {
    "c01": {
        "head": ["Research context", "Common experience / interpretation", "Evidence ki had"],
        "rows": [
            ["Egypt aur Denmark [R7]",
             "Cairo aur Copenhagen samples mein sleep paralysis ki explanations compare hui. Egyptian general-population subgroup mein 48% ne Jinn ko explanation maana.",
             "Sample-specific belief; poore desh ka rate ya actual Jinn detection nahi."],
            ["Abruzzo, Italy [R8]",
             "Presence aur visual experiences mein local Pandafeche belief se milte witch/cat-like descriptions mile.",
             "Culture aur symptoms ka sambandh; cause ka complete proof nahi."],
            ["Khmer refugee clinical sample [R9]",
             "Sleep paralysis waale 42 participants mein 38 ne approaching being ki visual experience report ki.",
             "Trauma-affected clinical sample; general Cambodian population ka estimate nahi."],
            ["DMT reports [R1,R2]",
             "Guides, alien-like beings, deities, jesters aur insect-like forms jaise descriptions.",
             "Broad categories; ek hi individual being ki verified identity nahi."],
        ],
    },
    "c02": {
        "head": ["Daava", "Kya dikhana padega?"],
        "rows": [
            ["Milta-julta theme",
             "Do reports mein \u201ckoi presence thi\u201d ya \u201cguide mila\u201d jaise common motifs. Yeh documented hain."],
            ["Milta-julta visual",
             "Independent descriptions mein uncommon shape, rang, placement ya behaviour ka measurable overlap."],
            ["Wahi entity",
             "Matching rare details, independently recorded information aur alternative explanations ke controls. \u201cAlien\u201d kehna kaafi nahi."],
            ["Wahi waqt, alag desh",
             "Synchronized timestamps, contact-free reports, blind scoring aur repeated results. Purani memories ka baad mein match hona yeh test nahi hai."],
        ],
    },
    "c09": {
        "head": ["Sawaal", "Review ka jawab"],
        "rows": [
            ["Kya recurring patterns hain?",
             "Haan: presence, changed body/self, unusual visuals aur altered time jaise experiences documented hain."],
            ["Kya sab wahi beings dekhte hain?",
             "Nahi. Broad overlap ke saath substantial variety hai; selected reports ki frequency poori population par apply nahi hoti."],
            ["Kya same entity same time par verified hai?",
             "Is focused review mein replicated, controlled cross-location proof nahi mila."],
            ["Kya doosri zindagi ke saal prove hue?",
             "Time/identity distortion studied hai; literal alternate lifetime ki independent verification nahi mili."],
            ["Kya DMT afterlife ko prove karta hai?",
             "Nahi. Near-death questionnaire overlap doosre lok ya death mechanism ka proof nahi."],
            ["Kya dimensions par research hai?",
             "Haan, lekin physics dimensions, subjective realms aur speculative consciousness theories alag claims hain."],
            ["Kya sab kuch explain ho chuka hai?",
             "Nahi. Individual content aur full causal mechanisms par open questions hain; unknown ko external entity ka proof bhi nahi maana ja sakta."],
        ],
    },
}

DROP = re.compile(r"^(RAAT KE US PAAR|Research checked:|REFERENCES|Source directory|\d+\s*$)")


def blocks(page):
    out = []
    for b in page.get_text("blocks"):
        t = " ".join(b[4].split())
        if not t:
            continue
        out.append((b[1], b[0], t))
    return out


def parse_chapter(doc, page_no, cid, kicker, title, table_zone):
    page = doc[page_no - 1]
    bs = blocks(page)
    paras = []
    for y, x, t in bs:
        if DROP.match(t):
            continue
        if "Research Special" in t or "Research checked" in t:
            continue
        if kicker and t.lower() == kicker.lower():
            continue
        if t == title:
            continue
        if t.startswith("PAPERS /"):
            continue
        if table_zone[1] and table_zone[0] <= y <= table_zone[1]:
            continue
        if re.match(r"^\d\d\s*/", t):
            continue
        if t.upper().startswith("NAYA SECTION"):
            continue
        paras.append(t)
    return {"id": cid, "kicker": kicker, "title": title, "page": page_no,
            "paras": paras, "table": TABLES.get(cid)}


def parse_refs(doc):
    refs = []
    for pg in (83, 84, 85):          # 0-based pages 84,85,86
        links = [l["uri"] for l in doc[pg].get_links() if l.get("uri")]
        entries = [t for _, _, t in blocks(doc[pg]) if re.match(r"^R\d+\.", t)]
        for i, e in enumerate(entries):
            m = re.match(r"^(R\d+)\.\s*(.+?)\s*Read source\s*$", e)
            text = (m.group(2) if m else e)
            refs.append({"id": e.split(".")[0], "text": text,
                         "url": links[i] if i < len(links) else ""})
    return refs


def main():
    doc = pymupdf.open(PDF)
    chapters = [parse_chapter(doc, *c) for c in CHAPTERS]
    refs = parse_refs(doc)
    data = {
        "checked": "24 October 2026",
        "intro_title": "Ek jaise encounters, alag duniya?",
        "chapters": chapters,
        "references": refs,
    }
    js = ("/* RESEARCH SPECIAL — global patterns, DMT/entity/dimension research.\n"
          "   Text verbatim from the uploaded book (pages 74-86); structure from tools/parse_research.py */\n"
          "const RESEARCH = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    OUT.write_text(js, encoding="utf-8")
    for c in chapters:
        print(f"{c['id']:>4} p{c['page']}  paras={len(c['paras'])}  table={'yes' if c['table'] else 'no'}  {c['title'][:44]}")
    print("references:", len(refs))
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
