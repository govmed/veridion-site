# veridion-site

The public website for Veridion LLC — veridion-llc.com.

Static site (no build step): Veridion front page, NewsDog and The Market
Brief show pages with press bios, and the network transparency standards.
Deployed via GitHub Pages; the domain is registered at Hostinger and
pointed here via DNS.

Content sources: press bios from `govmed/newsdog` (docs/anchor-bios.md)
and `govmed/marketbrief` (docs/*-bio.md) — public press-bio sections only,
internal character sheets never publish. Images are web-optimized copies
of each anchor's `chosen/` branding art.

Episode videos (assets/video/): **public cuts only — Patreon editions
never go on the site.** Self-hosted MP4s are fine at pilot scale (~7MB
each); when the episode count grows past a few dozen, switch the players
to TikTok/YouTube embeds or move video to a dedicated host and keep only
posters here. Every player carries AI-content + not-advice badges.

Members (added 2026-07-13): Google sign-in via Firebase Auth (project
veridion-d54e2, config in firebase-config.js — public identifiers; the
protection is the console's authorized-domains list). The member list
lives in Firebase console → Authentication → Users. Apple/Facebook/X
buttons are staged "coming soon" — each needs its own developer-account
registration before enabling as a provider.
## Structure

Two sections off the root, both on this domain — no subdomain, no extra DNS,
and the certificate already covers them:

    /apps           the software directory, with a platform filter
    /apps/ios  /apps/macos  /apps/android  /apps/windows
    /apps/<slug>    a detail page per app
    /media          the shows
    /media/dnn  /media/market-brief  /media/off-the-leash

### /apps is generated — do not hand-edit it

`tools/apps.json` is the single source of truth. Change it, then:

    python3 tools/build-apps.py

That rewrites the directory, all four platform pages and every detail page.
Adding an app is one JSON object; editing HTML under `/apps` will be
overwritten on the next build.

Facts in `apps.json` (category, platforms, price, store URL) were taken from
`itunes.apple.com/lookup`, not from memory. Re-check them against the store
when a listing changes.

Curo is the exception: it has a longer hand-written page at `/apps/curo/`,
so its record carries `links.site` and the generator skips it.

### Two URLs that must never move

`veridion-llc.com/support` and `veridion-llc.com/curo/privacy` are compiled
into the shipped Curo binary and registered in App Store Connect. They stay
at these exact paths for the life of every installed copy — which is why the
Curo *product* page moved to `/apps/curo/` while the *privacy* page did not.

Old flat URLs (`/newsdog.html`, `/marketbrief.html`, `/offtheleash.html`,
`/curo/`) are canonical + meta-refresh stubs, because Pages serves no
server-side redirects.

## Pending: App Store listings still point at veridiontechnology.com

Four shipped apps carry support/marketing URLs on the *other* domain. Apple
freezes these on a live version — `PATCH` returns
`409 STATE_ERROR: Attribute 'supportUrl' cannot be edited at this time` — so
each one can only be corrected **in that app's next version submission**:

| App | currently points at | should be |
|---|---|---|
| SSH Terminal & SFTP | `veridiontechnology.com/ssh-terminal` + `/ssh-terminal-support` | `/apps/terminal/` + `/support` |
| Studio Sentinel | `govmed.github.io/MacSentinelAgent/` (support), `veridiontechnology.com` | `/apps/studio-sentinel/` + `/support` |
| HOA Board | `veridiontechnology.com/support.html` + `veridiontechnology.com` | `/apps/hoa-board/` + `/support` |
| Revenge of the Worm | `veridion-llc.com` (support), none (marketing) | `/apps/revenge-of-the-worm/` + `/support` |

Curo's marketing URL is currently its **privacy policy**, which is the wrong
field; set it to `/apps/curo/` once it is out of review.

**Until those ship, veridiontechnology.com cannot simply become a test site** —
these four paths are reached from live App Store listings:
`/ssh-terminal`, `/ssh-terminal-support`, `/support.html`, `/`. That site runs
on Netlify, which unlike GitHub Pages does real 301s, so the clean fix is to
turn it into a redirector and test somewhere else entirely.
