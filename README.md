# reel-builder

Builds the 6-second Instagram reels (1080x1350, 4:5 portrait, 30fps) that announce new plugins on @agentic_ai_sb, using Python and ffmpeg. Every reel comes out in the same locked style, so the feed reads as one series.

## What a reel looks like

- Tagline at the top, a "new plugin" label, the plugin's icon in the center, and the plugin name typing in at the bottom
- A real, recognizable classical piece underneath, a different one for each plugin
- A full description below each post, modeled on the Questions Worth Asking post
- Style locked October 4, 2026

## Scripts

### build_plugin_reel.py

Builds a plugin announcement reel.

```
python3 build_plugin_reel.py questions-worth-asking
```

Run it with no argument to see the list of plugins. To add a plugin, add an entry to the `PLUGINS` dictionary (name, tagline, icon, two gradient colors, caption).

Output, written to the `OUT` folder:

- `{slug}-reel-final.mp4` (the reel with music)
- `{slug}-reel.mp4` (silent version)
- `{slug}-reel-cover.png` (last frame, for the cover image)

This is the locked style. Edit this script when the style needs to change instead of starting over.

> The Satie track was removed from this repo. The script's `MUSIC` setting still points to `gymnopedie-6s.m4a`, so set `MUSIC` to the new piece's file before the next build.

### build_podcast_reel.py

Builds an "AI Tools Daily" podcast promo reel: dark background with the cover art faded at the top, the date, up to four headlines, and a slow zoom. Piano music plays underneath. Edit the headlines, date, and slug at the bottom of the file, then run:

```
python3 build_podcast_reel.py
```

Output: `{slug}-reel-piano.mp4`, `{slug}-reel.mp4`, and `{slug}-reel-cover.png` (first frame).

## What you need

- Python 3 with Pillow (`pip install pillow`)
- ffmpeg
- Noto Sans fonts (Bold, Regular, Medium) at `/usr/share/fonts/truetype/noto/`. On Debian or Ubuntu: `sudo apt install fonts-noto-core`

## Assets

The scripts read assets from hard-coded folders. Copy the files from this repo into those folders before you run them.

| File in this repo | Copy it to | Used by |
|---|---|---|
| `assets/icons/worth-asking.png` | `REF` folder | build_plugin_reel.py |
| `assets/icons/github-portfolio-creator.png` | `REF` folder | build_plugin_reel.py |
| `assets/icons/secure-your-data.png` | `REF` folder | build_plugin_reel.py |

`OUT` and `REF` are set at the top of each script. Change them to match your machine.

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

Run `build_plugin_reel.py` with the plugin's slug (see Scripts above).

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

Post `{slug}-reel-final.mp4` with `{slug}-reel-cover.png` as the cover and the description from Step 4, tagging @the_rachael_review in the center of the frame.
