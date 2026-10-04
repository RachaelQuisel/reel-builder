#!/usr/bin/env python3
"""AI Tools Daily podcast reel builder: 1080x1350, 6s, with headlines and piano music."""
import os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/ig-plugins"
TMP = "/tmp/podcast_frames"
INK = (62, 52, 46)
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
MED = "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"
W, H = 1080, 1350
FPS, DUR = 30, 6.0

GIRAFFE = "/home/hatch/workspace/podcasts/covers/media-generation-hardfork-style-cover-preview-0-94fb097b-4f90-4bcf-8b80-c97c3b849a0e.webp"
PIANO = f"{OUT}/piano-calm-6s.m4a"


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


def build_reel(date_str, headlines, slug):
    """Build a 6s podcast promo reel."""
    # Background: dark with giraffe accent
    bg = Image.new("RGB", (W, H), (28, 25, 22))
    d = ImageDraw.Draw(bg)

    # Giraffe cover as faded background top
    try:
        gf = Image.open(GIRAFFE).convert("RGB")
        gf = gf.resize((W, 700), Image.LANCZOS)
        # Darken it
        overlay = Image.new("RGB", (W, 700), (28, 25, 22))
        gf = Image.blend(gf, overlay, 0.55)
        bg.paste(gf, (0, 0))
    except Exception as e:
        print(f"giraffe load failed: {e}")

    # Title
    tf = ImageFont.truetype(BOLD, 72)
    title = "AI Tools Daily"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 60), title, font=tf, fill=(255, 240, 200))

    # Date
    df = ImageFont.truetype(MED, 40)
    dw = d.textlength(date_str, font=df)
    d.text(((W - dw) / 2, 150), date_str, font=df, fill=(200, 180, 150))

    # Headlines
    hf = ImageFont.truetype(REG, 44)
    y = 780
    for hl in headlines[:4]:
        lines = wrap(d, "• " + hl, hf, 920)
        for ln in lines:
            lw = d.textlength(ln, font=hf)
            d.text(((W - lw) / 2, y), ln, font=hf, fill=(235, 225, 210))
            y += 62
        y += 18

    # CTA at bottom
    cf = ImageFont.truetype(MED, 36)
    cta = "New episode daily  •  Link in bio"
    cw = d.textlength(cta, font=cf)
    d.text(((W - cw) / 2, H - 120), cta, font=cf, fill=(180, 160, 130))

    # Animate: subtle zoom over 6s
    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    nframes = int(FPS * DUR)
    for i in range(nframes):
        t = i / nframes
        # 1.0 -> 1.06 zoom
        z = 1.0 + 0.06 * t
        zw, zh = int(W * z), int(H * z)
        frame = bg.resize((zw, zh), Image.LANCZOS)
        # Center crop
        x0, y0 = (zw - W) // 2, (zh - H) // 2
        frame = frame.crop((x0, y0, x0 + W, y0 + H))
        frame.save(f"{TMP}/f{i:03d}.png")

    mp4 = f"{OUT}/{slug}-reel.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{TMP}/f%03d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-movflags", "+faststart", mp4],
                   check=True, capture_output=True)

    # Add piano audio
    mp4_music = f"{OUT}/{slug}-reel-piano.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", mp4, "-i", PIANO,
                    "-c:v", "copy", "-c:a", "aac", "-shortest", mp4_music],
                   check=True, capture_output=True)

    # Cover = first frame
    cover = Image.open(f"{TMP}/f000.png")
    cover.save(f"{OUT}/{slug}-reel-cover.png")
    shutil.rmtree(TMP)
    print(f"wrote {mp4_music}")


if __name__ == "__main__":
    headlines_oct4 = [
        "ChatGPT Dot allegedly emailed city hall",
        "OpenAI DevDay: Dots get their own computers",
        "Pro plan usage halved, new $500 tier",
        "Global usage reset after demand spike",
    ]
    build_reel("October 4, 2026", headlines_oct4, "ai-tools-daily-oct4")
