"""Shared ffmpeg helper (binary comes from imageio-ffmpeg, no system install needed)."""
import subprocess, pathlib
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()

def run(args, quiet=True):
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + args, capture_output=True, text=True)
    if r.returncode:
        print("ffmpeg error:", r.stderr[-900:])
    return r.returncode == 0

def concat_audio(parts, out):
    lst = pathlib.Path(out).with_suffix(".txt")
    lst.write_text("\n".join(f"file '{pathlib.Path(p).resolve()}'" for p in parts))
    return run(["-f", "concat", "-safe", "0", "-i", str(lst),
                "-c:a", "libmp3lame", "-b:a", "96k", "-ar", "44100", str(out)])
