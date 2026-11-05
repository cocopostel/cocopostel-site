#!/usr/bin/env python3
"""Build static report pages, Open Graph images, sitemap and robots.txt.

Reads assets/reports.json and writes:
  r/<slug>/index.html
  assets/og/<slug>.png
  assets/og/default.png
  sitemap.xml
  robots.txt

Removes stale r/<slug>/ directories not present in reports.json.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    raise SystemExit("Pillow required: pip install Pillow") from e

ROOT = Path(__file__).resolve().parents[1]
REPORTS_JSON = ROOT / "assets" / "reports.json"
R_DIR = ROOT / "r"
OG_DIR = ROOT / "assets" / "og"
AVATAR = ROOT / "assets" / "avatar.jpg"
SITE = "https://cocopostel.com"
CSS_V = "59"
JS_V = "59"

# Brand colours matching style.css
INK = (18, 18, 18)
CREAM = (250, 247, 240)
ACC = (179, 38, 30)
MUTE = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_DISP = Path(
    "/usr/share/fonts/truetype/sand-box/google/Playfair Display/"
    "PlayfairDisplay-VariableFont_wght.ttf"
)
FONT_SERIF_BOLD = Path(
    "/usr/share/fonts/truetype/sand-box/google/Crimson Text/CrimsonText-Bold.ttf"
)
FONT_SANS = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")
FONT_SANS_REG = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")
FONT_FALLBACK = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")


def load_font(path: Path, size: int, weight: int | None = None):
    p = path if path.exists() else FONT_FALLBACK
    font = ImageFont.truetype(str(p), size=size)
    if weight is not None and hasattr(font, "set_variation_by_axes"):
        try:
            font.set_variation_by_axes([weight])
        except Exception:
            pass
    return font


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def esc_text(s: str) -> str:
    return html.escape(s or "", quote=False)


def desc200(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    if len(s) <= 200:
        return s
    cut = s[:197].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def parse_gmt(t: str) -> str:
    """Return ISO 8601 UTC from '05 Nov 2026, 03:47'."""
    try:
        dt = datetime.strptime(t.strip(), "%d %b %Y, %H:%M")
        return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def wrap_lines(draw, text: str, font, max_width: int, max_lines: int = 5) -> list[str]:
    words = (text or "").split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
            if len(lines) >= max_lines:
                break
    if len(lines) < max_lines:
        lines.append(cur)
    else:
        # Truncate last line
        last = lines[-1]
        while draw.textlength(last + "…", font=font) > max_width and len(last) > 3:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last.rstrip(".,;:") + "…"
    return lines


def circular_avatar(size: int = 72) -> Image.Image:
    img = Image.open(AVATAR).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def make_og(title: str, out_path: Path, subtitle: str | None = None) -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top red accent bar
    draw.rectangle([0, 0, W, 10], fill=ACC)
    # Bottom ink bar
    draw.rectangle([0, H - 14, W, H], fill=INK)
    # Left red stripe
    draw.rectangle([0, 10, 8, H - 14], fill=ACC)

    # Brand row
    avatar = circular_avatar(78)
    img.paste(avatar, (56, 48), avatar)
    brand_font = load_font(FONT_DISP if FONT_DISP.exists() else FONT_SERIF_BOLD, 42, 900)
    tag_font = load_font(FONT_SANS_REG if FONT_SANS_REG.exists() else FONT_SANS, 22)
    draw.text((152, 58), "CocoPostel News", font=brand_font, fill=INK)
    draw.text((152, 108), "Independent reporting", font=tag_font, fill=MUTE)

    # Divider under brand
    draw.line([(56, 160), (W - 56, 160)], fill=ACC, width=3)

    # Headline
    head_font = load_font(FONT_DISP if FONT_DISP.exists() else FONT_SERIF_BOLD, 54, 700)
    lines = wrap_lines(draw, title, head_font, W - 112, max_lines=4)
    y = 200
    for line in lines:
        draw.text((56, y), line, font=head_font, fill=INK)
        y += 66

    if subtitle and y < H - 80:
        sub_font = load_font(FONT_SANS_REG if FONT_SANS_REG.exists() else FONT_SANS, 24)
        sub_lines = wrap_lines(draw, subtitle, sub_font, W - 112, max_lines=2)
        y += 10
        for line in sub_lines:
            draw.text((56, y), line, font=sub_font, fill=MUTE)
            y += 32

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)


def body_paras(body: str) -> str:
    parts = [p.strip() for p in re.split(r"\n\s*\n", body or "") if p.strip()]
    return "\n".join(f"<p>{esc_text(p)}</p>" for p in parts)


def share_markup(slug: str, title: str) -> str:
    u = f"{SITE}/r/{slug}/"
    eu = html.escape(u, quote=True)
    et = html.escape(title, quote=True)
    # percent-encode for share intent URLs (basic)
    from urllib.parse import quote

    q_u = quote(u, safe="")
    q_t = quote(title, safe="")
    return f"""<div class="share" data-slug="{esc(slug)}"><span class="share-label">Share</span>
 <a class="sb" href="https://x.com/intent/post?text={q_t}&amp;url={q_u}" target="_blank" rel="noopener">X</a>
 <a class="sb" href="https://wa.me/?text={q_t}%20{q_u}" target="_blank" rel="noopener">WhatsApp</a>
 <a class="sb" href="https://t.me/share/url?url={q_u}&amp;text={q_t}" target="_blank" rel="noopener">Telegram</a>
 <a class="sb" href="https://www.facebook.com/sharer/sharer.php?u={q_u}" target="_blank" rel="noopener">Facebook</a>
 <button class="sb" type="button" data-act="link">Copy link</button>
 <button class="sb" type="button" data-act="text">Copy report</button>
 <button class="sb native" type="button" data-act="native" hidden>More</button></div>"""


def page_html(r: dict) -> str:
    slug = r["slug"]
    title = r["title"]
    summary = r["summary"]
    body = r.get("body") or ""
    t = r.get("t") or ""
    desc = desc200(summary)
    url = f"{SITE}/r/{slug}/"
    img = f"{SITE}/assets/og/{slug}.png"
    published = parse_gmt(t)
    return f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · CocoPostel News</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CocoPostel News">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{esc(img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta property="article:published_time" content="{esc(published)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(img)}">
<link rel="icon" href="/assets/avatar.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&amp;family=Inter:wght@400;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v={CSS_V}"></head><body>
<div class="topbar wrap"><span id="dateline"></span><span>All times GMT</span><a class="btn sm" href="https://x.com/CocoPostel" target="_blank" rel="noopener">Follow on X</a></div>
<header class="masthead wrap"><img src="/assets/avatar.jpg" alt="CocoPostel avatar" width="64" height="64"><div><h1><a href="/">CocoPostel News</a></h1><p class="motto">Power. Oil. Conflict. Clarity without the noise.</p></div></header>
<nav class="sections wrap" id="tabs"><a href="/#press" class="press-tab">From the Press</a><a href="/">Top stories</a><a href="/#live">Live from X</a><a href="/#about">About</a></nav>
<main class="wrap">
<article class="report">
<p class="back"><a href="/#press">← Back to From the Press</a></p>
<div class="kick">Report</div>
<h1 class="report-title">{esc_text(title)}</h1>
<div class="meta report-meta">{esc_text(t)} GMT · London</div>
<div class="report-standfirst">{esc_text(summary)}</div>
<div class="report-body">
{body_paras(body)}
</div>
{share_markup(slug, title)}
</article>
</main>
<footer class="wrap"><div class="fm">CocoPostel News</div><a class="btn" href="https://x.com/CocoPostel" target="_blank" rel="noopener">Follow @CocoPostel on X</a><p class="small">Design is original; no affiliation with other publications.</p></footer>
<script>window.__REPORTS=window.__REPORTS||[];</script>
<script src="/script.js?v={JS_V}"></script>
<script>
fetch('/assets/reports.json?v='+Date.now()).then(r=>r.json()).then(R=>{{window.__REPORTS=R;}}).catch(()=>{{}});
(function(){{var n=document.querySelector('.share .native'); if(n && navigator.share) n.hidden=false;}})();
</script>
</body></html>
"""


def write_sitemap(slugs: list[str]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{SITE}/</loc><lastmod>{now}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>"]
    for s in slugs:
        urls.append(
            f"  <url><loc>{SITE}/r/{s}/</loc><lastmod>{now}</lastmod>"
            f"<changefreq>daily</changefreq><priority>0.8</priority></url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    reports = json.loads(REPORTS_JSON.read_text(encoding="utf-8"))
    if not isinstance(reports, list):
        raise SystemExit("reports.json must be a list")

    OG_DIR.mkdir(parents=True, exist_ok=True)
    R_DIR.mkdir(parents=True, exist_ok=True)

    # Default OG for home
    make_og(
        "Power. Oil. Conflict.",
        OG_DIR / "default.png",
        subtitle="Independent news and analysis from CocoPostel News",
    )

    keep: set[str] = set()
    for r in reports:
        slug = r["slug"]
        if not re.fullmatch(r"[a-z0-9\-]+", slug):
            raise SystemExit(f"bad slug: {slug!r}")
        keep.add(slug)
        make_og(r["title"], OG_DIR / f"{slug}.png", subtitle=desc200(r.get("summary") or ""))
        out_dir = R_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page_html(r), encoding="utf-8")

    # Remove stale report dirs
    for child in list(R_DIR.iterdir()):
        if child.is_dir() and child.name not in keep:
            shutil.rmtree(child)

    # Remove stale OG images (keep default.png)
    for png in OG_DIR.glob("*.png"):
        if png.name == "default.png":
            continue
        if png.stem not in keep:
            png.unlink()

    write_sitemap(sorted(keep))
    write_robots()
    print(f"built {len(keep)} reports → r/, assets/og/, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
