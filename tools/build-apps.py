#!/usr/bin/env python3
"""Generate /apps from tools/apps.json.

One record per app drives the directory, the four platform pages and each
detail page, so adding an app is a single edit here rather than the same
facts typed into five files that then drift.

    python3 tools/build-apps.py
"""
import json, pathlib, shutil, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "apps.json").read_text())
OUT = ROOT / "apps"

# iOS covers two devices; the rest map one to one.
PLATFORM_PAGES = {
    "ios":     ("iOS",     ["iPhone", "iPad"], "iPhone and iPad"),
    "macos":   ("macOS",   ["Mac"],            "the Mac"),
    "android": ("Android", ["Android"],        "Android"),
    "windows": ("Windows", ["Windows"],        "Windows"),
}

def e(s): return html.escape(str(s), quote=True)

def nav(depth_prefix="/"):
    return f'''<nav>
      <a href="/apps/">Apps</a>
      <a href="/media/">Media</a>
      <a href="/transparency.html">Transparency</a>
      <a href="/support.html">Support</a>
      <a href="/members.html">Members</a>
    </nav>'''

def shell(title, desc, canonical, body, extra_head=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/apps/apps.css">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site">
  <div class="wrap">
    <div class="logo"><a href="/">VERIDION <span>LLC</span></a></div>
    {nav()}
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site">
  <div class="wrap">
    <div>&copy; 2026 Veridion LLC</div>
    <div><a href="/support.html">Support</a> &middot; <a href="/apps/">All apps</a></div>
  </div>
</footer>
</body>
</html>
'''

def badges(app):
    return "".join(f'<span class="badge">{e(p)}</span>' for p in app["platforms"])

def status_pill(app):
    if app["status"] == "review":
        return f'<span class="pill pill-review">{e(app.get("statusLabel","In review"))}</span>'
    return '<span class="pill pill-live">On the App Store</span>'

def detail_url(app):
    # Curo has a full product page of its own already; do not duplicate it.
    return app["links"].get("site") or f'/apps/{app["slug"]}/'

def card(app):
    price = e(app["price"]) + (f' &middot; {e(app["priceNote"])}' if app.get("priceNote") else "")
    return f'''      <a class="app-card" href="{e(detail_url(app))}" data-platforms="{e(','.join(app['platforms']))}">
        <img src="/apps/{e(app["icon"])}" alt="" width="72" height="72" loading="lazy">
        <div class="app-card-body">
          <h3>{e(app["name"])}</h3>
          <p class="tagline">{e(app["tagline"])}</p>
          <div class="badges">{badges(app)}</div>
          <div class="app-card-meta">{e(app["category"])} &middot; {price}</div>
        </div>
        <div class="app-card-foot">{status_pill(app)}<span class="go" aria-hidden="true">&rarr;</span></div>
      </a>
'''

def directory(apps, *, title, desc, canonical, heading, lead, chips, empty_note=None):
    chip_html = ""
    if chips:
        chip_html = '''
    <div class="filters" role="group" aria-label="Filter apps by platform">
      <button type="button" class="chip is-on" data-filter="all" aria-pressed="true">All</button>
''' + "".join(
        f'      <button type="button" class="chip" data-filter="{e(p)}" aria-pressed="false">{e(p)}</button>\n'
        for p in DATA["platforms"]) + '''    </div>
    <p class="count" aria-live="polite" id="count"></p>
'''
    cards = "".join(card(a) for a in apps)
    empty = f'''    <p class="empty" id="empty" hidden>{e(empty_note or "Nothing here yet.")}</p>\n''' if True else ""
    body = f'''<div class="wrap">
  <div class="hero apps-hero">
    <h1>{heading}</h1>
    <p class="lead">{lead}</p>
  </div>
</div>

<section class="alt">
  <div class="wrap">
{chip_html}    <div class="app-grid" id="grid">
{cards}    </div>
{empty}  </div>
</section>

<section>
  <div class="wrap">
    <div class="disclosure">
      <strong>Something wrong, or something missing?</strong> Bugs, questions and
      feature requests all go to one inbox and a real person reads it.
      <a href="/support.html">Get in touch.</a>
    </div>
  </div>
</section>
'''
    script = '<script src="/apps/filter.js" defer></script>\n' if chips else ""
    return shell(title, desc, canonical, body, extra_head=script)

def detail(app):
    links = app["links"]
    ctas = []
    if links.get("appStore"):
        ctas.append(f'<a class="btn btn-primary" href="{e(links["appStore"])}">View on the App Store</a>')
    if links.get("play"):
        ctas.append(f'<a class="btn btn-primary" href="{e(links["play"])}">Get it on Google Play</a>')
    if links.get("site"):
        ctas.append(f'<a class="btn" href="{e(links["site"])}">Visit the site</a>')
    if links.get("privacy"):
        ctas.append(f'<a class="btn" href="{e(links["privacy"])}">Privacy</a>')
    ctas.append('<a class="btn" href="/support.html">Support</a>')

    feats = "".join(f'''      <div class="feature">
        <h3>{e(t)}</h3>
        <p>{e(b)}</p>
      </div>
''' for t, b in app["features"])

    shot_dir = {"terminal":"terminal","studio-sentinel":"sentinel",
                "revenge-of-the-worm":"worm","hoa-board":"hoa-board","curo":"curo"}[app["slug"]]
    alts = app.get("shotAlt") or []
    shots = "".join(
        f'      <figure><img src="/apps/assets/shots/{shot_dir}/{e(s)}" '
        f'alt="{e(alts[i]) if i < len(alts) else e(app["name"]) + " screenshot"}" loading="lazy"></figure>\n'
        for i, s in enumerate(app["shots"]))
    shots_block = f'''
<section>
  <div class="wrap">
    <h2 class="section">Screens</h2>
    <div class="shots">
{shots}    </div>
  </div>
</section>
''' if app["shots"] else ""

    price = e(app["price"]) + (f' &middot; {e(app["priceNote"])}' if app.get("priceNote") else "")
    body = f'''<div class="wrap">
  <p class="crumb"><a href="/apps/">&larr; All apps</a></p>
  <div class="hero detail-hero">
    <img class="mark" src="/apps/{e(app["icon"])}" alt="{e(app["name"])} app icon" width="112" height="112">
    <div class="copy">
      <h1>{e(app["name"])}</h1>
      <p class="lead">{e(app["tagline"])}</p>
      <div class="badges">{badges(app)}</div>
      <div class="app-card-meta">{e(app["category"])} &middot; {price} &middot; {e(app["requires"])}</div>
      <div class="ctas">{"".join(ctas)}</div>
    </div>
  </div>
</div>

<section class="alt">
  <div class="wrap">
    <p class="summary">{e(app["summary"])}</p>
    <div class="feature-grid">
{feats}    </div>
  </div>
</section>
{shots_block}'''
    return shell(f'{app["name"]} — Veridion LLC', app["summary"][:180],
                 f'https://veridion-llc.com/apps/{app["slug"]}/', body)

# ---- write everything -------------------------------------------------------
apps = DATA["apps"]
OUT.mkdir(exist_ok=True)

(OUT / "index.html").write_text(directory(
    apps,
    title="Apps — Veridion LLC",
    desc="Software from Veridion LLC for iPhone, iPad, Mac, Android and Windows.",
    canonical="https://veridion-llc.com/apps/",
    heading="Small tools,<br><em>built properly</em>.",
    lead="Five apps across iPhone, iPad, Mac and Android. Each one does a "
         "specific job and says plainly what that job is — no upsell in the "
         "middle of the work, and no claim the software can't back.",
    chips=True,
    empty_note="Nothing on that platform yet."))
written = ["apps/index.html"]

for slug, (label, match, phrase) in PLATFORM_PAGES.items():
    subset = [a for a in apps if set(a["platforms"]) & set(match)]
    d = OUT / slug; d.mkdir(exist_ok=True)
    note = (f"No {label} app has shipped yet. The ones below are on other "
            f"platforms in the meantime.") if not subset else ""
    (d / "index.html").write_text(directory(
        subset or apps,
        title=f"{label} apps — Veridion LLC",
        desc=f"Veridion LLC software for {phrase}.",
        canonical=f"https://veridion-llc.com/apps/{slug}/",
        heading=f"Apps for {e(label)}",
        lead=(note or f"Everything we make for {phrase}."),
        chips=False))
    written.append(f"apps/{slug}/index.html  ({len(subset)} apps)")

for app in apps:
    if app["links"].get("site"):      # Curo lives at its own page
        continue
    d = OUT / app["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(detail(app))
    written.append(f'apps/{app["slug"]}/index.html')

for w in written: print(f"  {w}")
