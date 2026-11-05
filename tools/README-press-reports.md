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
- Headlines on the site link to `report.html?id=<slug>`.
