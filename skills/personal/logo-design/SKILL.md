---
name: logo-design
description: Design a logo for a Kyle Johnson / Monument Labs project. Use whenever the user asks for a logo, logomark, wordmark, brand mark, app icon, or favicon — or when they ask you to "design a logo for X" or "make a mark for X". Produces an HTML gallery of at least five SVG concepts in Kyle's house style (simple, clever, semantically tied to the name, renderable in pure SVG, theme-friendly), lets the user pick one, then delivers the chosen logo as a clean standalone SVG.
---

# Logo Design

A two-phase skill for designing logos in Kyle's house style: first present options, then ship the chosen one.

**Never skip the options phase.** Even if the user says "just make me a logo for X," generate the options gallery first. Kyle wants to pick.

## The house style (what "good" looks like here)

Every reference logo in `assets/sources/` follows the same rules. Read `references/design-principles.md` for the full breakdown. The short version:

1. **Semantic, not decorative.** The shape must *mean* the name. Margin = a page with a margin line. Daylight = a crescent bite out of the corner. Takeout = the zig-zag fold of a paper bag. Sift = bars narrowing like a sifter. Aria = voice lines / transcript stripes. A logo that would work equally well for any other company is the wrong logo.
2. **Primitive SVG only.** Rects, circles, lines, simple paths, arcs, masks. Nothing that requires illustration chops or hand-tuned bezier curves. If you can't describe the shape in one sentence, it's too complex.
3. **Theme-friendly color.** Use `currentColor`, `fill-primary` / Tailwind color classes, or a single accent color with a light-gray fallback. Never hardcode a gradient. The logo must look correct in dark mode without extra work.
4. **Monochrome or near-monochrome.** One strong color. If you use a second, it should be a tint of the first (e.g. sky-500 + sky-300) to suggest layers or hierarchy.
5. **Works at 16px and 400px.** No detail that disappears at favicon size. No detail that looks anemic at hero size.
6. **Square or near-square icon.** Wordmark is optional and lives beside the mark in a `flex` row with a small gap.

## Workflow

### Phase 1 — Generate options gallery

When the user asks for a logo:

1. **Clarify briefly (one question max).** Ask only the thing you can't infer: the name, what the product does, and the general vibe if it isn't obvious. If the user already gave you enough context, skip this step entirely.
2. **Brainstorm 5-8 semantic hooks** internally. For each, ask: "what does this word *literally* mean, and what is the most primitive shape that captures it?" Reject hooks that feel generic (gears, lightbulbs, rockets, brain-with-circuits — these are banned).
3. **Render the gallery** as `logo-options-{name}.html` in the current working directory. Use `assets/templates/options-gallery.html` as a starting point. Each card must show:
   - The SVG rendered at ~160px
   - A one-line caption describing the concept ("a page with a margin line")
   - A small label with the option number (1-5+)
4. **Present at least 5 options.** Aim for 6-8 if the hooks are strong. Every option must pass all six house-style rules above. Vary the *concepts*, not just the colors — five color variants of the same idea is one option, not five.
5. **Show the file path** to the user and wait for them to pick a number. Do NOT proceed to Phase 2 until they choose.

### Phase 2 — Deliver the chosen logo

Once the user picks:

1. Save the final logo as a standalone SVG at a path the user specifies (or ask). Default: `{project-root}/public/logo.svg` for Nuxt projects, otherwise `./logo.svg`.
2. Make sure the SVG uses `currentColor` or semantic Tailwind classes (`fill-primary`, `stroke-primary`, `class="fill-sky-500 dark:fill-sky-400"`) — not hardcoded hex, unless the user asked for a frozen brand color.
3. Include a brief comment at the top of the SVG explaining the concept, so future Kyle can read it in six months.
4. If the project uses Nuxt + Nuxt UI, also offer to drop a matching `AppLogo.vue` component that pairs the mark with the wordmark — see the reference patterns in `references/svg-patterns.md`.

## Reference material

- `references/design-principles.md` — the full house-style breakdown with examples.
- `references/svg-patterns.md` — copy-paste SVG techniques (mask-for-negative-space, arc-as-bite, currentColor theming, Vue component wrapper).
- `assets/sources/*.svg` — the five canonical reference logos (Margin, Daylight, Takeout, Sift, Aria).
- `assets/previews/*.png` — 512×512 PNG renders of each reference, for vision.
- `assets/templates/options-gallery.html` — the gallery template to clone for Phase 1.

**Before designing, skim `assets/previews/` to remind yourself what the house style actually looks like.** The vibe is easier to match from the rendered PNGs than from raw SVG path data.

## Common failure modes to avoid

- **Generic startup iconography.** Gradients, glass-morphism, 3D gears, abstract swooshes. If the logo would fit on a pitch-deck clip-art slide, throw it out.
- **Letterform-only marks.** A stylized "M" for Margin is lazy. The logo should show the *concept*, not the first letter.
- **Detail-overload.** If the SVG has more than ~6 shapes, you're probably illustrating instead of logo-ing.
- **Unrealized cleverness.** "It's a coffee cup, but also a data chart" — no. One clear idea per logo.
- **Skipping the gallery.** The gallery is the point of the skill. Never deliver a single logo on the first turn.
