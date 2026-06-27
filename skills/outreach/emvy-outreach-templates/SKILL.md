---
name: emvy-outreach-templates
description: Complete documentation of Blando's outreach pipeline — template design, sequence timing, state machine, brand rules, and send mechanism
category: outreach
tags: [hermes, convex, vps, blando, internal]
---

# EMVY Outreach Templates & Sequencing

**Purpose:** Document how Blando discovers leads, queues outreach sequences (E1+E2+E3), and sends emails via Resend. Source of truth for template content, timing gates, and the Convex state machine.

**Applies to:** Blando Hermes agent (VPS profile). System cron `send_outreach.py` is the only code path that calls Resend.

---

## Pipeline Architecture (3-Zone System)

| Zone | Schedule | Agent | What it does | Output |
|------|----------|-------|-------------|--------|
| **Zone 1** | `0 * * * *` (:00 hourly) | Blando (deepseek) | Discovers leads from Hipages/AussieWeb/Google, scores (6+ threshold), writes to Convex `leads` table via `upsert_lead()` | Convex leads table |
| **Zone 2** | `15 * * * *` (:15 hourly) | Blando (deepseek) | Reads uncontacted leads from Convex, generates personalised E1 + fixed E2/E3, calls `queue_sequence()` | Convex outreach_queue |
| **System cron** | `0 */2 * * *` (:00 even hours) | Python script | Runs `send_outreach.py --limit 15`, which claims due queue rows and sends via Resend raw HTML | Resend API sends |

**NEVER path:** Zone 2 generates content and writes to the queue. It MUST NEVER call Resend directly. Only `send_outreach.py` (system cron) touches the Resend API.

---

## Sequence Timing (E1 → E2 → E3)

Defined in `convex/hermes/outreach2.ts` (website repo):

```
E1: scheduledFor = now              (immediate, sends on next cron tick)
E2: scheduledFor = E1 + 4 days      (4d gap after E1 queued)
E3: scheduledFor = E2 + 6 days      (6d gap after E2 queued, so E1 + 10d total)
```

Constant definitions:
```typescript
const E2_GAP_MS = 4 * 24 * 60 * 60 * 1000  // 345,600,000 ms
const E3_GAP_MS = 6 * 24 * 60 * 60 * 1000  // 518,400,000 ms
```

Timing gates enforced at **send time** (not queue time):
- E2 will NOT send unless `lead.outreachState === "e1_sent"` AND ≥4d since E1 actually sent
- E3 will NOT send unless `lead.outreachState === "e2_sent"` AND ≥6d since E2 actually sent
- These gates are in the `claim()` mutation inside `claimAndSendStep`

---

## Template Design

### E1 — Initial Outreach (personalised per lead)

The agent generates E1 dynamically per lead with:
- Personalised opener referencing their business/industry pain point
- Named AI solution describing what we built for that sector
- Free Assessment CTA to `https://emvyai.com/assessment`

### E2 — Follow-up (fixed body, do NOT customise)

Sent 4 days after E1. Fixed body promoting EMVY's value proposition + Free Assessment CTA.

### E3 — Break-up (fixed body, do NOT customise)

Sent 6 days after E2 (10 days after E1). Final offer: free AI Strategy Call ($500 value) via `https://cal.com/jake-emvy/ai-strategy-call`.

---

## Brand Rules (ALL templates)

These apply to every email that leaves the system. Violations caused the 2026-06-26 61-email incident.

| Rule | Value | Why |
|------|-------|-----|
| **Signature name** | Jake | NEVER "Dusk" or "Dusk, EMVY AI" |
| **Brand** | EmvyAI | NOT "EMVY AI" with a space |
| **Title** | Founder - EmvyAI | NOT "Co-Founder" or any other title |
| **Background** | `#0a0a0a` (near-black) | Dark theme brand standard |
| **CTA color** | `#56d9ff` (sky cyan) | Brand accent colour |
| **CTA text** | White `#0a0a0a` on `#56d9ff` | Readability on cyan |
| **Greeting** | "Hey," | No first name — keeps it casual |
| **Reply-to** | jake@emvyai.com | NOT hello@emvyai.com |
| **From name** | Jake Marchin-Vincent | Full name per Resend sender identity |
| **From email** | jake@emvyai.com | Verified sender in Resend |
| **Domain** | emvyai.com | NOT emvy.ai (old domain) |

### HTML Structure

Every email body uses inline styles (no `<style>` tag — email client compat). Standard wrapper:

```html
<div style="background:#0a0a0a;padding:30px;font-family:Arial,Helvetica,sans-serif;color:#ffffff;max-width:600px;margin:0 auto;">
  <!-- content with inline styles on every element -->
  <p style="font-size:16px;line-height:1.6;">Body text here</p>
  <a href="..." style="background:#56d9ff;color:#0a0a0a;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px;">CTA Text</a>
</div>
```

---

## Convex State Machine

### `leads.outreachState` progression

```
null → e1_sent → e2_sent → e3_sent → complete
                ↘ unsubscribed (manual)
                ↘ do_not_contact (manual)
```

Set by `markStepSent()` mutation after Resend confirms delivery.

### `outreach_queue` status lifecycle

```
queued → sending → sent
                  ↘ failed    → retry on next cron tick
                  ↘ blocked   (manual unblock)
```

### `leads.stage` progression

```
discover → contacted → followup → breakup → engaged → interested → warm → booked
```

Updated by `markStepSent()`:
- E1 sent → `stage: "contacted"`
- E2 sent → `stage: "followup"`
- E3 sent → `stage: "breakup"`

### Queue item schema

| Field | Type | Description |
|-------|------|-------------|
| `leadId` | Id["leads"] | Foreign key to leads table |
| `touch` | 1, 2, 3 | Touch number (1=E1, 2=E2, 3=E3) |
| `status` | queued, sending, sent, failed, blocked | Current status |
| `scheduledFor` | number (ms epoch) | When this can be claimed |
| `subject` | string | Email subject line |
| `body` | string | Full HTML body |
| `claimedAt` | number (ms epoch) | When claim happened |
| `sentAt` | number (ms epoch) | When Resend confirmed |
| `resendId` | string | Resend API email ID |
| `error` | string | Error message if failed |

---

## Send Mechanism

```
  System Cron ──► send_outreach.py ──► Convex claimAndSendStep ──► Resend API
       │                                    │                           │
   0 */2 * * *                          claim() atomically          email.send()
   --limit 15                           gates check (E2/E3)         returns ID
                                         markStepSent()              updates lead
```

### `send_outreach.py` (v3 — raw HTML only)

Path: `~/.hermes/profiles/blando/bin/send_outreach.py`

Key behaviours:
- Reads due rows from Convex via `getDueSteps()` query
- Calls `claimAndSendStep()` action for each
- `claimAndSendStep` is a Convex action — claims the queue row atomically (status→sending), calls Resend, calls markStepSent
- `--dry-run` flag lists due steps without sending
- `--limit N` caps sends per run (default 30, system cron uses 15)
- Logs all activity to `logs/send_outreach.log`

### Resend API call (inside claimAndSendStep)

```typescript
await resend.emails.send({
  from: "Jake Marchin-Vincent <jake@emvyai.com>",
  to: lead.email,
  subject: queueItem.subject,
  html: queueItem.body,
  reply_to: "jake@emvyai.com",
});
```

---

## Auth & Wiring

### VPS → Convex

- `convex.py` sends `CONVEX_DEPLOY_KEY` as `Authorization: Convex <key>` header
- Every mutation/query/action call injects `agent: "blando"` + `token: <HERMES_TOKEN_BLANDO>`
- Convex `hermesAuth.ts` constant-time compares against `process.env.HERMES_TOKEN_BLANDO`
- `.env` auto-loaded at import time in `convex.py` (fix for terminal sessions missing env vars)

### Function Surface

All outreach Convex functions live under `convex/hermes/outreach2.ts`:

| Function | Type | Purpose |
|----------|------|---------|
| `queueStep` | Mutation | Queue single step for a lead (idempotent on email+step) |
| `queueSequence` | Mutation | Queue E1+E2+E3 in one call (used by Zone 2) |
| `claimAndSendStep` | Action | Claim queue row + send via Resend + update state |
| `markStepSent` | Mutation | Update lead state after successful send |
| `markStepFailed` | Mutation | Mark queue row as failed |
| `getDueSteps` | Query | Get all due (queued + scheduledFor ≤ now) rows |
| `getLeadSequenceState` | Query | Get full sequence state for a lead |
| `suppressLead` | Mutation | Unsubscribe / do_not_contact a lead |
| `resetSequenceForLead` | Mutation | Reset sequence back to start |
| `forceSendNow` | Mutation | Immediately claim and send a specific queue item |

---

## Error Handling

### Resend 422 (validation error)

Full error: `Resend send failed: 422 {"statusCode":422,"name":"validation_error","message":"..."}`

Common causes:
- Empty or malformed HTML body (body was set to "FIXED" from old v2 pipeline)
- Template ID mismatch (from old template-based pipeline)
- Invalid `reply_to` format

Resolution: Reset the queue item and re-queue with valid body.

### Convex HTTP 429 (Token Plan limit)

Full error: `HTTP 429: Token Plan usage limit reached`

The `deepseek-v4-flash` model hits plan limits when generating long outputs for many leads. The cron retries automatically on next interval (hourly). If persistent, wait for plan reset or upgrade token plan.

### Convex KeyError (env missing)

Full error: `KeyError: HERMES_TOKEN_BLANDO`

Root cause: gateway systemd service doesn't load profile `.env`. Terminal sessions from the gateway lack the env var. Fixed by `.env` auto-load at import time in `convex.py` (2026-06-27). If this reappears, check that `convex.py`'s `.env` loader is present:

```python
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
```

---

## Incident History

### 2026-06-26: 61 emails sent with wrong signature

**Root cause:** Zone 2 cron prompt was too short, agent didn't follow brand rules. Used "— Dusk, EMVY AI" signature, wrong reply_to (hello@emvyai.com), wrong CTA (15-min call instead of Free Assessment).

**Fix:** Zone 2 prompt rewritten with explicit brand rules, hardcoded E2/E3 bodies, and "NEVER call Resend directly" guardrail.

### 2026-06-27: convex.py KeyError + hallucinated Resend sends

**Root cause:** Gateway terminal sessions lacked `HERMES_TOKEN_BLANDO` env var. `convex.py` crashed on import with `KeyError`. Zone 2 agent couldn't write to Convex, so it fell back to calling Resend directly via curl.

**Fix:** `.env` auto-load at import time in `convex.py`. Also added stronger "NEVER call Resend directly" instruction to Zone 2 prompt.

### 2026-06-27: 7 E1s failed with Resend 422

**Root cause:** Leads from old v2 pipeline had `body="FIXED"` in queue rows (leftover from broken migration). Resend rejected 422 on empty/invalid HTML.

**Fix:** Reset queue items and re-queued with valid bodies. Also added template body verification step.

---

## Testing & Verification

### Dry-run mode

```bash
python3 ~/.hermes/profiles/blando/bin/send_outreach.py --dry-run
```

Lists due steps without sending. Always run before modifying templates.

### Body verification checklist

Before every campaign send, verify E1 body contains:
- [ ] Jake signature
- [ ] Dark background `#0a0a0a`
- [ ] Cyan CTA `#56d9ff`
- [ ] Free Assessment link (`emvyai.com/assessment` in body)
- [ ] No "Dusk" anywhere
- [ ] `EmvyAI` brand (not "EMVY AI")

### Queue state check

```bash
python3 ~/.hermes/profiles/blando/bin/send_outreach.py --dry-run
```

Or via convex.py directly (for SSH sessions):
```python
import sys; sys.path.insert(0, "/home/dusk/.hermes/profiles/blando")
from convex import get_due_steps
steps = get_due_steps(100)
for s in steps:
    print(s.get("email"), s.get("touch"), s.get("status"))
```
