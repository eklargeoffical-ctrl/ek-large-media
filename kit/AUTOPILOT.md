# Weekly autopilot (runs every Sunday morning, IST)

You are producing the next week of reels for the Instagram page @ek.large. The owner has asked not to be involved:
you make, upload and schedule everything yourself. Be careful: these posts go live automatically.

Since 23 Oct 2026 every reel is a **Large Sahab Explains** reel in the classy format the owner approved
(see `kit/classy/FORMAT.md`): slow, elegant explainers about whisky, other spirits, cocktails and bar etiquette, with
an occasional short comedy film. The older formats (`kit/film`, `kit/make_reel.py`, carousels) are retired.
No voiceover, and never use ElevenLabs or any paid credits.

1. **Get the kit.** Attach and clone the GitHub repository `eklargeoffical-ctrl/ek-large-media` (push access).
   Read `kit/README.md`, `kit/classy/FORMAT.md` and `kit/classy/BACKLOG.md`. Read `kit/log.md` to see what is already made.
2. **Find the window.** Call Metricool `getBrandSettings` (brand 6288777, Asia/Kolkata) and `getScheduledPosts` from
   today to 21 days ahead. The window is every date from the day after the last scheduled reel up to and including the
   first Monday that is at least 7 days after today. If the window is empty, skip to step 6.
3. **Respect the free plan.** Metricool's free plan allows about 20 scheduled posts per calendar month. Count the posts
   already scheduled or published through Metricool in each month the window touches (from `kit/log.md` and
   `getScheduledPosts`). Never plan more than 20 in a month. When a month cannot take a reel every day, pick days in
   this order: Fri, Sat, Sun, Wed, Mon, Thu, Tue.
4. **Make the reels.** For each chosen date take the next unused idea in `kit/classy/BACKLOG.md` (keep about four
   explainers to one comedy film, and honour any date it names, such as Diwali). Verify every fact with web searches
   first; never invent a fact, a date or a number. Write `kit/classy/specs/explainNN.json` in the **version 2** format (hook first, 3–4 scenes, 18–25 s; see
   FORMAT.md; copy one of the v2 specs explain05–12), preview it with `python3 kit/classy/preview.py kit/classy/specs/explainNN.json /tmp/pv` and look at the
   contact sheet: fix anything that wraps badly, overflows or crowds. Then render with
   `python3 kit/classy/make_classy.py kit/classy/specs/explainNN.json` and look at a few frames of the finished video and
   at the cover before scheduling.
5. **Publish and schedule.** Commit and push to `main`, then use links pinned to that commit:
   `https://raw.githubusercontent.com/eklargeoffical-ctrl/ek-large-media/<commit>/reels/<file>`. For each reel call
   Metricool `createScheduledPost`: providers [{network: instagram}], instagramData {type: REEL, showReelOnFeed: true},
   media [mp4 link], videoThumbnailUrl [ExplainNN_Cover.jpg link], text = caption from the spec (exactly five hashtags),
   publicationDate {dateTime: "YYYY-MM-DDT20:00:00", timezone: "Asia/Kolkata"}, autoPublish true, draft false. If
   Metricool refuses a post because of a plan limit, stop, keep the files, and say so in the report. Confirm with
   `getScheduledPosts`.
6. **Log and report.** Append a dated entry to `kit/log.md` (reels made, dates, Metricool ids, ideas used, fact sources)
   and push. Pull last week's numbers with Metricool `getAnalyticsDataByMetrics` (reels: reach IGRE11, views IGRE23,
   shares IGRE21, saves IGRE12, average watch time IGRE24, view rate IGRE28; followers IGEV01) and add them to the log.
   Then send the owner one short, plain message: the reels scheduled this week (date, title), last week's best reel and
   the follower count. No questions, nothing for them to do.

Never: post anything outside the window, delete or change posts you did not create in this run, change the Metricool
brand settings, use paid features or credits, promote an alcohol brand or copy its logo or label, or invent facts.
