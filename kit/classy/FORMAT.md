# Large Sahab Explains: the classy format (from 23 Oct 2026)

Approved by the owner on 22 Oct 2026. Every reel is a slow, elegant explainer (or a short comedy film) in a dark
speakeasy look: warm bokeh, a gold art-deco frame, gold line drawings that draw themselves in, cream serif type and
Large Sahab in a gold medal. Lounge jazz plays low underneath. No voiceover, no paid credits, the owner is not involved.

Mix: about four explainers to one comedy film. Topics: whisky and other spirits, Indian whisky, brand history and
name meanings (editorial only), cocktails, bar etiquette, myths, quizzes. Comedy films roast the habit, never a person.

## How a reel is built
`python3 kit/classy/make_classy.py kit/classy/specs/explainNN.json` → `reels/ExplainNN_<slug>.mp4` and `reels/ExplainNN_Cover.jpg`.
Before rendering, run `python3 kit/classy/preview.py kit/classy/specs/explainNN.json /tmp/pv` and look at
`/tmp/pv/ExplainNN_sheet.jpg` (opener, every card fully revealed, outro, cover). Fix anything that wraps badly or crowds.
Rendering takes about 6–10 minutes per reel on two cores.

## Version 2 (from 26 Oct 2026): hook first, shorter. This is now the default.
Why: after the first 4 classy reels, viewers still left after 2–4 seconds (average watch 1.6–3.7 s on 34–42 s reels).
The 3-second title card looked like a slide, so most people never reached the first fact.
- Set `"v2": true, "open": 0, "outro_dur": 3.0` and a `hook` (HTML, `<i>` = honey italic, ≤ 2 lines at 68 px, ideally a question).
  The hook sits in a bar at the top for the whole reel, with a small Large Sahab medal, the series label and a thin progress line.
  There is no title card: the first scene is already on screen at frame 0 (its drawing nearly complete, its first lines visible),
  and a glass clink plays at frame 0.
- 3–4 scenes, 4.6–5.4 s each (recipe 6.2, quiz 6.8 with `"qcd": 1.0, "qrv": 4.0`, comedy beats 3.6), total 18–25 s.
  Keep each scene calm; cut scenes rather than speeding them up. Put the most surprising scene first.
- Hooks that worked best: a curiosity question with an India link ("Why does tonic say ‘Indian’?" kept 45% past 3 s).
  The two reels that reached the most people were about Indian whisky: make about half the reels India-angle topics.
- Covers stay as before (the separate thumbnail). With exactly 4 cards the `grid` cover becomes 2 × 2.

## Spec (copy the closest existing spec)
- `id` ExplainNN, `slug` CamelCase, `date` YYYY-MM-DD (posts at 20:00 IST), `seed`
- Music: `prog` D | Eb | F, `shift` (semitones, −2…+2), `bpm` 72–82. Vary them from the previous few reels.
- Opener: `series` ("LARGE SAHAB EXPLAINS", "LARGE SAHAB’S BAR QUIZ", "LARGE SAHAB PRESENTS"), `hindi` (short Devanagari line),
  `title` (the hook; HTML, `<i>` = honey italic; it is on screen at frame 0), `title_size` (optional), `sub`, `badge` ("TOPIC · NN").
- `cards`: each has `type` and `dur` (seconds). Types:
  - `info` — art in the arch + `kicker`, `head` (one line; `head_size`; `wrap: true` for a sentence), `sub_label`?, `sub`, `body`, `tip`?
    Years: `head: '<span style="color:var(--honey)">1858</span>'`, `head_size: 150`. Big number instead of art: `stat` ("No.1"),
    or a counting number with `stat_num`, `stat_pre`, `stat_suf`, `stat_note`, `stat_size` (≤190). dur 5.2–6.0.
  - `myth` — `myth` (gets struck through), `truth`, `body`, `tip`?. dur 6.6.
  - `recipe` — `kicker`, `head`, `rows` [[measure, ingredient] ×≤4], `note_label`, `note`. dur 6.4–6.6.
  - `quiz` — `kicker` ("CLUE 1"), `clue` (≤ 3 lines), `options` (3), `answer` (index), `explain`. dur 7.6 (3-2-1 countdown, ticks, ding).
  - `beat` (comedy) — `label` (RAAT KE / SUBAH KE), `time`, `quote`, `glasses` (total), `from` (glasses already there), `stage`
    (an italic stage direction about Large Sahab), `react` {raise, brow2, mouth, look, smile}, `wobble` on the last beat. dur 4.2.
  - `verdict` — Large Sahab's line `quote` and `sub`. dur 4.6.
  - `drink` — the original Explain 01 card (`name`, `from`, `fact`, `glass`, `liq`, `src`, `tip`).
- `timeline: true` swaps the progress dashes for a year strip (each card needs `tl`).
- Art (`art` on a card): `main` + optional `side` + optional `over`, plus `liq` (amber | dark | gold | brandy | clear | gin | tonic | none),
  `mono` (a letter on a bottle label), `label` (lines on a bottle label), `word` (on `print`, `seal`, `apothecary`).
  - main: rocks, shot, tall, copa, snifter, tulip, bottle, apothecary, barrel, still, hills, trophy, seal, print, pair, eu
  - side: barley, cane, potato, juniper, agave, grapes, hourglass, thistle, lime, bark, magnifier, dasher, peel, antlers, mill, river, drop, shop, field, eye, stopwatch
  - over: dropper (`over_y`: 200 for rocks, 152 for tulip), aroma, light, swirl, bubbles, cube, spoon
  New drawings go in `classy.html` (MAIN / SIDE / OVER): original gold line-art only.
- `outro` {line, cta, pill}. Pills: "DRINK SLOW · NEVER DRINK AND DRIVE", "WATER BETWEEN EVERY PEG", "SIP SLOW · NEVER DRINK AND DRIVE".
- `cover_title` and `cover` (the thumbnail): `grid` (art of every card), `list` {items} (struck-through myths), `hero` {art, note},
  `timeline` {art, years}, `quiz` {options}, `film` {series, size, note}. Keep the key content between y 240 and 1680
  (the profile grid shows the middle 3:4).
- `caption`: hook line with the keywords first, the facts in short lines, a save/share/comment call, the responsible line
  ("Drink slow. Never drink and drive. 18+"), then **exactly five hashtags** ending with #LargeSahab #EkLarge (Instagram allows 5).

## Rules that never change
- Facts must be verified (web search) before they go in a spec; note the source in `kit/log.md`. Legends are labelled as legends.
- Brands only editorially (history, what a name means, awards). Never "why X is good", prices, offers or "buy".
  Never download or copy logos, labels or bottle photos; draw original line-art instead (a plain letter on a label is fine).
- No copyrighted music or film dialogue. The music is generated by `make_classy.py`.
- Always "Large Sahab", never just "Sahab". Responsible line in every reel and caption. 18+.
- Pacing stays slow: never shorten `dur` below the numbers above. Music stays low (loudnorm −18 LUFS).
