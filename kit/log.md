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
