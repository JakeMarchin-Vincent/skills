---
name: polish-slice
description: One-shot slice polisher. Loads a slice from a Pocock issue, runs the right tier (5a write-time / 5b close / 5c hero), browser-use verifies, hands back a screenshot + summary. Use this skill whenever the operator says "polish [slice]" or names an issue, or when the operator wants the 5b/5c gates fired automatically. Compresses the "polish any slice" loop to one prompt.
---

# /polish-slice

One-shot slice polisher. Loads the slice context, runs the right tier,
browser-use verifies, hands back the artifact. Operator approves →
commit.

## When to invoke

- "polish [slice-name]"
- "polish issue #N"
- "polish the [page/component]"
- Operator wants the 5b sweep on a closed slice
- Operator wants a 5c review on a hero surface

## Inputs (in priority order)

1. **Issue number** — `polish-slice #12` → reads the issue body, uses
   the polish-issue template fields
2. **Slice name** — `polish-slice "history page"` → greps the repo
   for the surface
3. **File path** — `polish-slice app/(main)/history/page.tsx` → polish
   that file in context

If nothing is given, ask one AskUserQuestion. Never guess.

## What it does

### Step 1 — Load context

- Read the issue body if `#N` was given
- Read the surface files (page + components + styles)
- Read the relevant design-handbook topic (e.g. `01-components/buttons.md`
  for a button polish)
- Check git log for recent commits to the surface (avoid redoing work)

### Step 2 — Pick the tier

From the issue's `tier:` field if present, else infer:

| Signal | Tier |
|---|---|
| Surface is in active development (recent commits, half-written) | **5a** at write-time, then 5b at close |
| Surface is feature-complete, needs polish | **5b** |
| Surface is brand / hero (Logo, landing, dashboard, dialog, command palette) | **5c** |
| Surface was just shipped, needs a re-check | **5b** |

### Step 3 — Run the tier

- **5a:** apply the baseline from `lepepai-brand` § "5a baseline-ui"
  while writing. Run the grep from `03-anti-slop/checklist.md` before
  commit.
- **5b:** invoke `lepepai-brand` + read `03-anti-slop/taste-review.md` +
  answer the 5 review questions for the slice.
- **5c:** invoke `frontend-design` + `theme-factory` + `lepepai-brand` +
  `emil-design-eng` + taste review. Heavy lift.

### Step 4 — Verify with browser-use

Always, regardless of tier:

```bash
~/browser-use/run.py "go to <slice URL>, screenshot at desktop (1440x900)
  and mobile (390x844), capture each state (default, hover, focus,
  error, empty, loading)"
```

Read the PNGs. Apply the taste review to what you see. Fix what fails.

### Step 5 — Hand back

Produce a summary:
- Tier fired (5a / 5b / 5c)
- Skills invoked
- Issues found (table: before → after → why)
- Files changed
- Screenshot path(s)
- Open questions (if any)
- Recommendation: commit / needs review / not ready

### Step 6 — Wait

Do NOT commit. Hand back to the operator. The operator approves →
operator runs the commit (or asks polish-slice to commit explicitly).

## Grading the slice close

The slice is "ready" when:
- [ ] Typecheck passes
- [ ] Lint passes
- [ ] The grep from `03-anti-slop/checklist.md` returns 0 violations
- [ ] The taste review from `03-anti-slop/taste-review.md` passes all 5
- [ ] Browser-use screenshot at desktop + mobile looks right
- [ ] Operator has approved the screenshot

If any box is unchecked, the slice isn't ready. Fix and re-verify.

## What it does NOT do

- Does not commit
- Does not push
- Does not open a PR
- Does not change the design tokens (that's foundation slice 1c)
- Does not change the Logo (that's foundation slice 1a)

It polishes within the foundation. Foundation work is its own slice.
