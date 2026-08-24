# veridion-site

The public website for Veridion LLC — veridion-llc.com.

Static site (no build step), deployed via GitHub Pages. The domain is
registered at Hostinger and pointed here via DNS.

## This repo is the hub, not the whole site

Each property has its own subdomain, its own repo, and its own
auto-provisioned certificate — GitHub Pages allows one custom domain per
repository and does not issue wildcards, so the split is one repo each:

| Host | Repo |
|---|---|
| `veridion-llc.com` | `veridion-site` (this one) — directory, Transparency, Support, Members |
| `dnn.veridion-llc.com` | `veridion-dnn` |
| `brief.veridion-llc.com` | `veridion-brief` |
| `leash.veridion-llc.com` | `veridion-leash` |
| `curo.veridion-llc.com` | `veridion-curo` |

That also gives each site its own ~1 GB Pages budget instead of one shared
across every show — DNN's video alone is over 200 MB.

**`style.css` lives here and every other site loads it from here.** It is
the one thing the five sites share; edit it once and all five follow. Each
site overrides only its accent colour, locally.

The old flat URLs (`/newsdog.html`, `/marketbrief.html`, `/offtheleash.html`,
`/curo/`) are canonical + meta-refresh stubs pointing at the subdomains,
because GitHub Pages serves no server-side redirects.

### Two URLs that must never move

`veridion-llc.com/support` and `veridion-llc.com/curo/privacy` are compiled
into the shipped Curo binary and registered in App Store Connect. They stay
on this repo, at these paths, for the life of every installed copy.

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
