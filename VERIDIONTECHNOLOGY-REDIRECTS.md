# Retiring veridiontechnology.com

That domain cannot simply be switched off. **Six paths on it are reached from
three live App Store listings**, and the fields naming them are frozen — Apple
refuses to edit `supportUrl`, `marketingUrl` (`409 STATE_ERROR`) or
`privacyPolicyUrl` (`INVALID_STATE`) on a version that is already on sale.
They can only be corrected in each app's next submission.

Until then, turn the domain into a pure redirector. It runs on **Netlify**,
which does real 301s, so this is a `_redirects` file at the site root:

    /ssh-terminal-privacy   https://veridion-llc.com/apps/terminal/privacy    301!
    /ssh-terminal-support   https://veridion-llc.com/support                  301!
    /ssh-terminal           https://veridion-llc.com/apps/terminal/           301!
    /support.html           https://veridion-llc.com/support                  301!
    /privacy.html           https://veridion-llc.com/apps/hoa-board/privacy   301!
    /*                      https://veridion-llc.com/apps/                    301!

The `!` forces the rule even where a file of that name still exists, so the old
pages stop serving without having to delete them.

Every destination is live and returns 200. `/apps/hoa-board/privacy` was
republished here on 31 August 2026 from the original policy — same terms, with
the publishing entity renamed to Veridion LLC.

## Which listings still point at the old domain

| App | Field | Points at | Should become |
|---|---|---|---|
| SSH Terminal | `supportUrl` | `/ssh-terminal-support` | `veridion-llc.com/support` |
| SSH Terminal | `marketingUrl` | `/ssh-terminal` | `veridion-llc.com/apps/terminal/` |
| SSH Terminal | `privacyPolicyUrl` | `/ssh-terminal-privacy` | `veridion-llc.com/apps/terminal/privacy` |
| Studio Sentinel | `marketingUrl` | `/` | `veridion-llc.com/apps/studio-sentinel/` |
| HOA Board | `supportUrl` | `/support.html` | `veridion-llc.com/support` |
| HOA Board | `marketingUrl` | `/` | `veridion-llc.com/apps/hoa-board/` |
| HOA Board | `privacyPolicyUrl` | `/privacy.html` | `veridion-llc.com/apps/hoa-board/privacy` |

Set these when submitting each app's next version. Once all three have shipped,
the redirects can go and the domain can lapse.

**Studio Sentinel's `privacyPolicyUrl` is a separate problem** — it points at
`govmed.github.io/MacSentinelAgent/privacy.html`, a raw GitHub URL on a paid
app. It needs a page here too, and the same next-submission treatment.
