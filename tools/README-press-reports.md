# From the Press (assets/reports.json)
Refresh: `python3 tools/press_feeds.py` lists current headlines from public RSS (Guardian, BBC, NYT, Al Jazeera; Washington Post feeds return empty/blocked).
Then rewrite 8 to 12 items in your own words into assets/reports.json:
{"outlet","t" (DD Mon YYYY, HH:MM GMT),"url","title","summary"}. Rules: no copied sentences, credit outlet with link, no hyphens/dashes, no UAE/Dubai, no images.
Commit: git pull --rebase; git add assets/reports.json; git commit; git push. Only this file changes, so it does not collide with posts.json.
