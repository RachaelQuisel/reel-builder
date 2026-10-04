# reel-builder

Build 6-second Instagram reels (1080x1350, 4:5 portrait, 30fps) with Python and ffmpeg.

## Scripts

### build_plugin_reel.py

Builds a plugin announcement reel: tagline at the top, a "new plugin" label, the plugin icon in the center, and the plugin name typing in at the bottom. Satie music plays underneath.

```
python3 build_plugin_reel.py questions-worth-asking
```

Run it with no argument to see the list of plugins. To add a plugin, add an entry to the `PLUGINS` dictionary (name, tagline, icon, two gradient colors, caption).

Output, written to the `OUT` folder:

- `{slug}-reel-final.mp4` (the reel with music)
- `{slug}-reel.mp4` (silent version)
- `{slug}-reel-cover.png` (last frame, for the cover image)

This is the locked style. Edit this script when the style needs to change instead of starting over.

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
| `assets/audio/gymnopedie-6s.m4a` | `OUT` folder | build_plugin_reel.py |
| `assets/icons/worth-asking.png` | `REF` folder | build_plugin_reel.py |
| `assets/icons/github-portfolio-creator.png` | `REF` folder | build_plugin_reel.py |
| `assets/icons/secure-your-data.png` | `REF` folder | build_plugin_reel.py |

`OUT` and `REF` are set at the top of each script. Change them to match your machine.

Not in this repo yet (build_podcast_reel.py needs these to run):

- `piano-calm-6s.m4a` (piano music, goes in the `OUT` folder)
- the podcast cover image (set in `GIRAFFE`). The script still runs without it and skips the cover art.

Icons come from [ghibli-icon-maker](https://github.com/RachaelQuisel/ghibli-icon-maker).

## Music credit

"Gymnopedie No 1" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

The license requires this credit wherever the music is used, including the Instagram caption or description of each reel.
