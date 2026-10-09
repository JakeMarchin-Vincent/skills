# Implementation contract for automated outreach

Use this only if the user explicitly asks to build or connect a sender. The main skill works without one. This is an architecture and acceptance contract, **not executable production code**.

## Separate authority and processes

1. **Research/drafting agent:** reads only approved sources, drafts or revises content and writes a reviewable artefact. No provider send credential.
2. **Approval/queue:** stores the exact approved content, intended recipient, campaign, channel and sender, version, approved cadence and compliance metadata. Human review or an explicitly authorised batch-approval policy is required. No claimed atomicity without a transaction and unique constraints.
3. **Deterministic dispatcher:** exclusively holds send credentials. Selects a due candidate, checks fresh suppression/reply/bounce records and last *actual* send time, acquires a durable claim, rechecks, invokes the provider, and records its response. It must not invent or silently rewrite content.

If an inbox/CRM cannot be checked for replies and suppression, do not enable automatic follow-ups. Do not deploy cron, use API keys or send test emails as part of merely installing this skill.

## Acceptance tests with a fake provider

- A queued E2/E3 cannot send before the previous touch is recorded as accepted, even after downtime makes every schedule timestamp overdue.
- Gaps begin at previous confirmed acceptance, not at queue creation. Local send windows are applied.
- Concurrent workers cannot claim the same touch. Re-queueing an existing campaign/recipient/touch does not duplicate it.
- Reply, refusal, opt-out and bounce discovered between candidate selection and dispatch block that send.
- A definitive provider rejection records a bounded, visible failure; permanent errors require operator intervention.
- An ambiguous timeout, crash after acceptance or failed database update enters `outcome_unknown` and never auto-retries until reconciliation.
- Provider acceptance is recorded as accepted, not inbox-delivered; the application can distinguish delivery/bounce events if the provider exposes them.
- A preview/dry-run uses synthetic recipients and **cannot** make a network send call, even if credentials are present.

The published skill intentionally does not bundle the former SQLite/Resend example: it did not enforce its claimed eligibility checks and could dispatch all overdue touches in one run. A production adapter must be designed and tested for its actual database, provider, consent model and failure modes before anyone runs it.
