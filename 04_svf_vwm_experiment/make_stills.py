"""
make_stills.py — save still images (screenshots) from the reward videos, for the memory tests.

Run it ONCE, after the videos are in place and before running a session that includes the
memory tests. For every clip it saves two stills, taken at different moments:
    stills/<genre>/<bucket>/clip_000_a.jpg
    stills/<genre>/<bucket>/clip_000_b.jpg
The image-selection test uses the "a" stills and the one-by-one test uses the "b" stills,
so the two tests never show the exact same picture.

Needs ffmpeg (the same program the video download scripts use) to be installed.
Run it: open this file in PsychoPy Coder and press Run.
"""

import shutil
import subprocess
from pathlib import Path

VIDEO_ROOT = Path(__file__).parent / "videos"    # must match svf_vwm_mini.py
STILL_ROOT = Path(__file__).parent / "stills"    # must match svf_vwm_mini.py
MOMENTS = {"a": 0.35, "b": 0.65}                 # how far into the clip: 0 = start, 1 = end
LONGEST_SIDE = 480                               # pixels; small pictures load fast

if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
    raise SystemExit("ffmpeg is not installed (or not on PATH), so stills can't be made. See the README.")


def clip_seconds(clip):
    """How long the video really is, according to ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(clip)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


clips = sorted(VIDEO_ROOT.glob("*/*/*.mp4"))     # videos/<genre>/<bucket>/<clip>.mp4
print(f"Found {len(clips)} clips")

for number, clip in enumerate(clips, start=1):
    genre, bucket = clip.parent.parent.name, clip.parent.name
    if bucket == "calibration":                  # those clips aren't part of the main session
        continue

    seconds = clip_seconds(clip)
    for tag, moment in MOMENTS.items():
        out_file = STILL_ROOT / genre / bucket / f"{clip.stem}_{tag}.jpg"
        if out_file.exists():
            continue
        out_file.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", str(seconds * moment), "-i", str(clip),
             "-frames:v", "1", "-vf", f"scale={LONGEST_SIDE}:{LONGEST_SIDE}:force_original_aspect_ratio=decrease",
             str(out_file)],
            check=True,
        )
    print(f"  {number}/{len(clips)}  {genre}/{bucket}/{clip.name}")

print("Done.")
