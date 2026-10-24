# Horror Findings — Immersive Narrative Edition

Open **index.html** in your browser. The full reading experience and all story images are bundled into that file. `uploads/index.html` is an identical current copy.

## Content changes

- All 17 stories rewritten in natural Roman Hindi, approximately 9,800 words in total.
- Complete scenes, conversations, sensory details and emotional endings, primarily through a fictional first-person narrator.
- A short early disclosure and the existing “Sach kya hai?” box distinguish invented scenes, folklore and historical context.
- Three new AI illustrations: Ratnavati's perfume, Kuldhara's departure, and Nishi's doorway. Bhangarh has its existing cover plus two inline scenes; Kuldhara and Nishi have their existing covers plus one new inline scene each. Existing artwork remains included.
- Datiyana's location corrected to Hapur, Uttar Pradesh. Unsupported factual assertions and broken wording removed. Reading times recalculated at 150 words per minute for reflective reading.
- Existing CSS, layout, navigation, reader controls, typography and scripts preserved. Landing-page story summaries corrected as text only.

## Files and editing

- `site/stories.js`: final story content consumed by the site.
- `site/template.html`: original interface, with corrected descriptive copy.
- `site/build.py`: builds the standalone page, embedding images.
- `assets/`: original and new artwork.
- `editorial/narratives.txt`: readable manuscript for all stories.
- `editorial/apply_narratives.py`: converts the manuscript to story data, including factual notes and card copy.
- `editorial/original-stories.json`: original content snapshot retained for comparison, not loaded by the site.
- `editorial/SOURCES.md`: editorial references and limits.
- `editorial/IMAGE_PROMPTS.md`: briefs for the three newly generated images.

To rebuild after editing `site/stories.js`:

```bash
python3 site/build.py
```

For manuscript edits, run `python3 editorial/apply_narratives.py` first. After building, copy the root `index.html` to `uploads/index.html` if distributing both entry points.

The page's existing external fonts and video require internet; narrative content and image assets are embedded. The pre-existing browser narration button depends on installed browser/OS voices; Roman Hindi pronunciation varies.

## Original image credits

Bhangarh: Chainwit. / Wikimedia Commons, CC BY-SA 4.0. Kuldhara: Pinakpani / Wikimedia, CC BY 4.0. Shaniwar Wada: Dattatray Gavhane / Wikimedia, CC BY-SA 4.0. Credits supplied with the original project are retained. Other original images are labelled AI illustrations. The three new images are also AI illustrations, not historical photographs or paranormal evidence.
