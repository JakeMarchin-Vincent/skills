---
name: design-polish
description: >
  Thin coordinator for the 5a/5b/5c design-polish model. Picks the tier
  from context and invokes the real skills (lepepai-brand, frontend-design,
  theme-factory, brand-guidelines, emil-design-eng). The vault doc
  ~/Documents/Claude Vault/Topics/Claude Core Workflows.md §2 step 5
  is the policy; this skill is just the operational surface. If they
  drift, the vault wins. Use when writing, reviewing, or polishing any
  LepepAI UI slice.
---

# /design-polish

Thin coordinator. Picks the tier, invokes the real skills, points at
the catalog. **Does not paraphrase the rules** — the real skills have
the rules. This skill's only job is to route.

## When to invoke which tier

Pick by context, not by the operator asking for a number:

- **Writing or editing a UI component now** → 5a
- **Just finished implementing a UI slice** → 5b
- **Operator said "needs extra polish" / "this is a hero surface"** → 5c

If unsure, ask one AskUserQuestion. Never skip 5a on a UI slice.

## 5a — always-on baseline (every UI slice, write-time)

**Invoke:** `lepepai-brand`

**Apply at write-time, every UI slice:**
- Brand tokens (color, type, motion) — never raw hex, never default fonts
- The 5a baseline rules from `lepepai-brand` § "5a baseline-ui"
- Run the grep from `docs/design-handbook/03-anti-slop/checklist.md`
  before commit

That's it. The skill has the rules.

## 5b — polish pass (post-implementation, every UI slice)

**Invoke (in order):**
1. `lepepai-brand` — confirm the slice stays on brand
2. `docs/design-handbook/03-anti-slop/taste-review.md` — read the 5
   review questions, answer each for the slice
3. Browser-use verify — `~/browser-use/run.py "<surface> at desktop + mobile"`,
   read the PNGs, fix what fails

**Output:** a punch list of issues found + the fixes applied. If the
punch list is non-empty, fix and re-verify. Commit when the punch list
is empty.

## 5c — high-craft (operator calls)

**Invoke (in order):**
1. `frontend-design` (Anthropic) — the aesthetic direction + anti-slop
   doctrine
2. `theme-factory` (Anthropic) — sample or mutate a reference theme for
   inspiration
3. `lepepai-brand` — apply the lepepai tokens on top
4. Hand-craft the typography pairing, the motion, the empty/loading/
   error states
5. `emil-design-eng` — review the motion (animation, easing, transitions)
6. `docs/design-handbook/03-anti-slop/taste-review.md` — full review
7. Browser-use verify at multiple sizes

**Output:** the polished slice + screenshot + a note of which skills
informed each design decision.

## Skip list

Skip these (per the vault doc):
- Anything that pulls toward more motion without restraint
- Anything with GSAP / SwiftUI / Vue / Svelte stack assumptions
- Templates, themes, "starter kits" — the visual + brand is ours
- The Next.js default app look (Inter body, Geist Sans, gray palette)

## Grill-me gates

Pause and check at any tier if:
- A design decision emerges the skills can't answer
- A new component has no analogue
- The audit surfaces a design question with two taste-compliant answers
- Operator invokes /grill-with-docs for project-aware pressure-test

Don't grill on pure restraint-rule questions. Fix them.

## What this skill is NOT

- Not a rules dump — the real skills have the rules
- Not a substitute for the catalog — `docs/design-handbook/` is the
  full options
- Not the policy — the vault doc §2 step 5 is the policy
