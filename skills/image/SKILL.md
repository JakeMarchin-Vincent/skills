---
name: image
description: Generate images via MiniMax's text-to-image API. Use when asked to create, draw, render, or generate an image, logo, illustration, icon, OG image, or hero picture.
---

# /image — MiniMax text-to-image generation

Calls MiniMax's `text-to-image` endpoint. Auth via `MINIMAX_API_KEY` env var (set in `~/.zshrc`). Endpoint: `POST https://api.minimax.io/v1/image_generation`, model `image-01`.

## Usage

`/image <prompt>` — generates 1 image (1:1, URL) and prints the URL.

`/image <prompt> --n 4 --ratio 16:9` — generates 4 images at 16:9.

## Implementation

```bash
PROMPT="$1"; N=1; RATIO="1:1"
# parse --n and --ratio if present
[ "${2:-}" = "--n" ] && N="${3:-1}"; [ "${4:-}" = "--ratio" ] && RATIO="${5:-1:1}"

curl -sS -X POST "https://api.minimax.io/v1/image_generation" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" --argjson n "$N" --arg r "$RATIO" \
    '{model:"image-01", prompt:$p, n:$n, aspect_ratio:$r, response_format:"url"}')"
```

## Notes

- Image URLs expire in 24h — download immediately if persistence is needed.
- `prompt_optimizer: true` is worth enabling for short/rough prompts.
- Status codes: 0=ok, 1002=rate, 1004=auth, 1008=balance, 1026=sensitive, 2013=bad params, 2049=bad key.
- Aspect ratio options: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9. Or set width/height (512–2048, divisible by 8).
- For logos / favicons: ask for transparent background, flat design, no gradients. MiniMax doesn't have a transparency flag — composite onto a transparent or white BG downstream (sharp/sips/imagemagick).
