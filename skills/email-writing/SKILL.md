---
name: email-writing
description: Write cold outreach / follow-up / close emails that read like a person, not a template. Use whenever drafting or reviewing cold email copy — Blando outreach sequences, sales intros, follow-ups, "just checking in" attempts, investor updates, partnership asks, internal memos that need to land. The goal: short sentences, named AI solutions (when pitching), no preamble, no AI slop, voice that earns the next sentence.
---

# Email-writing — write cold email that actually reads

The whole point: an email that reads well is one the recipient finishes. Every structural choice below is in service of that. If a rule produces something that scans as mass-template, drop the rule.

## The 30-second test (use this first)

Before sending any draft, read it out loud. If any sentence makes you wince — rewrite it. If a phrase is something a salesperson on a podcast would say out loud, it's wrong.

## Hard rules (never break)

1. **No preamble.** Never start with: "I hope this finds you well", "I wanted to reach out", "Just checking in", "Circling back", "Quick note", "Not sure if you've seen this". The recipient deletes these in the first 3 seconds.

2. **Never use "AI workflows" as the headline solution.** Always a NAMED AI agent — `AI Recall Coordinator`, `AI Project Brief Agent`, `AI Quoting Assistant`, `AI After-Hours Enquiry Handler`. Generic "AI workflows" reads as filler.

3. **EMVY intro is AFTER the observation, BEFORE the named solution.** Not at the top. The email must prove it was written for this recipient before you introduce yourself.

4. **Short sentences. Varied rhythm.** Most sentences under 15 words. One longer sentence per email is fine — it's the breath. Multiple long sentences in a row = the email is now work to read.

5. **No semicolons in body copy.** They signal "this was written by someone trying to sound smart". Commas or em-dashes only.

6. **No parentheticals (except for short clarifications).** `(SMS for quick nudges, email for the longer reactivation sequence)` — kill these. If the thought needs a parenthetical, it needs its own sentence or it needs to die.

7. **No exclamation marks except for warmth moments** (welcome emails, replies to a yes, holiday). Cold outreach: zero `!`.

8. **Sign-off = name + title + URL on three short lines.** `Jake / EMVY / emvyai.com`. Not paragraphs. Not `Cheers,` followed by anything other than the sign-off block.

9. **Don't bury the CTA.** If you want them to take the assessment, the URL is one line above the sign-off. No `Take the Free Assessment\nJake\nEMVY\nemvyai.com` mash-up — the button is the CTA, the URL is the fallback.

10. **No AI slop words:** leverage, utilise, delve into, in today's world, game-changer, unlock, dive deep, robust, seamless, holistic, ecosystem, synergy, revolutionary, cutting-edge. Don't even use these as scaffolding to delete later — write the email without them.

## Structure (the canonical EMVY cold-outreach shape)

**The Resend template renders the cyan CTA button + signature block for you.** Your BODY is just the prose paragraphs — do NOT include the URL or the `Jake / EMVY / emvyai.com` signature in BODY, or they'll be duplicated when the email renders.

The template does NOT add "Hey {{FIRST_NAME}}," — that goes in BODY.

```
<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Hey {firstName},</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">{OPENER — 1 sentence, industry tenure hook, em-dash to one punchy clause}</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Question for you: {PAIN QUESTION — specific to their workflow}</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Built an {NAMED AI AGENT} for {vertical} — {what it does, 1 short sentence}.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">I have created a free Mini Strategy Assessment — a short set of questions that helps you see exactly where AI could take something off your plate. Happy to share it with you.</p>
```

Template renders below BODY:
- Cyan CTA button → `{{CTA_URL}}` labelled `{{CTA_LABEL}}` (set per email)
- Signature: `{{SENDER_NAME}} / {{SENDER_TITLE}} / emvyai.com`

Total BODY length: 90–140 words. If you're over 200 words, you're padding.

## Inline `<p>` styles — REQUIRED, not optional

Resend's template strips the default `<p>` margins. Without explicit spacing, the email renders as one wall of text. Every `<p>` in BODY needs:

```html
<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">
```

Without this, the recipient sees a single block. With it, paragraphs breathe.

**Verified 2026-06-27:** first send had no inline margin → jake@emvyai.com got a single wall of paragraphs. Fix: every `<p>` in BODY gets the inline style.

## What NOT to put in BODY

- ❌ The CTA URL (the cyan button renders below the BODY)
- ❌ A plain-text fallback URL alongside the button (unless the audience is known to have image-blocking clients — most aren't, so leave it out)
- ❌ The signature block `Jake / EMVY / emvyai.com` (template renders it)
- ❌ "Cheers," before the signature (it's not in the template and would dangle)
- ✅ "Hey {firstName}," is FINE — template doesn't add it (verified 2026-06-27)

What you DO put in BODY:
- "Hey {firstName}," (template doesn't render this)
- Opener sentence
- Pain question
- Named AI agent paragraph
- Assessment pitch (canonical 2-sentence form)
- Anything else you want before the CTA

## The opener sentence

The opener has one job: prove you actually looked at them. Good openers reference:

- Years in business + their specialty (e.g. "Nearly three decades in Western Australia with design-and-construct hydraulic services")
- Reputation signal (4.8 stars across 200+ reviews, 5-chair practice, 12-person team)
- A scope they handle (design-and-construct, project coordination, multi-chair dental, after-hours enquiries)

Format: `{tenure/scope observation} — {what that means for them in one punchy clause}`. One em-dash. Two clauses max.

**Bad opener:**
> "Joondalup Family Dental with 4.8 stars across 200+ Google reviews and a hygienist team running five chairs — that's a lot of recall reminders, follow-ups after fillings, and front-desk phone tag to keep on top of while the clinicians are still in surgery."

**Good opener:**
> "Five chairs, four hygienists, and 4.8 stars across 200+ Google reviews — that's a lot of recall reminders to keep on top of while the clinicians are still in surgery."

Cut: "follow-ups after fillings", "and front-desk phone tag". Pick one thing.

## The pain question

One sentence. "Question for you: ..." then a specific scenario they actually face. Not "do you struggle with admin?" — name the scenario.

**Bad:** "How do you handle recall reminders for lapsed patients?"

**Good:** "Question for you: when a patient is six months past their last clean and the recall email has bounced, who chases them — the front-desk team between bookings, or does it just not happen?"

Two options in the question (a / or does it just not happen) — this is the trick. It surfaces the gap without preaching.

## The named AI agent paragraph

`Built an {AGENT} for {vertical} — {1 short sentence of what it does, no benefit-stacking}.`

Then ONE more sentence with the benefit if it's a clean one.

**Bad (3 sentences, parenthetical, benefit-stacking):**
> "Built an AI Recall Coordinator for multi-chair dental practices — it watches your practice management system for lapsed patients, drafts the re-engagement message in the practice's voice, and sends on the timing you've set (SMS for quick nudges, email for the longer reactivation sequence). The front desk stops playing phone tag on reminders that don't need a human, and the hygienists' books fill from patients you already have."

**Good (2 sentences, no parenthetical, one benefit):**
> "Built an AI Recall Coordinator for multi-chair dental practices — it watches the PMS for lapsed patients and drafts the re-engagement message so nothing falls through the cracks."

Cut: "in the practice's voice", "(SMS for quick nudges, email for the longer reactivation sequence)", "the front desk stops playing phone tag on reminders that don't need a human, and the hygienists' books fill from patients you already have". All benefit-stacking. Pick ONE benefit per agent.

## The assessment pitch

The pattern is FIXED:

```
<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">I have created a free Mini Strategy Assessment — a short set of questions that helps you see exactly where AI could take something off your plate. Happy to share it with you.</p>
```

Don't rephrase. Don't add value props. Don't say "2-min". The recipient knows what an assessment is. Two sentences, period.

## E2 (follow-up, 3–4 days later)

```
<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Hey {firstName},</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">No stress if the timing's off — just following up from my last one.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">The pattern I'm seeing with {INDUSTRY} businesses in {SUBURB} is {PAIN_REF — one short line}. {Specific tasks that eat hours — one short list with em-dashes}.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">We've been helping a few of them claw that time back with {NAMED AGENT}.</p>
```

The CTA button (assessment) renders below the BODY. Do NOT include "Take the 2-min assessment" in BODY — the button replaces it.

## E3 (close, 7–10 days later)

```
<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Hey {firstName},</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Last one from me — don't want to clog your inbox.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Fair warning though: we're opening up 10 spots only for our free AI Strategy Calls — normally $500, no cost to you.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">It's a 60-minute call where I show you exactly where AI could take something off your plate in your business, and we provide a full AI Strategy report tailored specifically for your business.</p>

<p style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;">Just be quick before the spots run out!</p>
```

Don't pitch in E3. It's an exit, not a value prop. The CTA button (cal.com link) renders below — do NOT include "Lock in your spot here: {CAL_LINK}" in BODY.

## Voice

- **Mate-style.** Direct, casual, no corporate filler.
- **Plain words over clever ones.** "helps" not "facilitates". "uses" not "leverages". "talks to" not "interfaces with".
- **Active voice.** "It watches the PMS" not "The PMS is monitored".
- **Numbers where they earn their place.** "4.8 stars across 200+ reviews" lands. "Over a hundred five-star ratings" doesn't.
- **Reciprocity by being useful, not by asking first.** The pain question is the gift — it names a problem they may not have named themselves.

## When reviewing a draft

Walk through this checklist. If any item fails, rewrite that sentence, not the whole email:

**Copy**
- [ ] Opens with a specific observation (not "I hope this finds you well")
- [ ] Has exactly one pain question (not three rhetorical ones)
- [ ] Names the AI solution (not "AI workflows")
- [ ] AI solution is 1–2 sentences (not 3–4 with parentheticals)
- [ ] Assessment pitch is the canonical 2-sentence form
- [ ] No "!", no AI slop words, no semicolons
- [ ] Under 200 words (under 150 ideal)
- [ ] Reads out loud without wincing

**Rendering (BODY in the Resend template)**
- [ ] Every `<p>` has inline `style="margin:0 0 18px 0;color:#ffffff;font-size:16px;line-height:1.7;"` (otherwise paragraphs collapse into a wall)
- [ ] BODY has "Hey {firstName}," (template doesn't add it)
- [ ] BODY does NOT include the CTA URL (template renders the cyan button below)
- [ ] BODY does NOT include "Jake / EMVY / emvyai.com" (template signature renders below)
- [ ] BODY does NOT start with "Cheers," or any other sign-off

**Before sending any test**
- [ ] Render the email in browser-use (screenshot), eyeball it, look for double-ups and visual density
- [ ] Confirm cyan CTA button shows below BODY
- [ ] Confirm signature block shows below CTA
- [ ] Confirm no paragraph runs into the next

## References

- `~/.hermes/profiles/blando/skills/lead-generation/emvy-lead-generation/references/cold-email-research.md` — benchmarks, reply-rate lifts, what kills reply rates
- `~/.hermes/profiles/blando/templates/outreach-sequence.md` — canonical E1/E2/E3 templates (canonical word-for-word fallback)
- `~/.hermes/profiles/blando/templates/RESEND-TEMPLATES.md` — Resend template IDs + variables contract
