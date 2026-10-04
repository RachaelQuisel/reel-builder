# reel-builder

Builds the 6-second Instagram reels that announce new plugins on @agentic_ai_sb. Every reel comes out in the same locked style, so the feed reads as one series.

## What a reel looks like

- 1080x1350 (4:5 portrait), 6 seconds, 30fps
- Tagline at the top, "NEW PLUGIN" eyebrow, the plugin's icon in the center, plugin name typing out at the bottom
- Chill classical music underneath (Satie, Debussy), a different track for each plugin
- Style locked October 4, 2026

## The process

### Step 1: Get the plugin details

Clone the plugin repo, read its README for the name and tagline, and find the icon file.

```bash
cd ~/workspace/plugins
git clone --depth 1 https://github.com/RachaelQuisel/<repo>.git
head -20 <repo>/README.md    # name and tagline
find <repo> -name "*.png"    # icon
```

Use the repo's own icon. Do not generate one. If the repo has no icon, stop and ask Rachael before going further.

### Step 2: Build the reel

```bash
python3 ~/workspace/ig-plugins/build_plugin_reel.py <plugin-slug>
```

This creates `<plugin-slug>-reel-final.mp4` and a cover PNG. The script is the locked format, so do not rebuild a reel from scratch.

> The script still needs to be added to this repo. Right now it lives at `~/workspace/ig-plugins/build_plugin_reel.py`.

### Step 3: Swap the music (optional)

Satie's Gymnopedie No. 1 is the default track. To use a different one, download the MP3, cut a 6-second clip, and layer it under the reel with ffmpeg:

```bash
ffmpeg -i <reel>.mp4 -t 6 -i <track>.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest <reel>-music.mp4
```

Tracks used so far (both from archive.org):

| Track | Recording by | License | Credit in caption? |
|---|---|---|---|
| Satie, Gymnopedie No. 1 | Kevin MacLeod | CC BY 4.0 | Yes |
| Debussy, Clair de Lune | Caela Harrison | Public domain | No |

The compositions are long out of copyright, but each recording carries its own license. A CC BY track needs a credit line in the caption, for example:

`Music: "Gymnopedie No. 1" by Kevin MacLeod (incompetech.com), CC BY 4.0`

### Step 4: Post to Instagram

```bash
instagram-cli post-feed --account-id 17841439052023842 \
  --file <reel>.mp4 \
  --cover <reel>-cover.png \
  --caption "NEW PLUGIN: <Name>. <Tagline>." \
  --mentions '[{"user_fbid":"17841401896333226","x":0.5,"y":0.5}]'
```

- `17841439052023842` is @agentic_ai_sb, the account that posts
- `17841401896333226` is @the_rachael_review, tagged in the center of the frame

Caption rules: keep it short, no em-dashes, tag @the_rachael_review, and add the music credit when the track needs one.

### Step 5: Check that it posted

The CLI returns `{"media_fbid":"..."}` on success. On failure it prints the error. HTTP 429 means Instagram's daily posting limit was hit, so wait until tomorrow and try again.

## How to start it

Say "Post [plugin name] to IG" and include the repo link and the one-line tagline.
