# Design Principles — Kyle's Logo House Style

Five reference logos live in `assets/sources/`. Each one demonstrates the same small set of rules. If a new logo breaks a rule, it's almost always wrong.

## The reference set

| Name     | Concept                                                                                   | Key technique                                                                 |
| -------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Margin   | A page with a thin margin line running down it                                            | `<rect>` with a `<mask>` to punch out the line                                |
| Daylight | Rounded square with a crescent-moon bite out of the top-left (sunrise emerging from dark) | Single `<path>` combining straight edges and an `A` (arc) command             |
| Takeout  | The zig-zag fold of a paper takeout bag                                                   | Single `<path>` with a `L`-heavy zig-zag top and a rounded `Q` bottom         |
| Sift     | Three stacked bars, each shorter than the last, centered                                  | Three `<rect>` elements with small `rx`                                       |
| Aria     | Three horizontal "extract lines" of varying length, middle line bolder                    | Three `<line>` elements with different `stroke-width` and tint variants      |

See `assets/previews/` for 512×512 PNGs of each. **Look at them.** The shared vibe is easier to absorb from rendered images than from raw SVG.

## The six rules

### 1. Semantic, not decorative

The shape must *mean* the word. Ask: "If I showed this logo to someone who didn't know the name, and told them one word, what word would it be?" If the answer isn't the product name (or a very close synonym), the concept is wrong.

- **Good:** Margin's vertical line reads as the margin on a piece of notebook paper.
- **Good:** Daylight's bite-out corner reads as a crescent moon or the edge of dawn.
- **Bad:** A generic "M" in a circle for Margin. The letter isn't the concept.
- **Bad:** A lightbulb for an AI product. A lightbulb is decoration, not meaning.

### 2. Primitive SVG only

Every reference logo can be written in under 10 lines of SVG using only:

- `<rect>` (with optional `rx` for rounding)
- `<circle>` / `<ellipse>`
- `<line>`
- `<path>` with simple `M / L / Q / A / Z` commands
- `<mask>` for negative space

If you find yourself reaching for intricate bezier curves (`C` commands with multiple control points), filters, or gradients to make it work, the concept is too complex. Start over with a simpler hook.

### 3. Theme-friendly color

The logo must look right on light backgrounds *and* dark backgrounds without redrawing it. Three acceptable approaches:

- `fill="currentColor"` / `stroke="currentColor"` — the parent element controls the color via CSS `color`. Use this when the logo is one solid color.
- Tailwind semantic classes — `class="fill-primary"`, `class="stroke-sky-500 dark:stroke-sky-400"`. Use this when the project has a Nuxt UI theme.
- A single hex accent — only for cases where the brand color is locked in and will never change (e.g. a client deliverable where the color is part of the contract).

Never use gradients. Never use more than two colors. If you need two, they should be a tint of the same hue (e.g. sky-500 + sky-300).

### 4. Monochrome-first

Start with one color. Add a second tint only if the concept requires visual hierarchy (like Aria's middle line being the "primary" voice). Two colors max.

The reference logos that use two colors (Aria) pair a primary with a lighter tint of the same hue, which keeps it visually one color at a glance.

### 5. Works at 16px and 400px

- Test it as a favicon (16×16). No detail should disappear.
- Test it at hero-banner size (400+). No shape should look anemic or pixelated.

Rule of thumb: no stroke thinner than 3 units in a 64-unit viewBox, no gap smaller than 4 units.

### 6. Square-ish icon, wordmark optional

The mark itself should fit in a roughly square bounding box (1:1 or close to it). The wordmark lives next to the mark in a `flex` container with a small gap — never fused into the mark.

```vue
<div class="inline-flex items-center gap-1.5">
  <LogoMark class="h-6 w-auto text-primary" />
  <span class="font-semibold tracking-tight">Name</span>
</div>
```

## The generation process

When brainstorming 5+ options for a new project:

1. Write down every **literal meaning** of the name. For "Ledger" that's: a book, ruled lines, a column of numbers, a balance scale, a horizontal shelf.
2. For each meaning, name the **most primitive shape** that captures it. Ruled lines = a few horizontal strokes. A balance scale = two rects on either side of a vertical line. Shelf = one long thin rect.
3. Reject any hook that requires illustration (e.g. "a detailed antique ledger book" — no, a few lines is enough).
4. Reject any hook that has been done a hundred times in every startup deck: lightbulbs, gears, rockets, brains with circuit patterns, infinity loops, abstract swooshes.
5. For each surviving hook, sketch the SVG mentally — if you need more than ~6 primitive shapes, simplify or drop it.
6. Aim for variety of *concept*, not variety of *color*. "The same bars in five colors" is one option. "Bars + a funnel + a magnifying glass + a grid-with-highlight + a sieve cross-section" is five.

## Anti-patterns (things that look AI-generated)

- Gradients (especially purple-to-pink)
- Glass-morphism / frosted glass
- 3D bevels and drop shadows
- Isometric cubes
- Abstract swooshes / ribbons
- Perfectly symmetric hexagons with an icon inside
- Circuit-board brain imagery
- Letterforms as the entire mark
- Two or more unrelated concepts mashed together ("it's a leaf AND a checkmark AND a bar chart")
