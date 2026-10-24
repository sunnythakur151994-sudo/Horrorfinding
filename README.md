# RAAT KE US PAAR — 60 kahaniyan (site build)

**Deliverable:** `/home/user/index.html` — ek self-contained page (4.4 MB), book ki 60 kahaniyan +
alag Gaurav Tiwari section. Sab kuch inline hai: koi CDN nahi, koi redirect nahi.

Source of content: `uploads/Raat_Ke_Us_Paar_60_Horror_Stories_Under_10MB.pdf` aur
`uploads/Gaurav_Tiwari_Zindagi_Aur_Tahqiqaat.pdf`. **Text verbatim copy hai** — sirf structure
(`<p>`, headings, verdict box) add hua hai. Purani 137-kahaniyon wali archive `site/archive/` mein
rakhi hai (build mein use nahi hoti).

---

## Page ka dhaancha

| # | Section | Kya hai |
|---|---|---|
| — | Hero + notice | book ka title, "Darwaaza kholne se pehle" wali honesty note |
| — | `#types` | 9 kshetra tiles (auto counts) |
| — | `#bhangarh` | Kahani 01 feature (asli photo + credit) |
| 01–09 | `#zone-*` | 9 grid sections, cluster ke hisaab se |
| 10 | `#research` | **Research special** — book ke 9 chapters + site ke 6 naye chapters (`#more`), 3 tables, 46 sources |
| 10b | `#worldwide` / `#entity` / `#rs-refs` | usi section ke teen hisse (jump links) |
| 11 | `#gaurav` | **Gaurav Tiwari** — 10 chapters, 4 asli tasveerein, provenance box |
| 12 | `#video` | Monkey Man (kahani 07) ka archive footage, in-page player |
| 13 | `#sach` | 4 rules: kahani vs kagaz |

### Kshetra aur counts

| key | label | kahaniyan |
|---|---|---|
| `india` | Bharat | 12 (01–12) |
| `japan` | Japan | 5 (13–17) |
| `seasia` | Asia–Pacific | 7 (18–24) |
| `britain` | Britain aur Ireland | 9 (25–33) |
| `europe` | Europe | 5 (34–38) |
| `namerica` | North America | 12 (39–50) |
| `latam` | Latin America | 5 (51–55) |
| `africa` | Africa | 2 (56–57) |
| `oceania` | Oceania | 3 (58–60) |

### Reader (design same as pehle)

- card → reader: hero image, meta chips (kahani no / min / shabd), full text
- **JAANCH MEIN KYA MILA?** verdict box + `Sources:` line (book ki source list se)
- 🔊 Suniye (browser voice narration, sentence highlight, speed bar) · 🎬 Cinema mode (in-page film)
- card par credit: `ASLI TASVEER · <photographer> · <license>` ya `AI ILLUSTRATION`

---

## Files

```
index.html                 deliverable (build output)
site/template.html         CSS + markup + JS (design)
site/data-book.js          BOOK[60] + BOOK_CLUSTERS[9]  (verbatim book text)
site/data-gaurav.js        GAURAV[10] chapters (verbatim PDF text)
site/data-research.js      RESEARCH{intro, 9 chapters, 23 refs} — book pages 74-86 verbatim
site/build.py              template + data -> index.html, inlines images as data URIs
site/shots.json            (khali) extra-image galleries ke liye registry
site/archive/              purani 137-kahaniyon ki data files (build nahi hoti)
assets/book/k01..k60.webp  60 tasveerein (PDF se extract)
assets/gaurav/*.webp       4 published photos (hero, cast, geelong, kitchen)
assets/research/*.webp     4 AI illustrations for the research section (labelled)
tools/parse_book.py        PDF -> data-book.js / data-gaurav.js + image extraction
tools/parse_research.py    PDF pages 74-86 -> data-research.js (+ tables, refs with DOI)
tools/make_site.py         template surgery (nav, hero, 9 sections, gaurav section)
tools/dump_index.js        built site -> editorial/stories-index.json (metasearch)
tools/media.py, make_films.py, shots.py   narration/film/gallery helpers (optional)
uploads/                   original PDFs
```

## Rebuild

```
python3 tools/parse_book.py     # PDFs -> data files + images (idempotent)
python3 tools/parse_research.py # research special -> data-research.js
python3 tools/make_site.py      # sirf ek baar, jab template ka dhaancha badle
python3 site/build.py           # -> index.html
```

## Honesty rules jo site mein built-in hain

1. Book ka note har page par hai: ye 60 *verified* incidents ki list nahi.
2. Har kahani ke end mein **JAANCH MEIN KYA MILA?** + sources.
3. Image credit har card par; AI illustration saaf label.
4. Gaurav section: "public-source overview, official archive nahi"; koi AI photo nahi;
   July 2016 par police ke bayaan aur afwaah ka farq likha hua hai.
5. Video section mein boundary note: footage rumour ka record hai, creature ka proof nahi.

## Pending / optional

- **Narration audio:** book ki 60 kahaniyon ke liye studio MP3 abhi nahi hain (purani files
  `audio/` mein hain par wo hataye gaye text ki thi, isliye manifest khali kar diya). Browser voice
  chal rahi hai. Chahiye to `node tools/extract_scripts.js && node tools/split_script.js --all`
  se clip scripts ban jayenge, phir TTS 10 clips/turn ke hisaab se.
- **Films:** `video/*.mp4` purani narration ke hain — naye text ke liye regenerate karna hoga.
- **Extra images:** agar har kahani par 5 shots chahiye, `tools/shots.py` + `site/shots.json`
  wahi purana system hai (cap: 10 generated images per turn).


## Research special (new section)

Source: pages **74–86** of `uploads/Raat_Ke_Us_Paar_60_Stories_With_Entity_Research.pdf`
("RESEARCH SPECIAL / NAWA SECTION"). Text verbatim; only structure added.

Two halves, one section (`#research`):

- **Hissa 01 · `#worldwide`** — "Duniya bhar mein ek jaise kisse": sleep paralysis clusters
  (Cheyne), Egypt/Denmark Jinn (Jalal), Abruzzo Pandafeche, Khmer refugee sample (Hinton),
  DMT entity labels; plus the "same ke chaar alag matlab" table (theme / visual / wahi entity /
  wahi waqt) and the 5-step *shared-encounter test* (ch 08).
- **Hissa 02 · `#entity`** — DMT research (Davis 2020 n=2,561; Lawrence 2022 45.5% entity code;
  Michael 2021 interviews), mechanisms (Bressloff geometry, Timmermann 2023 EEG-fMRI, Blanke
  presence, Mago 2026 model), the "doosri zindagi" claims (Salvia vs DMT, Maqueda, MacLean,
  SOF-Q familiarity), endogenous DMT/pineal claims (Dean 2019, Nichols 2018, 5-MeO-DMT),
  dimensions + 2026 updates (DMTx, Sanders 14 Jul 2026, "Traces of the Other" preprint),
  and the evidence-summary table.
- **`#rs-refs`** — all 23 references with DOI/PubMed strings (shown as text; the site keeps its
  "no outbound links" rule).

Also added: a **live-check box** (24 Oct 2026) where the key numbers were re-verified against the
original papers (Davis 2020 percentages, Mago et al. 2026 niaf069, Jalal et al. 2014 48% Jinn),
and a **safety box**: DMT/Salvia are not truth detectors; India's NDPS Act applies.

Files: `toolbar`-free, all inline. Rebuild: `python3 tools/parse_research.py && python3 tools/make_site.py && python3 site/build.py`.


## Research special · Hissa 03 (site-written, added later)

`site/data-research2.js` — 6 chapters written for the site (**not** from the book), each with its own
source list (`tools/make_research_extra.py`):

| id | chapter | kya |
|---|---|---|
| e1 | "Teesra aadmi" | third man factor — Shackleton 1916, Smythe 1933, Messner 1970, Geiger 2009, Critchley 1955, Blanke 2014 robot induction, 2023 altitude-psychosis review (83% hallucinations, 54% felt presence) |
| e2 | Bina dawa ke bhi "entity" | hypoxia, sleep deprivation, hypothermia, CO poisoning, grief — same structure without any substance |
| e3 | DMT ka medical pehlu | Nature Medicine 2026 phase 2a (34 patients, MADRS −10.8 vs placebo, 3–6 months), vapour DMT TRD (14 patients, −21.14 at day 7), 2025 safety review; boundary: clinical ≠ recreational, entities never verified |
| e4 | India ka kanoon | NDPS Act 1985 s.22 — DMT small 0.1 g / commercial 2 g, saza 1 yr → 20 yr, s.37 bail bar; no religious exemption |
| e5 | Same entity, alag jagah | mass psychogenic illness: Monkey Man 2001 (51 reports, 67% during power cuts), Spring-heeled Jack, phantom slasher, phantom clowns; internet as shared template |
| e6 | India ka capsule | bhoot/pishach/yakshi vs DMT entity typology; cultural patterning (Mago 2026 mid-level priors); same structure, different cloth |

Rendering: `.rs-ch.rs-extra` cards with `.rs-chsrc` (source + URL displayed as text, not clickable —
the site keeps its "no outbound redirect" rule). Jump link `#more` in the research hero.
