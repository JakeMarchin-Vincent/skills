---
name: lepepai-brand
description: LepepAI's brand source-of-truth. Apply these colors, typography, motion, and voice to every UI slice. Use this skill on every LepepAI frontend task — component, page, dialog, form, list, navigation, anything visual. The handbook at docs/design-handbook/ is the full catalog; this skill is the active ruleset. Invoke together with frontend-design for hero surfaces (5c).
---

# LepepAI Brand

## When to use

Use this skill on every LepepAI frontend task — component, page, dialog,
form, list, navigation, anything visual. Pair with `frontend-design`
(Anthropic) for hero surfaces (5c). The detailed catalog lives at
`docs/design-handbook/` in the repo; this skill is the active ruleset
to invoke.

## Brand identity

**Product:** Voice-to-build-report for site inspectors. Field workers
record voice notes on a phone visit, AI structures them into a report,
office admins receive by email.

**Voice:** Professional, considered, distinctive — not generic SaaS.
The Logo mark evokes a "site foreman's clipboard → AI" relationship.
Think Linear / Pitch / Arc Browser, not Notion / Asana.

**Quality bar:** Client-presentable. Every surface should pass the
"hand it to a client" test from `docs/design-handbook/03-anti-slop/taste-review.md`.

## Color tokens

Defined in `app/globals.css`. Apply by referencing tokens, never raw
hex. The current system:

```css
--bg: #0A0A0C;          /* page background */
--text: #f4f4f5;        /* primary text */
--text-muted: #a1a1aa;
--text-faint: #71717a;
--accent: #f59e0b;      /* amber — the brand */
```

**Missing (foundation slice 1c adds):**
- `--surface`, `--surface-raised`, `--surface-overlay`
- `--border`, `--border-strong`
- `--accent-hover`, `--accent-pressed`, `--accent-fg`
- `--severity-critical/high/medium/low`
- `--focus-ring` (use the brand accent)
- Dark + light mode pair

See `docs/design-handbook/00-foundation/color-tokens.md`.

## Typography

Loaded via `next/font` in `app/layout.tsx`:

| Role | Font | Source | Why |
|---|---|---|---|
| Display | **Fraunces** (opsz axis) | next/font/google | Distinctive transitional serif; opsz for size-appropriate optical adjustments |
| Body | **Switzer** (v1) | next/font/local (Fontshare) | Free, modern, warm, doesn't look default. Upgrade to PP Neue Montreal if budget allows. |
| Mono | **JetBrains Mono** | next/font/google | Code, IDs, technical strings |

**Banned as body sans** (per Anthropic `frontend-design` skill):
Inter, Roboto, Arial, system fonts, Space Grotesk, Geist Sans
(the "default Next.js app" look is its own kind of AI slop).

**Type scale:** 12 / 14 / 16 / 20 / 24 / 32 / 40 / 56 / 72.
Fraunces `opsz`: 14 (small) / 36 (mid) / 48 (H2) / 96+ (hero).

See `docs/design-handbook/00-foundation/typography.md` for the full
options table and the v1 call.

## Motion

Defined in `app/globals.css` (foundation slice 1d adds):

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
--ease: cubic-bezier(0.4, 0, 0.2, 1);

--duration-press: 100ms;
--duration-small: 150ms;
--duration-medium: 200ms;
--duration-large: 300ms;
```

**Restraint rule** (from `emil-design-eng`, applies always):
- 100+/day actions (command palette, keyboard shortcuts) = NO animation
- Hover effects gated behind `@media (hover: hover) and (pointer: fine)`
- `prefers-reduced-motion: reduce` removes movement, keeps opacity/color
- UI animations under 300ms
- Use `transform` + `opacity` only (GPU, interruptible)

See `docs/design-handbook/00-foundation/motion-language.md` and
`03-anti-slop/motion-restraint.md`.

## Logo

`components/Logo.tsx` is the brand mark. Current mark (foundation slice
1a shipped 2026-06-08): refined clipboard — single integrated
silhouette (board + clip as one path) with a single amber tick inside,
the "AI stamp". Two primitive SVG shapes, semantic to the product,
works at 16/32/64/128 px, theme-friendly via `currentColor` for the
mark + `var(--accent)` for the tick.

**For any Logo / favicon / app-icon / wordmark work, invoke the
`logo-design-skill` (GKjohns).** Its house style (semantic, primitive
SVG, monochrome, works at 16 and 400 px) is the source of truth — this
section is just the application of it to LepepAI's brand.

- Mark + wordmark, optical balance
- Multi-size tested (16px favicon through 64px hero)
- Dark + light variants (via `currentColor`)
- No animation on the mark itself (decorative, used 100+/day)

See `docs/design-handbook/00-foundation/brand-identity.md`.

## 5a baseline-ui (every slice, write-time)

Apply these at write-time. From `docs/design-handbook/03-anti-slop/checklist.md`:

- **No** `transition: all` — specify exact properties
- **No** `animate-*` without a request
- **No** `duration-` over 300 on UI
- **No** `ease-in` on UI (use `--ease-out`)
- **No** `scale(0)` entry (use `scale(0.95)` + `opacity: 0`)
- **No** `transform-origin: center` on popover (modals exempt)
- **No** hover without `@media (hover: hover) and (pointer: fine)`
- **No** keyframes on rapidly-triggered UI (use transitions)
- **Yes** `transform: scale(0.97)` on `:active` for buttons
- **Yes** `--ring` focus state (use the brand accent)
- **Yes** paste-friendly inputs
- **Yes** `aria-label` on icon-only buttons
- **Yes** structural skeletons for loading, not spinners-as-content
- **Yes** inline errors next to fields, not global toasts

Run the grep from `03-anti-slop/checklist.md` before any commit.

## 5b polish (every slice close)

After implementation, before commit:
1. Re-read the slice as if you'd never seen it
2. Run the taste review from `03-anti-slop/taste-review.md`
3. Browser-use verify (screenshot at desktop + mobile, every state)
4. Read the PNGs — does it look AI-generated? Does it serve a real moment?
5. Fix anything that fails. Commit when it passes.

## 5c high-craft (operator calls)

For hero surfaces — Logo, landing, dashboard, SendReportDialog,
CommandPalette, any "this is the moment" surface:
1. Invoke `frontend-design` (Anthropic) explicitly for the design doctrine
2. Invoke `theme-factory` (Anthropic) to sample / mutate a reference theme
3. Apply the lepepai brand tokens (above) on top
4. Hand-craft the typography pairing, the motion, the empty/loading/error states
5. Verify with browser-use at multiple sizes

## Pointers

- `docs/design-handbook/` — the full design catalog (21 files)
- `app/globals.css` — current tokens (partial; foundation slice 1c fills out)
- `~/Documents/Claude Vault/Topics/Claude Core Workflows.md` §2 step 5
  — 5a/5b/5c policy
- `emil-design-eng` skill — motion craft doctrine
- `frontend-design` skill (Anthropic) — anti-slop + aesthetic direction
- `theme-factory` skill (Anthropic) — 10 reference themes
- `brand-guidelines` skill (Anthropic) — brand identity structure template
