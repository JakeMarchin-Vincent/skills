---
name: grill-api
description: Grill the user to pick the right API or plugin for a project need. Walks through use case, constraints, and candidate options one question at a time with a recommended answer. Use when the user wants to choose an API, evaluate alternatives, or says "what's the best X for Y". Mirrors the /grill-me cadence — one question, recommended answer, no big scopes.
argument-hint: "<use-case>  # e.g. 'e-sign for SMB contracts' or 'email delivery for transactional'"
---

# Grill-api

A focused grilling flow for picking the right API/plugin for a project need. Slower than a research dump — designed to converge on a single pick the user can defend.

## Flow

### 1. Frame the need (one question)

Ask: "What's the use case?" in the user's own words if they haven't specified. Examples:
- "transactional email for assessment PDFs"
- "e-sign for SMB audit contracts"
- "scheduling for discovery calls"
- "observability for the Next.js app"

**Don't ask multiple things at once.** Get the use case before any constraints.

### 2. Constrain (one question at a time)

Walk through the constraints, in this order, skipping any the user has already answered:

1. **Volume / scale** — per month, peak day
2. **Data residency** — AU-only, US, global, no constraint
3. **Existing accounts** — already pay for X? already integrated Y?
4. **Build vs buy** — is this core product or supporting infra?
5. **Solo or team** — who maintains the integration?
6. **Budget** — free tier acceptable, or paid expected
7. **Time-to-live** — needs to ship this week, or can take a quarter

For each, present a recommended default at the end of the question. Example:

> "Volume / scale? Recommended starting point: assume < 1k/month at launch, scale to 10k by year 2 — most SMB SaaS will fit this. Override if different."

Skip questions whose answer is obvious from the use case.

### 3. Surface candidates

Based on the use case + constraints, name 2–4 candidate APIs with:
- One-line description
- Why it fits / why it doesn't
- Pricing model (rough)
- Migration cost if picked and then changed

Examples by use case (illustrative, not exhaustive):

| Use case | Candidates |
|---|---|
| Transactional email | Resend, Postmark, SendGrid, AWS SES |
| E-sign | Dropbox Sign, DocuSign, PandaDoc, native (PDF + email) |
| Scheduling | Cal.com, Calendly, SavvyCal, TidyCal |
| Payments | Stripe, Paddle, LemonSqueezy, Square |
| Observability | Sentry, PostHog, LogRocket, Highlight.io |
| Auth | Clerk, Auth0, Supabase Auth, NextAuth/Auth.js, Convex Auth |
| Database | Convex, Supabase, Neon, PlanetScale, Firebase |
| File storage | AWS S3, Cloudflare R2, Backblaze B2, UploadThing |
| AI/LLM | Anthropic Claude, OpenAI, Google Gemini, open-source (Ollama) |
| CRM | HubSpot, Attio, Pipedrive, Notion-as-CRM |

Make a recommendation. Default to: paid-but-ubiquitous (Stripe, Resend, Cal.com, Sentry) unless constraints say otherwise. Match the user's existing stack — if they already have Convex, don't recommend Firebase.

### 4. Lock the pick

Once the user picks, capture:

```markdown
## <Use case>

- **Pick**: <name>
- **Why**: <one-sentence rationale tied to constraints>
- **Rejected**: <other candidates> — <one-line reason each>
- **When to revisit**: <trigger that would change the pick>
```

Save to:
- The current project's vault folder: `~/Documents/Claude Vault/Projects/<Project>/decisions.md` (append)
- If that file doesn't exist, create it
- If the project doesn't have a vault folder, ask the user which to use

### 5. Update registry

After locking, add the pick to:
- `package.json` (if the user wants it added) — confirm before editing
- The `deferred` section of the api registry (if not yet wired)
- The current Convex `convex.config.ts` if it's a Convex component (e.g. `@convex-dev/rag`)

Confirm each side-effect before doing it.

## Cadence rules (from /grill-me)

- **One question at a time** — never ask "what's the volume and budget and timeline" in one go
- **Always recommend** — present a default at the end of every question
- **No scope dumps** — don't list all 4 candidates' pricing on the first turn; introduce them in the candidate step
- **Allow "skip"** — let the user say "use the default" or "you pick"
- **Don't re-grill locked decisions** — check `~/Documents/Claude Vault/Projects/<Project>/` for any prior API decisions before asking the use case

## Don'ts

- Don't recommend building from scratch when an off-the-shelf option fits. The whole point of the question is "which SaaS", not "should we build it".
- Don't recommend OpenAI for everything by default — match the task to the model family.
- Don't surface 10 candidates. 2–4. The user is choosing, not shopping.
- Don't write code or wire anything up — this is decision-only. Hand off to `/to-prd` or `/to-issues` after the lock step.

## Related

- `/api` — the catalog of currently-wired APIs
- `/grill-me` — the general-purpose grill (no API-specific flow)
- `/to-prd` — convert the locked decision into a PRD for implementation
