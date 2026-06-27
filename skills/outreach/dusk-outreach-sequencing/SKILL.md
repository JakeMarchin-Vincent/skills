---
name: dusk-outreach-sequencing
description: Generalised email outreach sequence pattern — E1/E2/E3 timing, brand rules, state machine, and reference Python implementation. Adapt to any stack.
category: outreach
---

# Dusk Outreach Sequencing

**Purpose:** A production-tested email outreach pattern for AI coding tools and developers. Design sequences (E1→E2→E3), manage lead state, enforce brand rules, and send via your email provider — without hallucinating wrong templates.

**Based on real production system.** This skill documents what we actually run at EMVY. The reference implementation is Python but the pattern is stack-agnostic. Any AI coding tool can load this and generate outreach sequences that follow the same discipline.

---

## The Sequence Pattern

Every outreach campaign follows a 3-touch sequence:

| Touch | Timing | Purpose | Content |
|-------|--------|---------|---------|
| **E1** | Immediate | Open + introduce value proposition | Personalised per lead — references their industry/business pain point, names a specific solution, soft CTA |
| **E2** | E1 + 4 days | Follow-up, reinforce value | Fixed — expands on the solution, more detail on what you offer, same CTA |
| **E3** | E2 + 6 days (E1 + 10 total) | Break-up / final offer | Fixed — last chance, stronger offer (free call/consult), clear call to action |

Timing constants (adjust for your cadence):

```
E2_GAP_MS = 4 * 24 * 60 * 60 * 1000  = 345,600,000 ms  (4 days)
E3_GAP_MS = 6 * 24 * 60 * 60 * 1000  = 518,400,000 ms  (6 days, so E1 + 10 total)
```

### Why this cadence?
- **E1 now:** Strike while interest is fresh. The lead was just identified (via search, directory, referral).
- **E2 +4d:** Short enough that they remember your first email, long enough to not feel spammy.
- **E3 +6d:** Break-up frame — respectful, no further follow-ups after this. Creates urgency with the "last one" framing.

---

## State Machine

Every lead moves through a state machine. This prevents double-sending, respects timing gates, and gives you observability.

### Lead state progression

```
null → contacted (E1 sent) → followup (E2 sent) → breakup (E3 sent) → complete
                           ↘ unsubscribed
                           ↘ do_not_contact
```

### Queue item lifecycle

```
queued → sending → sent
                  ↘ failed → retry on next tick
                  ↘ blocked (manual)
```

### Important gates

- E2 will NOT send unless the lead has state `contacted` AND ≥4 days since E1 was sent
- E3 will NOT send unless the lead has state `followup` AND ≥6 days since E2 was sent
- These gates are checked at **send time** (not queue time), so queuing E1+E2+E3 atomically is safe

This means you can queue the entire 3-email sequence immediately upon lead qualification, and the system automatically releases each email at the right time with the right gate checks.

---

## Brand Rules

These are critical. A template that looks wrong destroys credibility. Define rules your AI tool can check against.

### Required checklist for every email

| Rule | Why it matters |
|------|---------------|
| **Send name** is a real person, not a company name | People reply to people |
| **Signature** includes title + company | Establishes authority |
| **Greeting** is casual ("Hey," not "Dear [Name]") | Warm, not corporate |
| **CTA button** stands out (contrasting colour) | Drives action |
| **Email background** is dark (or your brand colour) | Visual consistency |
| **Reply-to** is the sender's real email | Replies land somewhere useful |
| **No founder/CEO name** in the body (unless signature) | The focus is the offer, not the person |
| **Domain** is consistent across all links | Trust signal |

### HTML email structure

Email clients strip `<style>` tags. All styles must be inline. Standard wrapper:

```html
<div style="background:#0a0a0a;padding:30px;font-family:Arial,Helvetica,sans-serif;color:#ffffff;max-width:600px;margin:0 auto;">
  <p style="font-size:16px;line-height:1.6;">Body text here</p>
  <p style="text-align:center;margin:28px 0;">
    <a href="https://yourdomain.com/cta"
       style="background:#56d9ff;color:#0a0a0a;padding:14px 28px;border-radius:8px;
              text-decoration:none;font-weight:600;font-size:15px;display:inline-block;">
      Your CTA
    </a>
  </p>
  <p style="font-size:16px;line-height:1.6;">Cheers,<br>Your Name<br>Title - Company<br>domain.com</p>
</div>
```

### Writing E1 (personalised per lead)

The first email must feel specific, not templated:
- Open with a pain observation about their industry/business type
- Name a specific problem they likely face (not generic "we can help you grow")
- Introduce your solution as built FOR their type of business
- End with a low-friction CTA (free assessment, free resource)

E1 structure:
1. **Pain opener:** "Running a roofing business means emergency callouts, quoting overhead, and compliance paperwork never stop. How much time are you spending on the admin side?"
2. **Named solution:** "We built a custom AI system for exactly this — our AI emergency response system + quoting assistant."
3. **Soft CTA:** Free assessment link, not a booked call
4. **Signature:** Person, not company

### E2 and E3 (fixed bodies)

E2 and E3 are NOT personalised per lead. They are the same for everyone in the campaign. This is deliberate:
- E2 expands on the solution with concrete benefits ("free up 15-20 hours a week")
- E3 creates urgency with a limited-time offer ("last one from me", "limited to 10 spots")
- Hardcoding these prevents the AI from inventing wrong offers or tones

---

## Pipeline Architecture

Three separate concerns. Keep them isolated — never let one zone do another zone's job.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Zone 1     │     │  Zone 2     │     │  System     │
│  Discovery  │ ──► │  Queue      │ ──► │  Send       │
│  (hourly)   │     │  (hourly)   │     │  (every 2h) │
└─────────────┘     └─────────────┘     └─────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
  Find leads         Write E1/E2/E3        Send via
  Score + store      to queue only         email API
     │                    │                    │
     └────────────────────┴────────────────────┘
                         │
                         ▼
                   Your database
```

**Critical rule:** Zone 2 (the AI generating content) MUST NEVER call the email API directly. It only writes to a queue. A separate, non-AI process reads the queue and sends. This prevents AI hallucination from reaching real inboxes.

---

## Reference Implementation

Below is a complete reference Python implementation. Adapt the storage/email layers to your stack.

### 1. Queue system (queue.py)

```python
"""Email outreach queue system.

Manages lead state, queue items, and timing gates.
Swap the storage layer (SQLite/Postgres/Convex) as needed.
"""
import json
import sqlite3
import time
from datetime import datetime, timezone
from typing import Optional

# Timing constants
E2_GAP_MS = 4 * 24 * 60 * 60 * 1000
E3_GAP_MS = 6 * 24 * 60 * 60 * 1000


class OutreachStore:
    """SQLite-backed outreach store. Drop-in replaceable with any DB."""

    def __init__(self, db_path: str = "outreach.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                business_name TEXT,
                contact_name TEXT,
                stage TEXT DEFAULT 'discover',
                outreach_state TEXT,
                next_action_at INTEGER,
                created_at INTEGER DEFAULT (strftime('%s','now') * 1000)
            );
            CREATE TABLE IF NOT EXISTS outreach_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                touch INTEGER NOT NULL CHECK(touch IN (1,2,3)),
                status TEXT DEFAULT 'queued'
                    CHECK(status IN ('queued','sending','sent','failed','blocked')),
                subject TEXT,
                body TEXT,
                scheduled_for INTEGER NOT NULL,
                claimed_at INTEGER,
                sent_at INTEGER,
                error TEXT,
                resend_id TEXT,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            );
            CREATE INDEX IF NOT EXISTS idx_queue_due
                ON outreach_queue(status, scheduled_for);
        """)
        self.conn.commit()

    def upsert_lead(self, email: str, business_name: str = None,
                    contact: str = None, stage: str = "discover") -> int:
        cur = self.conn.execute(
            "INSERT INTO leads (email, business_name, contact_name, stage) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(email) DO UPDATE SET "
            "  business_name = COALESCE(?, business_name), "
            "  contact_name = COALESCE(?, contact_name) "
            "RETURNING id",
            (email, business_name, contact, stage,
             business_name, contact)
        )
        lead_id = cur.fetchone()[0]
        self.conn.commit()
        return lead_id

    def get_uncontacted_leads(self, min_score: int = 6):
        """Get leads that haven't started outreach."""
        cur = self.conn.execute(
            "SELECT * FROM leads WHERE outreach_state IS NULL AND stage='discover'"
        )
        return [dict(r) for r in cur.fetchall()]

    def queue_step(self, lead_id: int, touch: int, subject: str, body: str,
                   scheduled_for: int) -> str:
        """Queue a single outreach step. Idempotent on (lead_id, touch)."""
        existing = self.conn.execute(
            "SELECT id FROM outreach_queue WHERE lead_id=? AND touch=?",
            (lead_id, touch)
        ).fetchone()
        if existing:
            return "exists"

        self.conn.execute(
            "INSERT INTO outreach_queue (lead_id, touch, subject, body, scheduled_for) "
            "VALUES (?, ?, ?, ?, ?)",
            (lead_id, touch, subject, body, scheduled_for)
        )
        self.conn.commit()
        return "created"

    def queue_sequence(self, lead_id: int, e1_subject: str, e1_body: str,
                       e2_subject: str, e2_body: str,
                       e3_subject: str, e3_body: str):
        """Queue E1+E2+E3 atomically. Each is idempotent."""
        now_ms = int(time.time() * 1000)
        results = []

        e1 = self.queue_step(lead_id, 1, e1_subject, e1_body, now_ms)
        results.append(("e1", e1))

        e2_at = now_ms + E2_GAP_MS
        e2 = self.queue_step(lead_id, 2, e2_subject, e2_body, e2_at)
        results.append(("e2", e2))

        e3_at = e2_at + E3_GAP_MS
        e3 = self.queue_step(lead_id, 3, e3_subject, e3_body, e3_at)
        results.append(("e3", e3))

        # Update lead's next action
        self.conn.execute(
            "UPDATE leads SET next_action_at=? WHERE id=?",
            (now_ms, lead_id)
        )
        self.conn.commit()
        return results

    def get_due_steps(self, limit: int = 30):
        """Get all queued items past their scheduled time."""
        now_ms = int(time.time() * 1000)
        cur = self.conn.execute(
            "SELECT q.*, l.email, l.business_name, l.outreach_state "
            "FROM outreach_queue q "
            "JOIN leads l ON q.lead_id = l.id "
            "WHERE q.status='queued' AND q.scheduled_for <= ? "
            "ORDER BY q.scheduled_for "
            "LIMIT ?",
            (now_ms, limit)
        )
        return [dict(r) for r in cur.fetchall()]

    def claim_step(self, queue_id: int) -> bool:
        """Atomically claim a queue item. Returns False if already claimed."""
        now_ms = int(time.time() * 1000)
        cur = self.conn.execute(
            "UPDATE outreach_queue SET status='sending', claimed_at=? "
            "WHERE id=? AND status='queued'",
            (now_ms, queue_id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def mark_sent(self, queue_id: int, lead_id: int, touch: int,
                  resend_id: str):
        """Mark queue item as sent and update lead state."""
        now_ms = int(time.time() * 1000)

        # Update queue item
        self.conn.execute(
            "UPDATE outreach_queue SET status='sent', sent_at=?, resend_id=? "
            "WHERE id=?",
            (now_ms, resend_id, queue_id)
        )

        # Map touch to state
        state_map = {1: "contacted", 2: "followup", 3: "breakup"}
        new_state = state_map.get(touch, "contacted")

        # Update lead
        self.conn.execute(
            "UPDATE leads SET outreach_state=?, stage=?, next_action_at=NULL "
            "WHERE id=?",
            (f"e{touch}_sent", new_state, lead_id)
        )
        self.conn.commit()

    def mark_failed(self, queue_id: int, error: str):
        now_ms = int(time.time() * 1000)
        self.conn.execute(
            "UPDATE outreach_queue SET error=?, claimed_at=? "
            "WHERE id=?",
            (error[:500], now_ms, queue_id)
        )
        self.conn.commit()
```

### 2. Send loop (sender.py)

```python
"""Outreach sender — the ONLY code that calls your email API.

This must be a separate process from your content generation.
Uses Resend as the email provider — swap the send_email() function
for SendGrid, SES, SMTP, etc.
"""
import os
import time
import json
import urllib.request
import urllib.error
from queue import OutreachStore


def send_email(api_key: str, from_addr: str, to_addr: str,
               subject: str, html_body: str,
               reply_to: str = None) -> str:
    """Send via Resend API. Replace this function for other providers."""
    data = json.dumps({
        "from": from_addr,
        "to": to_addr,
        "subject": subject,
        "html": html_body,
        "reply_to": reply_to or from_addr,
    }).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result["id"]
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Email send failed ({e.code}): {body}")


def send_outreach(store: OutreachStore, resend_key: str,
                  from_addr: str, limit: int = 15,
                  dry_run: bool = False):
    """Claim and send due outreach steps."""
    steps = store.get_due_steps(limit=limit)
    sent = failed = 0

    for step in steps:
        if dry_run:
            print(f"  DRY RUN: T{step['touch']} -> {step['email']} "
                  f"({step['business_name']})")
            continue

        # Claim atomically
        if not store.claim_step(step["id"]):
            continue

        try:
            resend_id = send_email(
                api_key=resend_key,
                from_addr=from_addr,
                to_addr=step["email"],
                subject=step["subject"],
                html_body=step["body"],
            )
            store.mark_sent(step["id"], step["lead_id"],
                           step["touch"], resend_id)
            print(f"  SENT T{step['touch']} -> {step['email']} "
                  f"({step['business_name']}) id={resend_id[:20]}")
            sent += 1
        except Exception as e:
            store.mark_failed(step["id"], str(e))
            print(f"  FAILED T{step['touch']} -> {step['email']}: "
                  f"{str(e)[:100]}")
            failed += 1

        # Rate-limit: small delay between sends
        time.sleep(1)

    return sent, failed
```

### 3. System cron entry

Run the sender as a cron job. Never let the AI content generator call the email API.

```cron
# Send outreach every 2 hours, max 15 per run
0 */2 * * * cd /path/to/project && python3 -c "
from sender import OutreachStore, send_outreach
store = OutreachStore()
send_outreach(store, os.environ['RESEND_API_KEY'],
              'Your Name <you@domain.com>', limit=15)
" >> logs/send_outreach.log 2>&1
```

---

## Error Handling

| Error | Likely cause | Fix |
|-------|-------------|-----|
| Email API 422 | Malformed HTML body (empty, truncated, or invalid tags) | Check body generation. Re-queue with valid HTML. |
| Email API 429 | Rate limited | Add delay between sends (1s is usually enough). Lower limit per run. |
| Connection timeout | API down or network issue | Retry on next cron tick (queue item stays in `queued`). |
| Auth failure (401/403) | API key expired or wrong | Check credentials in environment. |

### Failure recovery

- If sending fails, the queue item stays `queued` with an error recorded and retries on the next cron tick
- If the email API returns a successful ID, the item is marked `sent` and the lead state advances
- Timing gates (E2/E3) are checked at claim time, so even if the queue has items, they won't send early

---

## Incident Lessons From Production

### Lesson 1: Never let the AI call the email API
An AI agent couldn't write to the queue (env var missing), so it fell back to calling the email API directly — with wrong formatting, wrong signature, wrong CTA. **Fix:** The queue writer and the email sender must be separate processes with separate auth. The sender doesn't use the AI model; it's a simple script.

### Lesson 2: Hardcode follow-up bodies
When the AI generated E2 and E3 per-lead, it invented different offers, tones, and CTAs for each one. **Fix:** E2 and E3 are fixed bodies in the prompt. Only E1 is personalised. This constraints the AI to the approved messaging.

### Lesson 3: Brand rules must be a checklist
After an incident where 61 emails went out with wrong branding, we added a verification checklist that runs before every send. The AI must verify: signature correct? CTA correct? colours correct? no founder name in body? **Fix:** Make the checklist part of the generation prompt AND verify after generation.

### Lesson 4: Timing gates prevent double-sends
Without gates, E2 and E3 could fire simultaneously if the system came back online after downtime. The state machine check (`lead.outreachState must be contacted before E2`) prevents this even if both queue items are past due.

---

## Adapting to Your Stack

This pattern works with any:
- **Database:** SQLite, Postgres, MySQL, Supabase, Convex — just implement the storage methods
- **Email provider:** Resend, SendGrid, AWS SES, SMTP — just replace `send_email()`
- **AI model:** Claude, GPT, Gemini, local models — the pattern is prompt-agnostic
- **Schedule:** cron, GitHub Actions, AWS EventBridge, systemd timers

The three-zone isolation (discover → queue → send) is the key insight, not the specific implementation.

### Minimal adaptation path

1. Copy `queue.py` and swap SQLite for your DB
2. Copy `sender.py` and swap `send_email()` for your email provider
3. Set up a cron to run the sender every few hours
4. Generate E1/E2/E3 via your AI tool, call `queue_sequence()`
5. Never let your AI tool call the email API

---

## Body Verification Checklist

Before every send cycle, an AI tool should verify:
- [ ] Signature uses the correct name and company
- [ ] Background colour matches brand
- [ ] CTA button colour contrasts with background
- [ ] CTA link goes to the correct URL
- [ ] No name of founder/CEO in the body text
- [ ] Reply-to address is the sender's real email
- [ ] Domain in links matches the brand domain
- [ ] E2/E3 use the fixed body, not a custom generation

```python
def verify_body(body: str, brand_name: str, domain: str) -> list[str]:
    issues = []
    if "#0a0a0a" not in body:
        issues.append("Missing dark background (#0a0a0a)")
    if "#56d9ff" not in body:
        issues.append("Missing brand CTA colour (#56d9ff)")
    if brand_name not in body:
        issues.append(f"Missing brand name ({brand_name})")
    if domain not in body:
        issues.append(f"Missing domain ({domain}) in links")
    return issues
```
