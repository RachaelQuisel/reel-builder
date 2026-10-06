# reel-builder

Builds the 6-second Instagram reels (1080x1350, 4:5 portrait, 30fps) that announce new plugins on @agentic_ai_sb, using Python and ffmpeg. Every reel comes out in the same locked style, so the feed reads as one series.

## What a reel looks like

- Tagline at the top, a "new plugin" label, the plugin's icon in the center, and the plugin name typing in at the bottom
- Optional music added after the silent reel is built, with recording rights checked separately
- A full description below each post, modeled on the Questions Worth Asking post
- Style locked October 4, 2026

## Scripts

### build_plugin_reel.py

Builds a plugin announcement reel from the icons in this repository. From a fresh clone, install
Python 3, [Pillow](https://pypi.org/project/pillow/), and ffmpeg. The script uses installed Noto
Sans or DejaVu Sans fonts on Linux, or Arial on macOS. To keep the Noto look on another system,
pass `--font-dir` with `NotoSans-Bold.ttf` and `NotoSans-Medium.ttf`.

```sh
git clone https://github.com/RachaelQuisel/reel-builder.git
cd reel-builder
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pillow
# Install ffmpeg with your system package manager if it is not on PATH.
python build_plugin_reel.py github-portfolio-builder
```

This first run needs no music, copied assets, or path edits. It writes to `out/`:

- `github-portfolio-builder-reel.mp4` — six-second silent reel
- `github-portfolio-builder-reel-cover.png` — final frame for a cover

See the [silent sample reel](examples/github-portfolio-builder-reel.mp4) and its
[cover image](examples/github-portfolio-builder-reel-cover.png), generated with that command on
October 6, 2026. The sample contains no audio or client data. System fonts can change letter
spacing slightly; the layout, assets, dimensions, and timing come from this script.

Run `python build_plugin_reel.py --help` for the available slugs and options. Use `--output-dir`
to put the files elsewhere, `--icon-dir` for another icon folder, or `--font-dir` for Noto Sans.
When you have a recording you can use, pass `--music /path/to/track.m4a`; the script then also
writes `{slug}-reel-final.mp4` with audio. No recording is bundled with this repository.
To add a plugin, put its icon in `assets/icons/` and add its name, tagline, icon filename, and
gradient colors to the `PLUGINS` dictionary.

This is the locked style. Edit this script when the style needs to change instead of starting over.

### build_podcast_reel.py

Builds an "AI Tools Daily" podcast promo reel: dark background with the cover art faded at the top, the date, up to four headlines, and a slow zoom. Piano music plays underneath. Edit the headlines, date, and slug at the bottom of the file, then run:

```
python3 build_podcast_reel.py
```

Output: `{slug}-reel-piano.mp4`, `{slug}-reel.mp4`, and `{slug}-reel-cover.png` (first frame).

## What you need

- Python 3 with Pillow (`pip install pillow`)
- ffmpeg on `PATH` (for example, `brew install ffmpeg` on macOS or `sudo apt install ffmpeg` on Debian or Ubuntu)
- Noto Sans or DejaVu Sans on Linux, or Arial on macOS. For Noto Sans on Debian or Ubuntu, install `fonts-noto-core`.

## Assets

The plugin reel script reads these icons directly from `assets/icons/`:

| File | Plugin slug |
|---|---|
| `assets/icons/worth-asking.png` | `questions-worth-asking` |
| `assets/icons/github-portfolio-creator.png` | `github-portfolio-builder` |
| `assets/icons/secure-your-data.png` | `secure-your-data` |

`build_podcast_reel.py` is a separate author workflow and still uses local paths and assets. Its
output and reference folders must be configured before that script can run.

Not in this repo yet (build_podcast_reel.py needs these to run):

- `piano-calm-6s.m4a` (piano music, goes in the `OUT` folder)
- the podcast cover image (set in `GIRAFFE`). The script still runs without it and skips the cover art.

Icons come from [ghibli-icon-maker](https://github.com/RachaelQuisel/ghibli-icon-maker).

## How to post a plugin reel

### Step 1: Get the plugin details

Every plugin's details, including its name, tagline, and icon, come from Rachael's personal GitHub: [github.com/RachaelQuisel](https://github.com/RachaelQuisel). Each plugin has its own repo there.

Use the repo's own icon. Do not generate one. If the repo has no icon, stop and ask Rachael before going further.

### Step 2: Pick the music

- A real, recognizable classical composition (Satie, Debussy, Chopin, Bach, and so on), and the composition must be public domain
- The recording must be public domain, or CC BY with a credit in the description
- No synth pads, no generic stock music
- A different piece for each plugin. Check the table below so no piece repeats.

Music used so far:

| Piece | Recording by | Recording license | Status |
|---|---|---|---|
| Satie, Gymnopedie No. 1 | Kevin MacLeod | CC BY 4.0 | Do not use again |
| Debussy, Clair de Lune | Caela Harrison | Public domain | Used |

To layer a 6-second clip of a new piece under a silent reel:

```bash
ffmpeg -i {slug}-reel.mp4 -t 6 -i <track>.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest {slug}-reel-final.mp4
```

### Step 3: Build the reel

Run `build_plugin_reel.py` with the plugin's slug (see Scripts above). Pass the chosen recording
with `--music` if you want the script to produce the audio version. The silent reel is ready for
review without a music file.

### Step 4: Write the description

Model every description on the [Questions Worth Asking post](https://www.instagram.com/reel/DeAsm-rCa1I/) from October 2, 2026. Write one short paragraph per part, with a blank line between parts:

1. **Hook:** one line, second person, a moment the reader recognizes. It has to work on its own, because Instagram cuts the description off after the first line or two.
2. **Pain:** one or two sentences on why the problem keeps happening.
3. **What it does:** the plugin name and what it does, plus one short line on why it matters.
4. **Credibility:** "Built by me at XRAY, an official Anthropic partner."
5. **Call to action:** "What plugin do you wish existed? Drop it below. I'll pick one, build it, and share it here."
6. **Tag:** @the_rachael_review
7. **Music credit:** only if the recording is CC BY
8. **Hashtags:** #AItools #ClaudePlugins #buildinpublic

Keep sentences short, use plain words, and skip em-dashes.

Example:

```
You left the meeting. Then the real question hit you in the car.

It happens every week. The question that would have changed the whole conversation, arriving ten minutes too late.

Questions Worth Asking replays your meetings and finds the questions you didn't ask. Before the moment passes.

Built by me at XRAY, an official Anthropic partner.

What plugin do you wish existed? Drop it below. I'll pick one, build it, and share it here.

@the_rachael_review
#AItools #ClaudePlugins #buildinpublic
```

Music credit format for a CC BY recording:
`Music: "<Piece>" by <Performer> (<source>), CC BY 4.0`

### Step 5: Post to Instagram

Post `{slug}-reel-final.mp4` when you added licensed music, or `{slug}-reel.mp4` when you chose a
silent post. Use `{slug}-reel-cover.png` as the cover and the description from Step 4, tagging
@the_rachael_review in the center of the frame.
