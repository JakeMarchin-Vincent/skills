---
name: api
description: List the APIs known to the current project, broken into sections: Project APIs (Convex, internal), Third-party SaaS (Stripe, Resend, Cal.com), Build/Infra (Vercel, etc.), and Deferred. For each: name, primary use, env var keys, code references, docs link. Sources: package.json deps, process.env references in code, vault notes (System Map.md), and a built-in reference list of well-known SaaS APIs.
argument-hint: "[section]  # optional: filter to one section (project|saas|infra|deferred|all)"
---

# Api

Pull a structured catalog of the APIs the current project knows about. Output is grouped into sections so the user can scan quickly.

## Sections

1. **Project APIs** — first-party / self-hosted / in-repo
   - e.g. Convex (functions + database), internal modules
2. **Third-party SaaS** — services with API keys/tokens
   - e.g. Stripe, Resend, Cal.com
3. **Build/Infra** — deployment, observability, auth providers, CI
   - e.g. Vercel, GitHub, Sentry
4. **Deferred** — known but not yet wired
   - e.g. e-sign providers (Dropbox Sign, DocuSign, PandaDoc) if discussed in vault but not in code

## How to discover

Run a sequence of grep/find commands to assemble the catalog. Don't write any code — just observe.

### Step 1: package.json deps

Read `package.json` dependencies. External packages that look like API clients:

```bash
cat package.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(d.get('dependencies',{})))"
```

Common ones to recognize: `stripe`, `resend`, `@sendgrid/mail`, `twilio`, `firebase`, `supabase`, `@aws-sdk/*`, `@slack/web-api`, `notion-client`, `openai`, `anthropic`, `@google/generative-ai`, `calcom`, `axios` (generic).

### Step 2: env var references in code

```bash
grep -rh "process\.env\." app/ lib/ convex/ --include="*.ts" --include="*.tsx" \
  | grep -oE "process\.env\.[A-Z_]+" | sort -u
```

Map known env var prefixes to services (e.g. `RESEND_*` → Resend, `STRIPE_*` → Stripe, `CALCOM_*` → Cal.com, `CONVEX_*` → Convex).

### Step 3: vault notes

Search the user's vault for an API registry if one exists:

```bash
find ~/Documents/Claude\ Vault/ -iname "*api*" -o -iname "*system*map*" 2>/dev/null
grep -rl "Stripe\|Resend\|Cal.com\|DocuSign" ~/Documents/Claude\ Vault/ --include="*.md" 2>/dev/null
```

Common files: `Projects/EMVY Business/System Map.md`, `Topics/API Registry.md`, anything in the project INDEX mentioning plugins.

### Step 4: built-in reference list

If a service is referenced in code or vault but not in the discovery above, fall back to a known reference list:
- Stripe, Resend, Cal.com, DocuSign, Dropbox Sign, PandaDoc, Postmark, SendGrid, Twilio, Notion, Slack, Linear, HubSpot, Salesforce, OpenAI, Anthropic, Google Gemini, AWS S3, Cloudflare R2, Sentry, PostHog, LogRocket, Plausible, Fathom, Vercel, Netlify, Cloudflare, Auth0, Clerk, Supabase, Firebase, Convex, Neon, PlanetScale, Supabase, Railway, Render

## Output format

For each API, show:

```markdown
### <Name>

- **Section**: <Project | SaaS | Infra | Deferred>
- **Primary use**: <one-line description>
- **Env vars**: `KEY_NAME`, `OTHER_KEY` (or "none")
- **Code refs**: `app/api/.../route.ts:12`, `lib/...`
- **Vault ref**: `Projects/EMVY Business/System Map.md` (if mentioned in notes)
- **Docs**: <link to official docs>
```

Group by section, alphabetise within each section. Mark "Deferred" entries with a `**Status**: not yet wired` line.

## Argument handling

- `/api` → show all sections
- `/api project` → only Project APIs
- `/api saas` → only Third-party SaaS
- `/api infra` → only Build/Infra
- `/api deferred` → only Deferred

## Don'ts

- Don't fabricate docs links — only include them if you can verify the URL pattern (`https://docs.<service>.com` or similar). If unsure, omit and note "(docs not in registry)".
- Don't include build tools (typescript, tailwind, postcss) — those aren't APIs.
- Don't include transitive dependencies (e.g. `lucide-react`, `react-pdf`) — only direct external API clients.
- Don't add APIs that aren't referenced anywhere — this is a "what we use" list, not a "what exists" list.

## Related

- `/grill-api` — for picking a new API to add (decision-making flow)
- The vault's `System Map.md` (if it exists) is the source of truth for "deferred" entries
