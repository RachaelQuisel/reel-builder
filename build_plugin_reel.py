#!/usr/bin/env python3
"""Build a six-second plugin announcement reel from the bundled icons.

Style locked 2026-10-04 per Rachael:
- 1080x1350 (4:5 portrait), 6 seconds, 30fps
- Grabby tagline hook at top, "NEW PLUGIN" eyebrow, icon center, name typing at bottom
- Music is optional and supplied by the person making the reel
- Icons: bundled Soft Index style assets
- Captions: short, no em-dashes, tag @the_rachael_review

DO NOT regenerate from scratch. Edit this script if the style needs to change.
"""
import argparse
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
INK = (62, 52, 46)
W, H = 1080, 1350
FPS, DUR = 30, 6.0

FONT_PAIRS = (
    ("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
     "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
     "/System/Library/Fonts/Supplemental/Arial.ttf"),
)

PLUGINS = {
    "questions-worth-asking": {
        "name": "Questions Worth Asking",
        "tagline": "Finds the questions you didn't ask, in meetings you already had.",
        "icon": "worth-asking.png",
        "top": (229, 238, 239), "bottom": (190, 212, 218),
        "caption": "NEW PLUGIN: Questions Worth Asking. Finds the questions you didn't ask, in meetings you already had.",
    },
    "github-portfolio-builder": {
        "name": "GitHub Portfolio Builder",
        "tagline": "See your GitHub the way a hiring manager does, before they do.",
        "icon": "github-portfolio-creator.png",
        "top": (251, 239, 222), "bottom": (235, 206, 180),
        "caption": "NEW PLUGIN: GitHub Portfolio Builder. See your GitHub the way a hiring manager does, before they do.",
    },
    "secure-your-data": {
        "name": "Secure Your Data",
        "tagline": "Compares documented AI privacy defaults with settings you can verify in your own accounts.",
        "icon": "secure-your-data.png",
        "top": (234, 238, 219), "bottom": (196, 209, 185),
        "caption": "NEW PLUGIN: Secure Your Data. Compares documented AI privacy defaults with settings you can verify in your own accounts.",
    },
}


def gradient(top, bottom):
    g = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        g.putpixel((0, y), tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3)))
    return g.resize((W, H), Image.BICUBIC)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines


def resolve_fonts(font_dir):
    if font_dir:
        pairs = ((font_dir / "NotoSans-Bold.ttf", font_dir / "NotoSans-Medium.ttf"),)
    else:
        pairs = FONT_PAIRS
    for bold, medium in pairs:
        if Path(bold).is_file() and Path(medium).is_file():
            return str(bold), str(medium)
    raise FileNotFoundError(
        "No supported fonts found. Install Noto Sans or pass --font-dir with "
        "NotoSans-Bold.ttf and NotoSans-Medium.ttf."
    )


def fit_font(text, path, start, max_w, max_lines=2):
    size = start
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while size > 20:
        f = ImageFont.truetype(path, size)
        if len(wrap(probe, text, f, max_w)) <= max_lines:
            return f
        size -= 4
    return ImageFont.truetype(path, 20)


def base_layers(p, icon_path, medium_font):
    bg = gradient(p["top"], p["bottom"])
    mid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(mid)
    # Grabby tagline hook at top
    tf = ImageFont.truetype(medium_font, 52)
    tlines = wrap(d, p["tagline"], tf, 920)
    lh = int(tf.size * 1.38)
    y = 110
    for ln in tlines:
        w = d.textlength(ln, font=tf)
        d.text(((W - w) / 2, y), ln, font=tf, fill=INK + (235,))
        y += lh
    # Eyebrow
    ef = ImageFont.truetype(medium_font, 40)
    brow = "N E W   P L U G I N"
    bw = d.textlength(brow, font=ef)
    d.text(((W - bw) / 2, y + 28), brow, font=ef, fill=INK + (200,))
    # Icon
    with Image.open(icon_path) as source_icon:
        icon = source_icon.convert("RGBA").resize((560, 560), Image.LANCZOS)
    mid.alpha_composite(icon, (int((W - 560) / 2), y + 100))
    return bg, mid


def build_reel(slug, output_dir, icon_dir, bold_font, medium_font, music=None):
    """Build a silent reel and cover; add audio only when a music file is supplied."""
    p = PLUGINS[slug]
    icon_path = icon_dir / p["icon"]
    if not icon_path.is_file():
        raise FileNotFoundError(f"Missing plugin icon: {icon_path}")
    if music and not music.is_file():
        raise FileNotFoundError(f"Missing music file: {music}")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required; install it and put it on PATH.")
    output_dir.mkdir(parents=True, exist_ok=True)
    bg, mid = base_layers(p, icon_path, medium_font)
    name = p["name"]
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    f = fit_font(name, bold_font, 96, 940)
    full_lines = wrap(probe, name, f, 940)
    nframes = int(FPS * DUR)
    with TemporaryDirectory(prefix="plugin-frames-", dir=output_dir) as frame_dir:
        frames = Path(frame_dir)
        for i in range(nframes):
            t = i / FPS
            frame = bg.convert("RGBA")
            a_mid = min(1.0, t / 0.8)
            if a_mid > 0:
                m = mid.copy()
                ma = m.getchannel("A").point(lambda v: int(v * a_mid))
                m.putalpha(ma)
                frame.alpha_composite(m)
            d = ImageDraw.Draw(frame)
            if t >= 0.8:
                frac = min(1.0, (t - 0.8) / 2.6)
                target = int(frac * len(name))
                shown = name[:target]
                y = 1050
                lh = int(f.size * 1.22)
                rem = shown
                for ln in full_lines:
                    if rem.startswith(ln):
                        w = d.textlength(ln, font=f)
                        d.text(((W - w) / 2, y), ln, font=f, fill=INK + (255,))
                        rem = rem[len(ln):].lstrip()
                        cx = (W - w) / 2 + w
                        last_line = y
                    elif rem:
                        w = d.textlength(rem, font=f)
                        d.text(((W - w) / 2, y), rem, font=f, fill=INK + (255,))
                        last_line, cx = y, (W - w) / 2 + w
                        rem = ""
                    else:
                        last_line, cx = y, W / 2
                    y += lh
                if frac < 1.0:
                    if (t * 2.4) % 1 < 0.65:
                        d.rectangle([cx + 8, last_line + 8, cx + 22, last_line + f.size + 4], fill=INK + (255,))
                elif t < 4.0:
                    d.rectangle([cx + 8, last_line + 8, cx + 22, last_line + f.size + 4], fill=INK + (255,))
            frame.convert("RGB").save(frames / f"f{i:03d}.png")

        silent = output_dir / f"{slug}-reel.mp4"
        subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "f%03d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                        "-movflags", "+faststart", str(silent)],
                       check=True, capture_output=True)
        cover = output_dir / f"{slug}-reel-cover.png"
        with Image.open(frames / f"f{nframes-1:03d}.png") as last_frame:
            last_frame.save(cover)

    print(f"wrote {silent}")
    print(f"wrote {cover}")
    if not music:
        return silent
    final = output_dir / f"{slug}-reel-final.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(silent), "-i", str(music),
                    "-c:v", "copy", "-c:a", "aac", "-shortest", str(final)],
                   check=True, capture_output=True)
    print(f"wrote {final}")
    return final


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", choices=PLUGINS)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "out")
    parser.add_argument("--icon-dir", type=Path, default=ROOT / "assets" / "icons")
    parser.add_argument("--font-dir", type=Path, help="directory with NotoSans-Bold.ttf and NotoSans-Medium.ttf")
    parser.add_argument("--music", type=Path, help="optional audio file for the final reel")
    args = parser.parse_args()
    bold_font, medium_font = resolve_fonts(args.font_dir)
    build_reel(args.slug, args.output_dir, args.icon_dir, bold_font, medium_font, args.music)
