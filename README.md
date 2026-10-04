# reel-builder

Builds the 6-second Instagram reels that announce new plugins on @agentic_ai_sb. Every reel comes out in the same locked style, so the feed reads as one series.

## What a reel looks like

- 1080x1350 (4:5 portrait), 6 seconds, 30fps
- Tagline at the top, "NEW PLUGIN" eyebrow, the plugin's icon in the center, plugin name typing out at the bottom
- Chill classical music underneath (Satie, Debussy), a different track for each plugin
- A full description below each post, modeled on the Questions Worth Asking post
- Style locked October 4, 2026

## The process

### Step 1: Get the plugin details

Every plugin's details, including its name, tagline, and icon, come from Rachael's personal GitHub: [github.com/RachaelQuisel](https://github.com/RachaelQuisel). Each plugin has its own repo there.

Clone the plugin repo, read its README for the name, tagline, and what it does, and find the icon file.

```bash
cd ~/workspace/plugins
git clone --depth 1 https://github.com/RachaelQuisel/<repo>.git
head -40 <repo>/README.md    # name, tagline, and what it does
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

| Track | Recording by | License | Credit in description? |
|---|---|---|---|
| Satie, Gymnopedie No. 1 | Kevin MacLeod | CC BY 4.0 | Yes |
| Debussy, Clair de Lune | Caela Harrison | Public domain | No |

The compositions are long out of copyright, but each recording carries its own license. A CC BY track needs a credit line in the description, for example:

`Music: "Gymnopedie No. 1" by Kevin MacLeod (incompetech.com), CC BY 4.0`

### Step 4: Write the description

Model every description on the [Questions Worth Asking post](https://www.instagram.com/reel/DeAsm-rCa1I/) from October 2, 2026. Write one short paragraph per part, with a blank line between parts:

1. **Hook:** one line, second person, a moment the reader recognizes. It has to work on its own, because Instagram cuts the description off after the first line or two.
2. **Pain:** one or two sentences on why the problem keeps happening.
3. **What it does:** the plugin name and what it does, plus one short line on why it matters.
4. **Credibility:** "Built by me at XRAY, an official Anthropic partner."
5. **Call to action:** "What plugin do you wish existed? Drop it below. I'll pick one, build it, and share it here."
6. **Tag:** @the_rachael_review
7. **Music credit:** only if the track needs one
8. **Hashtags:** #AItools #ClaudePlugins #buildinpublic

Keep sentences short, use plain words, and skip em-dashes.

Example, using the Questions Worth Asking post with the updated credibility line:

```
You left the meeting. Then the real question hit you in the car.

It happens every week. The question that would have changed the whole conversation, arriving ten minutes too late.

Questions Worth Asking replays your meetings and finds the questions you didn't ask. Before the moment passes.

Built by me at XRAY, an official Anthropic partner.

What plugin do you wish existed? Drop it below. I'll pick one, build it, and share it here.

@the_rachael_review
#AItools #ClaudePlugins #buildinpublic
```

### Step 5: Post to Instagram

Save the approved description to `<reel>-caption.txt`, then run:

```bash
instagram-cli post-feed --account-id 17841439052023842 \
  --file <reel>.mp4 \
  --cover <reel>-cover.png \
  --caption "$(cat <reel>-caption.txt)" \
  --mentions '[{"user_fbid":"17841401896333226","x":0.5,"y":0.5}]'
```

- `17841439052023842` is @agentic_ai_sb, the account that posts
- `17841401896333226` is @the_rachael_review, tagged in the center of the frame

### Step 6: Check that it posted

The CLI returns `{"media_fbid":"..."}` on success. On failure it prints the error. HTTP 429 means Instagram's daily posting limit was hit, so wait until tomorrow and try again.

## How to start it

Say "Post [plugin name] to IG" and include the repo link and the one-line tagline.
