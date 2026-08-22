# video.eidosagi.com

Public player for **ident-v6** plus mute scene stills. Hostkey + Caddy, same path as [shipr.eidosagi.com](https://shipr.eidosagi.com). Scroll method copied from [volta.eidosagi.com](https://volta.eidosagi.com).

Public reel argues reprints stay cheap because the ident lives in prims (`prim.scene`, `prim.video`, `prim.obf`, `prim.opf`, `prim.docket`), not session memory or a deck. Capture is video-3d-forge, not a prim.

Source mp4 is not in git (`site/*.mp4`). Encode a web copy with `+faststart` before rsync. Poster, stills, fonts, and CSS ship in this directory — rsync the whole tree except README.

## Deploy

```bash
# from this directory
rsync -avz --exclude README.md ./ hostkey:manyhats-host/status/video/
ssh hostkey 'docker exec manyhats-host-caddy-1 caddy reload --config /etc/caddy/Caddyfile'
```

DNS: A `video` → `162.120.18.7` (DNS only) on Cloudflare **Eidos AGI**.

Caddy site block lives in `manyhats-host/Caddyfile` and `eidos-infra/machines/hostkey-epyc-56223/Caddyfile`.
