# Shot plan — 5 images per story (next batches)

Rule set used for every story (so the gallery reads like a short film, not a wallpaper set):

| # | role | kya dikhta hai |
|---|------|----------------|
| 1 | **jagah** | establishing wide shot, raat, koi insaan nahi |
| 2 | **nishaan** | detail/close-up — rassi, sil, sikka, toota taala |
| 3 | **log** | insaan, aksar peeth se, torch/lantern light |
| 4 | **darr** | woh pal jiske liye kahani sunai jaati hai (no gore) |
| 5 | **sach** | subah ki roshni mein asli wajah — toota railing, khaali bangla, toota pipe |

Style tail (`STY`) — har prompt ke aakhir mein:
`Cinematic Indian folk-horror still, 16:9 widescreen, night, 35mm film grain, low-key amber lantern light, deep teal shadows, humid haze, painterly photoreal, no text, no watermark, no gore, no visible injury.`

Files: `assets/<id>-1.png … -5.png` → `python3 tools/shots.py add <id> assets/<id>-*.png`
→ captions in `site/shots.json` → `python3 site/build.py`.

---

## V-02 v-kaimur-ped — shot 4 (retry; 4/5 done)
- `v-kaimur-ped-4.png` — "Looking up into a banyan canopy at night: an empty jute rope loop hanging from a thick branch, swaying slightly, full moon behind the leaves, dry leaves falling, no body, no gore. STY"

## V-03 v-sundarbans-dokkhin — Dokkhin Rai ka jungle
1. `v-sundarbans-dokkhin-1.png` — "A narrow tidal creek in the Sundarbans mangrove forest at night, small wooden fishing boat with a kerosene lantern, black water, dense mangrove roots, heavy humidity haze. STY"
2. `-2.png` — "Four fishermen standing in a small boat at night seen from behind, one with hands raised in respect toward the dark tree line, lantern glow, mist over water. STY"
3. `-3.png` — "Close shot of huge tiger pugmarks pressed deep into wet mud on a mangrove bank, a single torch beam raking across them, mangrove roots behind, no animal visible. STY"
4. `-4.png` — "Torch beam cutting through thick night fog over tidal water, insects in the light, the mangrove wall dissolving into blackness, an oar half in frame. STY"
5. `-5.png` — "Dawn on the same creek: two fishermen repairing a net by a small fire on the mud bank, muddy footprints, a forest department notice board on a post, calm grey-gold light, documentary realism, desaturated. STY"

## V-04 v-bastar-chhalawa — Bastar ka chhalawa
1. `-1.png` — "A narrow red-earth jungle track in Bastar at night, three sharp bends, tall sal trees closing in, one bicycle lamp far away, no people. STY"
2. `-2.png` — "A dry stone well in the middle of a jungle clearing, cracked plaster, dry leaves inside the rim, roots crawling over it. STY"
3. `-3.png` — "A man in a vest walking a jungle path at night seen from behind, cheap torch with a weak orange beam, hand raised to shield his eyes, fog. STY"
4. `-4.png` — "The same jungle bend seen four times overlaid like repeating film frames, one figure walking in a loop, confusing identical trees, dreamlike doubling. STY"
5. `-5.png` — "First light: the same path from a distance showing the junction was a simple fork with a broken signboard and a low power line, a village fifty steps away, mundane. STY"

## V-05 v-kutch-dakan — Kutch ki dakan
1. `-1.png` — "A wide empty village lane in Kutch at night, whitewashed low houses with mirrored embroidery doorways, dusty ground, one bulb, salt flats glow on the horizon. STY"
2. `-2.png` — "A courtyard well with a rope and a brass pot, bangles resting on the rim, moonlight, neem shadow. STY"
3. `-3.png` — "A teenage girl in a Kutchhi odhni standing at the well at night, half-turned, torchlight low, seen from behind at three-quarter angle. STY"
4. `-4.png` — "An empty lane seen over the girl's shoulder: nothing there but dust, a swinging gate and a coconut tied on a string, unsettling emptiness rather than a figure. STY"
5. `-5.png` — "Morning in the same lane: a stray dog asleep by the gate, a herd of goats, laundry, an ordinary open gate, warm ordinary light, documentary realism. STY"

## V-06 v-bundelkhand-bangla — Railway colony ka khaali bangla
1. `-1.png` — "Eight identical old railway colony bungalows in a row behind a small Bundelkhand station at night, seven with lights on, the eighth dark with a neem tree in its courtyard. STY"
2. `-2.png` — "Close-up of the empty bungalow's door: rusted hasp and a broken lock, peeling green paint, faded curtain behind glass, dust. STY"
3. `-3.png` — "A twelve-year-old boy standing on a roof at 2 a.m., wrapped in a blanket, listening, seen from behind, the dark bungalow roof below him. STY"
4. `-4.png` — "Ceiling of an old bungalow seen from below: a long crack, sagging plaster, damp stains, a bare bulb, faint humming feeling, no person. STY"
5. `-5.png` — "Daylight inside the abandoned bungalow: an old fountain pen on a windowsill, termite dust, a fallen beam, a padlocked door from inside, plain documentary realism. STY"

## V-07 v-jharkhand-sil — Chudail ka sil
1. `-1.png` — "A grinding stone (silbatta) lying at the edge of a harvested field in Palamu at dusk, empty field, sal trees, no people. STY"
2. `-2.png` — "Close shot of the sil: flour dust on the stone, a cheap wooden photo frame tied with a red thread to a stake beside it. STY"
3. `-3.png` — "Village men standing in a half circle around the stone at night, one holding a phone torch, faces down, seen from behind. STY"
4. `-4.png` — "The framed photo found fallen on the ground at dawn, glass cracked, flour handprints on the stone, dew. STY"
5. `-5.png` — "Morning: two children's slippers and a cheap plastic toy near the stone, a torn school notebook page, the field behind, ordinary light, no ghost. STY"
