# Ek Large production log

## 15 Oct 2026 (set up in chat)
- Posted by owner: Post 1 Meet Large Sahab (pinned), Reel 01 Large Sahab Disapproves.
- Scheduled in Metricool (8:00 pm IST): Reel 02 Ghar Party Bingo (15 Oct), Reel 03 Friday Night Species, Field Guide No. 01 (16 Oct), Reels 04–08 (17–21 Oct, specs in kit/specs).
- Carousels ready for the owner (1:00 pm): Ghar Party Bingo (15 Oct), Patiala Peg (17 Oct), Chakna Tier List (20 Oct), Bar Cart Starter Kit (22 Oct, carousels/Car22_BarCartStarterKit).
- Used jokes/crimes so far: ice in single malt, cola in good whisky, "bottoms up", cucumber as chakna, drinking and driving, calling every whisky Scotch, clinking till the glass chips, bottle open all night, empty stomach, "I'm fine to drive".
- Metricool ids (15 Oct): 02=396576456, 03=396576491, 04=396592235, 05=396592295, 06=396592353, 07=396592406, 08=396592444. All confirmed PENDING at 20:00 IST on their dates.
- Next free numbers: Reel 09, Field Guide No. 02 (Fri 23 Oct).

## 15 Oct 2026 (autopilot, window Thu 22 – Mon 26 Oct)
- Scheduled in Metricool (8:00 pm IST, autoPublish): Reel 09 Daru Dictionary No. 02: Tasting Words (22 Oct), Reel 10 Field Guide No. 02: Friday Night Species (23 Oct), Reel 11 Whisky Glass Tier List (24 Oct), Reel 12 Large Sahab Disapproves No. 03 (25 Oct), Reel 13 Ghar Party Guest Etiquette (26 Oct).
- Metricool ids: 09=396656395, 10=396656499, 11=396656564, 12=396656603, 13=396656623. All confirmed PENDING at 20:00 IST on their dates.
- Carousel made for the owner (1:00 pm): Ghar Party Host's Checklist (Sat 24 Oct, carousels/Car24_GharPartyHostChecklist). Thu 22 Oct already had Bar Cart Starter Kit. No Tuesday in this window.
- New jokes/crimes used: dram/nose/finish/cask strength; Selfie Sommelier, Bill Vanisher, Story Repeater, Hug Distributor, Cab Captain; paper cup / steel glass / tulip glass ranking; bottle stored on its side, topping up without asking, sniffing like a bloodhound, finishing the last peg "so it's not wasted", pushing a friend who said no; guest rules (empty-handed, host's best bottle, clear one round, host yawning, "reached home" text); host checklist (water station, real glasses, dinner by ten, sofa made up, check how everyone gets home).
- Plan count: 12 reels scheduled via Metricool for October so far.
- Next free numbers: Reel 14, Field Guide No. 03 (Fri 30 Oct), Disapproves No. 04, Daru Dictionary No. 03.

## 15 Oct 2026, 8 pm (cover fix)
- Reel 02 went live without its cover: Instagram ignored the separate cover image (videoThumbnailUrl).
- Fix: the cover is now frame 0 of every reel (make_reel.py, kit/add_cover_frame.py for old files) and Metricool posts use videoCoverMilliseconds 0. Reels 03–13 re-encoded and their Metricool posts updated (new ids below).
- Owner did not want the cover inside the video, so this was undone the same evening (see next entry).

## 15 Oct 2026, 8:30 pm (separate thumbnails)
- New: kit/thumb.html + kit/make_thumb.py make a separate poster thumbnail per reel (reels/ReelNN_Thumb.jpg); `thumb` added to specs reel04–13, plus specs/thumb02.json and thumb03.json.
- Reel videos 03–13 restored to the clean versions (no cover frame). Metricool posts 03–13 updated to the clean video + videoThumbnailUrl = the new thumbnail (ids in the next line).
- Metricool ids after the thumbnail update (all PENDING 20:00 IST, clean video + new thumbnail): 03=396906273, 04=396906390, 05=396906444, 06=396906508, 07=396906570, 08=396906630, 09=396906734, 10=396906839, 11=396906892, 12=396906943, 13=396907003.
- Watch: Reel 02 ignored its cover. Check on 16 Oct that Reel 03 shows Reel03_Thumb.jpg as its cover.

## 18 Oct 2026 (autopilot, Sunday run)
- Window: day after the last scheduled reel (Mon 26 Oct, Reel 13) up to Mon 26 Oct = empty. Nothing new made or scheduled.
- Checked in Metricool (getScheduledPosts 18 Oct – 8 Nov): 9 reels PENDING at 20:00 IST, 18–26 Oct (ids 396906444 … 396907003), all as logged on 15 Oct. No changes made.
- Carousels: none due (no Tue/Thu/Sat in the window). Already with the owner: Car22 Bar Cart Starter Kit (Thu 22 Oct), Car24 Ghar Party Host's Checklist (Sat 24 Oct). Tue 20 Oct = Chakna Tier List (from 15 Oct).
- Next run (Sun 25 Oct): window Tue 27 Oct – Mon 2 Nov. Next free numbers unchanged: Reel 14, Field Guide No. 03 (Fri 30 Oct), Disapproves No. 04, Daru Dictionary No. 03. Carousels due Tue 27, Thu 29, Sat 31 Oct.

## 22 Oct 2026 (new format: Large Sahab Productions films)
- Owner's decision: fully automatic, no voiceover, no ElevenLabs credits, no carousels, owner not involved. Engine in kit/film (FORMAT.md, BACKLOG.md); autopilot rewritten for films with a 20-posts-per-month Metricool cap.
- Why: 8 slide reels gave 2 followers; 65–90% swiped away in 3 s; average watch 2–4 s of 30 s.
- Films made: 01 Bas Ek (Fri 23 Oct), 02 Main Theek Hoon (Sat 24), 03 Papa Ko Mat Batana (Sun 25), 04 Chakna Chor (Mon 26). They replace old-style Reels 10–13 in the same Metricool slots.
- Backlog next: 05 Cab Book Kar, 06 Ek Gaana Aur, 07 Last Wala, 08 Shaadi Ka Bar Counter, 09 Mummy Aa Gayi, 10 Bas 10 Minute (Sun 1 Nov), 11 Diwali Ki Raat (Fri 6 Nov).
- October Metricool count after this: 12 (Reels 02–09 + Films 01–04); room for 8 more in October.
- Metricool ids (Films 01–04, PENDING 20:00 IST, cover = FilmNN_Thumb.jpg): 01=403006528 (23 Oct), 02=403006582 (24 Oct), 03=403006658 (25 Oct), 04=403006712 (26 Oct).

## 22 Oct 2026, evening (new format: Large Sahab Explains, the classy style)
- Owner reviewed the poster films ("they look alike… transitions too fast… keep the music low") and approved a classy sample instead: slow explainers with gold line-art, low lounge jazz, a designed cover for every reel, SEO captions, a mix of facts (spirits, Indian whisky, brand history and name meanings, cocktails, etiquette) and some comedy. No voiceover, no paid credits, no logos or bottle photos.
- Engine: kit/classy (classy.html, make_classy.py, preview.py, FORMAT.md, BACKLOG.md). Autopilot (kit/AUTOPILOT.md and the scheduled task prompt) switched to this format. kit/film is retired.
- Instagram now allows five hashtags per post: every caption has exactly five.
- Made and scheduled (20:00 IST, cover = ExplainNN_Cover.jpg via videoThumbnailUrl):
  - Explain01 What’s actually in your glass? (WhatsInYourGlass) · Thu 22 Oct · Metricool 403087303
  - Explain02 5 whisky myths you still believe (WhiskyMyths) · Fri 23 Oct · Metricool 403087373
  - Explain03 How whisky came to India (WhiskyCameToIndia) · Sat 24 Oct · Metricool 403087589
  - Explain04 Why does tonic say ‘Indian’? (GinAndTonicStory) · Sun 25 Oct · Metricool 403087810
  - Explain05 What whisky names actually mean (WhiskyNamesMeaning) · Mon 26 Oct · Metricool 403087879
  - Explain06 Scotch, Bourbon or Irish? (ScotchBourbonIrishQuiz) · Tue 27 Oct · Metricool 403087976
  - Explain07 Taste whisky like a pro (TasteWhiskyLikeAPro) · Wed 28 Oct · Metricool 403088024
  - Explain08 Is your whisky really whisky? (IsYourWhiskyReallyWhisky) · Thu 29 Oct · Metricool 403088128
  - Explain09 The Old Fashioned, explained (OldFashionedExplained) · Fri 30 Oct · Metricool 403088198
  - Explain10 Bas ek. (BasEk) · Sat 31 Oct · Metricool 403092862
- At the owner's request (17:44) Explain 01 went to tonight, 22 Oct, replacing the old-style Reel 09 (Daru Dictionary No. 02, never posted), and every reel moved up a day. Films 01–04 were replaced in their Metricool slots; Films 05–09 were never made. Metricool updates keep the uuid and change the id; the ids above are current.
- Fact sources: Wikipedia (Indian whisky, Kasauli Brewery and Distillery, Amrut, Indri, Indian Malt Whisky Association, Tonic water, Gin and tonic, Cocktail, Old fashioned, Bourbon whiskey, Irish whiskey, Johnnie Walker), Scotch Whisky Regulations 2009 and SWA guidance (3 years in oak; E150a allowed), Inside Science on the 2017 water-in-whisky study, Business Wire (Indri Best in Show 2023), Diageo India (Godawan 100, Single Malt Whisky of the Year, London Spirits Competition 2024), IBA (Old Fashioned), Cocktail Society and Country Life (G&T history), Mental Floss and The Scotsman (Gaelic name meanings).
- Note for later: in June 2026 the Indian Malt Whisky Association launched a certification seal for Indian single malt (search results; verify before using).
- Plan count: October = 17 Metricool posts (Reels 02–08 + Explain 01–10). November = 0 so far.
- Next autopilot (Sun 25 Oct): window is Sun 1 – Mon 2 Nov → BACKLOG ideas 11 and 13 (keep 12, Diwali Ki Raat, for 5–7 Nov, made by the 1 Nov run).
- Review page for the owner: https://claude.ai/artifact/YQ8BtaZTLjTq8NknANeipP · calendar: https://claude.ai/artifact/KpYyJf9qYzeFieeMt6FCB4
