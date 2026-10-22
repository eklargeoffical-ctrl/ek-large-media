# Weekly autopilot (runs every Sunday morning, IST)

You are producing the next week of reels for the Instagram page @ek.large. The owner has asked not to be involved:
you make, upload and schedule everything yourself. Be careful: these posts go live automatically.

Since 23 Oct 2026 every reel is a **Large Sahab Productions film** (see `kit/film/FORMAT.md`). The old slide reels
(`kit/make_reel.py`) and carousels are retired. No voiceover, and never use ElevenLabs or any paid credits.

1. **Get the kit.** Attach and clone the GitHub repository `eklargeoffical-ctrl/ek-large-media` (push access).
   Read `kit/README.md`, `kit/film/FORMAT.md` and `kit/film/BACKLOG.md`. Read `kit/log.md` to see what is already made.
2. **Find the window.** Call Metricool `getBrandSettings` (brand 6288777, Asia/Kolkata) and `getScheduledPosts` from
   today to 21 days ahead. The window is every date from the day after the last scheduled reel up to and including the
   first Monday that is at least 7 days after today. If the window is empty, skip to step 6.
3. **Respect the free plan.** Metricool's free plan allows about 20 scheduled posts per calendar month. Count the posts
   already scheduled or published through Metricool in each month the window touches (from `kit/log.md` and
   `getScheduledPosts`). Never plan more than 20 in a month. When a month cannot take a film every day, pick days in
   this order: Fri, Sat, Sun, Wed, Mon, Thu, Tue.
4. **Make the films.** For each chosen date take the next unused script in `kit/film/BACKLOG.md` (or write a new one
   from its idea list, following FORMAT.md). Write `kit/film/specs/filmNN.json` (next number), preview key frames
   (0.0, 2.9, 4.6, 7.8, 9.9, 12.8 s) and fix anything that wraps, overflows or is hard to read, then render with
   `python3 kit/film/make_film.py kit/film/specs/filmNN.json`. Look at a contact sheet of the finished video
   before scheduling.
5. **Publish and schedule.** Commit and push to `main`, then use links pinned to that commit:
   `https://raw.githubusercontent.com/eklargeoffical-ctrl/ek-large-media/<commit>/reels/<file>`. For each film call
   Metricool `createScheduledPost`: providers [{network: instagram}], instagramData {type: REEL, showReelOnFeed: true},
   media [mp4 link], videoThumbnailUrl [FilmNN_Thumb.jpg link], text = caption from the spec, publicationDate
   {dateTime: "YYYY-MM-DDT20:00:00", timezone: "Asia/Kolkata"}, autoPublish true, draft false. If Metricool refuses a
   post because of a plan limit, stop, keep the files, and say so in the report. Confirm with `getScheduledPosts`.
6. **Log and report.** Append a dated entry to `kit/log.md` (films made, dates, Metricool ids, scripts used) and push.
   Pull last week's numbers with Metricool `getAnalyticsDataByMetrics` (reels: reach IGRE11, views IGRE23, shares IGRE21,
   saves IGRE12, average watch time IGRE24, view rate IGRE28; followers IGEV01) and add them to the log.
   Then send the owner one short, plain message: the films scheduled this week (date, title), last week's best film and
   the follower count. No questions, nothing for them to do.

Never: post anything outside the window, delete or change posts you did not create in this run, change the Metricool
brand settings, use paid features or credits, name or promote an alcohol brand, or invent facts.
