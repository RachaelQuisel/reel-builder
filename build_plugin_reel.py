#!/usr/bin/env python3
"""CANONICAL Instagram plugin announcement reel builder.

Style locked 2026-10-04 per Rachael:
- 1080x1350 (4:5 portrait), 6 seconds, 30fps
- Grabby tagline hook at top, "NEW PLUGIN" eyebrow, icon center, name typing at bottom
- Music: Satie Gymnopedie No.1 (Kevin MacLeod, CC-BY) - chill classical
- Icons: Soft Index style from ~/workspace/skills/soft-index-icons/references/
- Captions: short, no em-dashes, tag @the_rachael_review

DO NOT regenerate from scratch. Edit this script if the style needs to change.
"""
import os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/ig-plugins"
TMP = "/tmp/plugin_frames"
REF = "/home/hatch/workspace/skills/soft-index-icons/references"
INK = (62, 52, 46)
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
MED = "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"
W, H = 1080, 1350
FPS, DUR = 30, 6.0
MUSIC = f"{OUT}/gymnopedie-6s.m4a"  # Satie, chill classical, 6s

PLUGINS = {
    "questions-worth-asking": {
        "name": "Questions Worth Asking",
        "tagline": "Finds the questions you didn't ask, in meetings you already had.",
        "icon": f"{REF}/worth-asking.png",
        "top": (229, 238, 239), "bottom": (190, 212, 218),
        "caption": "NEW PLUGIN: Questions Worth Asking. Finds the questions you didn't ask, in meetings you already had.",
    },
    "github-portfolio-builder": {
        "name": "GitHub Portfolio Builder",
        "tagline": "See your GitHub the way a hiring manager does, before they do.",
        "icon": f"{REF}/github-portfolio-creator.png",
        "top": (251, 239, 222), "bottom": (235, 206, 180),
        "caption": "NEW PLUGIN: GitHub Portfolio Builder. See your GitHub the way a hiring manager does, before they do.",
    },
    "secure-your-data": {
        "name": "Secure Your Data",
        "tagline": "Compares documented AI privacy defaults with settings you can verify in your own accounts.",
        "icon": f"{REF}/secure-your-data.png",
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


def fit_font(text, path, start, max_w, max_lines=2):
    size = start
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while size > 20:
        f = ImageFont.truetype(path, size)
        if len(wrap(probe, text, f, max_w)) <= max_lines:
            return f
        size -= 4
    return ImageFont.truetype(path, 20)


def base_layers(p):
    bg = gradient(p["top"], p["bottom"])
    mid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(mid)
    # Grabby tagline hook at top
    tf = ImageFont.truetype(MED, 52)
    tlines = wrap(d, p["tagline"], tf, 920)
    lh = int(tf.size * 1.38)
    y = 110
    for ln in tlines:
        w = d.textlength(ln, font=tf)
        d.text(((W - w) / 2, y), ln, font=tf, fill=INK + (235,))
        y += lh
    # Eyebrow
    ef = ImageFont.truetype(MED, 40)
    brow = "N E W   P L U G I N"
    bw = d.textlength(brow, font=ef)
    d.text(((W - bw) / 2, y + 28), brow, font=ef, fill=INK + (200,))
    # Icon
    icon = Image.open(p["icon"]).convert("RGBA").resize((560, 560), Image.LANCZOS)
    mid.alpha_composite(icon, (int((W - 560) / 2), y + 100))
    return bg, mid


def build_reel(slug):
    """Build the 6s reel for a plugin slug. Output: {slug}-reel-final.mp4"""
    p = PLUGINS[slug]
    bg, mid = base_layers(p)
    name = p["name"]
    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    full_lines = wrap(probe, name, fit_font(name, BOLD, 96, 940), 940)
    f = fit_font(name, BOLD, 96, 940)
    nframes = int(FPS * DUR)
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
            for li, ln in enumerate(full_lines):
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
        frame.convert("RGB").save(f"{TMP}/f{i:03d}.png")

    mp4 = f"{OUT}/{slug}-reel.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{TMP}/f%03d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-movflags", "+faststart", mp4],
                   check=True, capture_output=True)
    # Add Satie music
    final = f"{OUT}/{slug}-reel-final.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", mp4, "-i", MUSIC,
                    "-c:v", "copy", "-c:a", "aac", "-shortest", final],
                   check=True, capture_output=True)
    cover = Image.open(f"{TMP}/f{nframes-1:03d}.png")
    cover.save(f"{OUT}/{slug}-reel-cover.png")
    shutil.rmtree(TMP)
    print(f"wrote {final}")
    return final


if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if slug and slug in PLUGINS:
        build_reel(slug)
    else:
        print(f"usage: {sys.argv[0]} <slug>")
        print(f"slugs: {', '.join(PLUGINS)}")
