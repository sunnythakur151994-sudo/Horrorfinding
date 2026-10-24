#!/usr/bin/env python3
"""
Render narrated story films (MP4, 1280x720, 16:9) from a story's artwork + narration.

  python3 tools/make_films.py bhangarh nishi

- artwork: assets/<art>.webp (falls back to the story's plate colour)
- narration: audio/<id>.mp3
- look: slow ken-burns push, drifting fog, vignette, film grain, silent title card
- output: video/<id>.mp4  + appends to audio/manifest.json
"""
import json, pathlib, subprocess, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1280, 720
FPS = 25

TITLES = {
    "bhangarh": ("BHANGARH KA SHRAP", "FILE 01 · RAJASTHAN · LOK-KATHA"),
    "nishi":    ("NISHI DAAK", "FILE 05 · BENGAL · LOK-KATHA"),
}

def probe_dur(path):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration" in line:
            hms = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = hms.split(":")
            return int(h)*3600 + int(m)*60 + float(s)
    return 30.0

from PIL import Image, ImageDraw, ImageFont
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def title_card(title, sub, tmpdir):
    """Transparent 1280x720 PNG with the film's opening title."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # soft dark plate behind the text
    d.rectangle([0, H//2 - 150, W, H//2 + 130], fill=(3, 6, 6, 150))
    f1 = ImageFont.truetype(SERIF, 62)
    while d.textlength(title, font=f1) > W - 160 and f1.size > 26:
        f1 = ImageFont.truetype(SERIF, f1.size - 2)
    f2 = ImageFont.truetype(MONO, 19)
    tw = d.textlength(title, font=f1)
    d.text(((W - tw) / 2, H//2 - 96), title, font=f1, fill=(246, 241, 228, 255))
    sw = d.textlength(sub, font=f2)
    d.text(((W - sw) / 2, H//2 + 10), sub, font=f2, fill=(232, 121, 79, 255))
    d.line([W/2 - 90, H//2 + 62, W/2 + 90, H//2 + 62], fill=(232, 121, 79, 180), width=2)
    out = pathlib.Path(tmpdir) / "title.png"
    img.save(out)
    return out

def make(story_id, art, audio, title, sub):
    out = ROOT / "video" / f"{story_id}.mp4"
    out.parent.mkdir(exist_ok=True)
    dur = probe_dur(audio)
    frames = int(dur * FPS)

    fade = 4.4
    tmp = tempfile.mkdtemp()
    card = title_card(title, sub, tmp)
    vf = (
        f"scale={int(W*1.25)}:{int(H*1.25)}:force_original_aspect_ratio=increase,crop={int(W*1.25)}:{int(H*1.25)},"
        f"zoompan=z='min(1.0+0.00035*on,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={frames}:s={W}x{H}:fps={FPS},"
        f"eq=saturation=0.78:contrast=1.06:brightness=-0.06,"
        f"vignette=PI/4.2,noise=alls=7:allf=t,"
        f"fade=t=in:st=0:d=1.2,fade=t=out:st={max(0,dur-2.2):.2f}:d=2.2,format=yuv420p[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0:d=0.9:alpha=1,fade=t=out:st={fade-0.9:.2f}:d=0.9:alpha=1[ttl];"
        f"[bg][ttl]overlay=0:0:enable='lt(t,{fade+0.6})':format=auto[v]"
    )
    cmd = [FF, "-y", "-loglevel", "error",
           "-loop", "1", "-i", str(art),
           "-loop", "1", "-i", str(card),
           "-i", str(audio),
           "-filter_complex", vf, "-map", "[v]", "-map", "2:a", "-r", str(FPS),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "29", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k",
           "-shortest", "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("FAIL", story_id, r.stderr[-1200:])
        return None
    print("film:", out.name, f"{out.stat().st_size/1e6:.1f} MB", f"{dur:.0f}s")
    return out

def main():
    man_p = ROOT / "audio" / "manifest.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    man.setdefault("audio", {})
    man.setdefault("films", {})

    # every ready narration becomes a film unless already present
    todo = sys.argv[1:] or [p.stem for p in sorted((ROOT/"audio").glob("*.mp3"))]
    arts = {"bhangarh": ROOT/"assets/bhangarh-real.webp",
            "nishi": ROOT/"assets/nishi-doorway.webp"}
    for sid in todo:
        aud = ROOT / "audio" / f"{sid}.mp3"
        if not aud.exists():
            print("no narration for", sid); continue
        man["audio"][sid] = [f"audio/{sid}.mp3"]
        if sid in arts and arts[sid].exists():
            t, s = TITLES.get(sid, (sid.upper(), "HORROR FINDINGS AROUND INDIA"))
            out = make(sid, arts[sid], aud, t, s)
            if out:
                man["films"][sid] = f"video/{sid}.mp4"
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print("manifest updated:", {k: len(v) for k, v in man.items()})

if __name__ == "__main__":
    main()
