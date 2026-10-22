# Ek Large production kit

Everything needed to make and schedule @ek.large content without the original chat.

> **Current format (from 23 Oct 2026): Large Sahab Productions films.** See `film/FORMAT.md`, `film/BACKLOG.md` and
> `AUTOPILOT.md`. No voiceover, no paid credits, no carousels; the owner is not involved. The sections below about
> slide reels, carousels and the v2 tabla music describe the retired format and are kept for reference.

## The brand (never break these)
- The character is always **Large Sahab** (never just "Sahab"): an illustrated silver-haired gentleman, white handlebar moustache, round glasses, maroon bandhgala. Faces: `wink` (approves), `dis` (disapproves), `shock`.
- Voice: witty Hinglish uncle at a wedding, a snob about the drink and warm to the drinker. Roast the habit, never the person.
- Colours: Ink #15100C, Oak #2A1D15, Oxblood #4A1A18, Amber #C8862E, Honey #E3B04B, Cream #F2E6CF.
- Type: Lora (headlines, body), Poppins (labels). Hindi accents only, small (FreeSerif Devanagari), never body text.
- Responsible-drinking rules: every caption ends with "Water between pegs" and/or "Never drink and drive". No prices, offers, "buy now", or paid-looking brand tags. 18+ only. Facts must be checkable; label legends as legends.
- Sign-off on every end card: `@EK.LARGE · WATER BETWEEN PEGS`.

## Music
Films (current): desi trap built by `film/make_film.py`: 808 bass, one clap, light hats, the tabla as the signature hook, and sound effects (title slam, whooshes, glass clinks, record scratch). The groove stops dead for Large Sahab's verdict. Owner opened this up on 22 Oct 2026 ("if you have a better option than tabla, use it").

### Retired: v2 tabla music (15 Oct 2026)
Tabla-led, quirky and catchy: a short repeating tabla hook with playful bass-drum wobbles on accents. No sitar, claps or bells; only a faint slow drone. Master at about -17 LUFS. `make_reel.py` does all of this automatically from the spec; vary `groove` (bounce | strut | sneak), `taal` (keherwa | dadra), `sa` and `seed` so consecutive reels sound different.

## Making a reel
1. Write `specs/reelNN.json` (copy an existing one). Scene types:
   - `hook` {label, hindi?, title (HTML, `<em>` = honey italic), sub, face}
   - `card` {label, n, k, title, body, face | icon (neat|rocks|splash|highball|patiala|water|bottle), stamp?, bg (ink|ox|deep|amber|cream)}
   - `tier` {title, rows:[{letter, items[]}]}
   - `list` {hindi?, title, items[], cta, face}
   - `end` {title, line1, line2}  (always last; amber; lines land on the tabla tihai)
   - `bars`: keherwa bar ≈ 2.1–2.3 s (2 bars per card); dadra cycle 1.5 s (3 per card). Keep reels 22–33 s.
   - Use `&nbsp;` to keep names together, always `Large&nbsp;Sahab` in on-screen text. Put `date` (IST, 20:00) and `caption` in the spec.
2. Preview: `python3 make_reel.py specs/reelNN.json --preview 1.5,6,10 /tmp/pv.png` and look at it. Titles must not wrap awkwardly; body text must be readable.
3. Render: `python3 make_reel.py specs/reelNN.json` → `reels/ReelNN_<slug>.mp4`.
   Thumbnail: add a `thumb` object to the spec (see the top of `make_thumb.py`; copy one from reel09–13) and run `python3 make_thumb.py specs/reelNN.json` → `reels/ReelNN_Thumb.jpg`. The thumbnail is a separate poster, never a frame of the video (owner's rule). Short punchy title (2–6 words), one sub line, a face that fits the joke, an optional stamp. Look at it before scheduling. Alternate light (cream, amber) and dark (ink, oak, ox) backgrounds so the profile grid looks good.
4. Commit and push to `main`. Public link: `https://raw.githubusercontent.com/eklargeoffical-ctrl/ek-large-media/main/reels/<file>`.

## Scheduling (Metricool, brand id 6288777, timezone Asia/Kolkata)
`createScheduledPost` with: providers [{network: instagram}], instagramData {type: REEL, showReelOnFeed: true}, media [raw mp4 link], videoThumbnailUrl [raw `ReelNN_Thumb.jpg` link] (never videoCoverMilliseconds), text = caption, publicationDate {dateTime: "YYYY-MM-DDT20:00:00", timezone: "Asia/Kolkata"}, autoPublish true, draft false. Then `getScheduledPosts` to confirm. The free plan allows about 20 posts a month: reels only; the owner posts carousels himself.

## Weekly plan
Current: one film a day at 8:00 pm IST, capped at 20 Metricool posts per calendar month (see AUTOPILOT.md).

Retired plan:
- Reels every day at 8:00 pm IST. Fridays = "Large Sahab's Field Guide: Friday Night Species" series.
- Carousels Tue/Thu/Sat 1:00 pm IST (owner posts). Make them with `carousel.html` (see below) and send the PNGs + captions to the owner.
- Series to rotate: Large Sahab Disapproves, Daru Dictionary, Tier Lists, Field Guide, Bar Etiquette, Made in India whisky trail, Ghar Party, Rate My Bar Cart (only with real DMs the owner shares).
- Never repeat a joke or a "crime" already used (check `specs/` and the captions).
