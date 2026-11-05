# From the Press reports

Public file: `assets/reports.json` (served on GitHub Pages).
Private dedupe/meta (NOT in this repo): `/workspace/press-private/reports-meta.json`.

## Public schema (assets/reports.json)
Array of objects:
- `slug` (string, URL id, e.g. `vance-iran-war-midterms`)
- `t` (string, GMT dateline, e.g. `05 Nov 2026, 15:43`)
- `title` (string, headline, no outlet name)
- `summary` (string, standfirst / card blurb)
- `body` (string, full original report, paragraphs separated by blank lines)

NEVER include `outlet`, `url`, `via`, source names, or external article links in the public JSON or on any page.

## Private schema (/workspace/press-private/reports-meta.json)
Array of objects used only for dedupe and refresh bookkeeping:
- `slug`, `outlet`, `url`, `t`, `title`

## Writing rules
- Original words only from lawfully public text (RSS summary / public page). Never bypass paywalls.
- Prefer 250 to 400 words when enough public facts exist; else 120 to 200 from headline+summary only. Do not invent facts or quotes.
- No hyphen, en dash or em dash characters in title/summary/body.
- Never write Dubai, UAE or Emirates. British feel, GMT, lang en-GB.
- Live report URLs are clean static pages: `https://cocopostel.com/r/<slug>/` (Open Graph ready).
- Old links `report.html?id=<slug>` redirect to `/r/<slug>/`.

## After writing reports.json
Always rebuild static pages and share images, then commit the generated files:

```bash
cd /workspace/cocopostel-site
python3 tools/build_reports.py
# commits must include: r/, assets/og/, sitemap.xml, robots.txt, assets/reports.json
```

`tools/build_reports.py` writes `r/<slug>/index.html`, branded `assets/og/<slug>.png` (1200x630), `assets/og/default.png`, `sitemap.xml` and `robots.txt`, and removes stale `r/` folders for slugs no longer in `reports.json`.
