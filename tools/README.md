# Media pipeline — narration audio + story films

Sab kuch `ffmpeg` (bundled via `imageio-ffmpeg`, no system install) aur is repo ke tools se banta hai.

```
story text ─► audio/scripts.json ─► generate_speech ─► audio/parts/<id>/partN.mp3
                                                   └─► audio/<id>.mp3      (concat)
audio/<id>.mp3 + assets/<art>.webp ─► tools/make_films.py ─► video/<id>.mp4
                                                          └─► audio/manifest.json
```

## 1. Scripts nikaalna

```bash
node tools/extract_scripts.js        # audio/scripts.json (122 stories, clean narration text)
```
(sirf HTML tags hataata hai — text waisa hi rehta hai jaisa site par hai)

## 2. Narration banana

- Har story ke liye ek hi file: `audio/<id>.mp3`.
- 1,500 characters per TTS call ki limit hai, isliye lambi kahaniyon ko `audio/parts/<id>/partN.txt`
  mein toड़ा jaata hai (`tools/split_script.js`), phir `concat_audio()` se joda jaata hai.
- Abhi ready: **bhangarh** (4 min 38 s) aur **nishi** (3 min 03 s) — dono full narration, verdict ke saath.

```bash
python3 - <<'PY'
import sys, pathlib, json; sys.path.insert(0,'tools')
from media import concat_audio
parts = sorted(pathlib.Path('audio/parts/bhangarh').glob('part*.mp3'), key=lambda p:int(p.stem[4:]))
concat_audio(parts, 'audio/bhangarh.mp3')
PY
```

## 3. Film render

```bash
python3 tools/make_films.py bhangarh nishi     # ya: koi bhi id jiska audio/<id>.mp3 ho
```

Kya hota hai:
- 1280×720, 25 fps, H.264 + AAC (MP4, `+faststart`)
- artwork par dheema ken-burns push, vignette, film grain, fog
- **silent opening title card** (render ki gayi PNG — is build mein `drawtext` filter available nahi tha)
- film ki lambai = narration ki lambai (audio ke saath perfectly synced)
- render ke baad `audio/manifest.json` apne aap update: `{"audio": {...}, "films": {...}}`

Rebuild page:

```bash
python3 site/build.py     # manifest padh kar const AUDIO + const FILMS inject karta hai
```

## 4. Page par kya hota hai

| Layer | Kahan | Kis par | Kis par nahi |
|---|---|---|---|
| **Studio narration** (`audio/<id>.mp3`) | reader → 🔊 Suniye | 2 stories | baaki 120 → browser voice |
| **Story film** (`video/<id>.mp4`) | reader hero → ▶ *Kahani ki film dekhein* | 2 stories | jahan film nahi, wahan Cinema mode |
| **Cinema mode** (in-page, koi file nahi) | reader → 🎬 | **saari 122 stories** | — |
| **Browser voice narration** | reader → 🔊 | saari 122 stories (voice install ho to) | jahan voice nahi, wahan text |

Agar `audio/` ya `video/` folder saath nahi hai (jaise sandboxed preview mein), page
automatically browser voice aur in-page Cinema mode par switch ho jaata hai — kuch tootta nahi.

## 5. Scale karna (baaki 120 stories)

1. `tools/split_script.js` se sabke parts banao (`audio/parts/`).
2. Parts ko TTS se generate karo — is environment mein **per turn 10 clips** ki limit hai,
   isliye 120 stories (~217 minutes audio) kai turns mein banengi.
3. `tools/make_films.py` (bina argument) har ready `audio/*.mp4` ka film render karta hai
   (~1–2 min per 4-minute film is machine par).


## shots.py — 5-image galleries

Registry lives in `site/shots.json`.

```
python3 tools/shots.py add v-nuh-kuaan assets/v-nuh-kuaan-1.png assets/v-nuh-kuaan-2.png
python3 tools/shots.py list
python3 tools/shots.py pending --cat village
```

`add` converts PNG/JPG to WebP (max 1600px, q82) and appends entries; captions are edited
directly in `site/shots.json`. Then `python3 site/build.py`.

Note: image generation is capped at 10 images per turn, and the site inlines every image,
so galleries are filled in batches (hero first, then shots 2–5).

## parse_book.py / make_site.py — book edition

```
python3 tools/parse_book.py    # uploads/*.pdf -> site/data-book.js, site/data-gaurav.js, assets/book|gaurav
python3 tools/make_site.py     # template surgery: nav, hero, 9 zone sections, Gaurav section (run once)
python3 site/build.py
```

`parse_book.py` reads the PDFs with PyMuPDF (`pip install pymupdf`), joins text **blocks** (not
lines, so wrapped paragraphs stay whole), splits each story page into: title / location / image
caption / body / `JAANCH MEIN KYA MILA?` / `Sources`, and extracts the page image to
`assets/book/kNN.webp`. Credits come from the book's credits pages (`credits[N]`), so every card
says either `ASLI TASVEER · author · license` or `AI ILLUSTRATION`.

`make_site.py` is destructive but re-runnable: it rebuilds the hero, nav, `#types`, the 9
`#zone-*` sections and `#gaurav` from the data files. Older story data lives in `site/archive/`.
