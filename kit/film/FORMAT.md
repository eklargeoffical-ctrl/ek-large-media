# Large Sahab Productions: the film format (from 23 Oct 2026)

Every reel is the 13.6-second "trailer" of a Bollywood-style film about one moment every desi friend group knows.
No voiceover and no paid voices: the jokes are carried by big on-screen text, a desi-trap beat with the tabla as
its signature, and sound effects (title slam, whooshes, glass clinks, record scratch). The owner does nothing.

## The clock (keep it exactly; the music is built on it)
| Seconds | Scene | What it does |
|---|---|---|
| 0–1.2 | Opening poster | Hook line at the top, Large Sahab shocked, Hindi title slams in. Frame 0 must already read. |
| 1.2–3.4 | Night card | Three short lines appear one by one (max ~18 characters each) |
| 3.4–8.2 | Three beats, 1.6 s each | Time stamp + one line in a speech bubble; glasses pile up and/or an emoji prop; Large Sahab watches from a corner |
| 8.2–10.8 | Verdict | Record scratch, music stops, Large Sahab's one-liner in a bubble |
| 10.8–13.6 | End poster | Title again, a "Tag the friend…" line, a responsible-drinking pill. Loops to frame 0. |

## Spec (kit/film/specs/filmNN.json; copy film01.json)
- `id` FilmNN, `slug` CamelCase, `date` "YYYY-MM-DDT20:00:00", `seed` (any number), `root` bass note in Hz (vary: 69.3, 73.42, 77.78, 82.41)
- `hook` the first thing people read: "Har group mein ek aisa dost hota hai…" style, under 50 characters
- `title_hi` Devanagari title, `title_en` the same in caps, `tagline` one short line
- `night.lines` 3 lines, `night.at` [1.3, 1.95, 2.6]
- `beats` 3 × {label "RAAT KE"/"SUBAH KE", time "9:00 PM", line (≤ 8 words), glasses 0–7, mood amber|plum|night|gold|red,
  pop [times the glasses appear], sticker (one emoji, optional), wobble true on the last beat if drunk}
  Pops: beat 1 starts 3.65, beat 2 5.25, beat 3 6.85, about 0.12–0.18 s apart.
- `sahab` {line ≤ 8 words, at 8.5, dur 1.5–2.0}
- `end` {line1 "Tag the friend who…", line2 a responsible pill in caps}
- `caption` hook line, "Large Sahab Productions presents: TITLE", tag line, a responsible-drinking line, 5–6 hashtags
- `times` and `total` exactly as film01.json

## Writing rules
- The title alone must be the joke and must be a phrase people already say ("Bas Ek", "Main Theek Hoon").
- Escalate across the three beats; the third is the funniest. The verdict flips it with Large Sahab's dry wit.
- Roast the habit, never a person or a community. No drinking games, no "chug", no glorifying being drunk;
  every film ends on a responsible pill (water, cab, sleep). No brand names of alcohol. No gambling.
- Check the preview frames before rendering: nothing wraps badly or touches the frame edge.

## Render
`python3 make_film.py specs/filmNN.json` (about 2 minutes). Output: `reels/FilmNN_<slug>.mp4` and `reels/FilmNN_Thumb.jpg`
(the end poster, used as the Metricool cover via videoThumbnailUrl).
