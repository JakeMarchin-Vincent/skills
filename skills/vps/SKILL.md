---
name: vps
description: Operate the EMVY Contabo VPS (dusk@100.103.229.74 via Tailscale) — the host of all Hermes agents that run the EMVY process. SSH via sshpass + password (pubkey blocked by cloud-init). Use for: listing/checking/editing agent profiles, reading cron health, tailing logs, debugging Hermes writes to Convex, restarting agent gateways, or auditing the agent setup. Triggers: "vps", "blando", "mewy", "maya", "deep-state", "cartz", "builds", "audit", "sage", "hermes agent", "agent profile", "cron job", "EMVY agent".
---

# VPS — EMVY Hermes agents on Contabo

The VPS hosts the Hermes agents that run the EMVY process end-to-end. This skill gives you the SSH pattern, the agent roster, and the common tasks — so you can answer questions like "is Blando's cron still paused?", "what does the audit agent do?", or "fix Blando's prompt" in one session.

## SSH pattern (the only auth path)

Pubkey auth is blocked by `/etc/ssh/sshd_config.d/50-cloud-init.conf` and `dusk` has no passwordless sudo. The only working path is `sshpass` with the password. **Do not change these flags** — the wrong options will silently try a different auth method and fail.

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh \
  -o StrictHostKeyChecking=accept-new \
  -o ConnectTimeout=8 \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o UserKnownHostsFile=/dev/null \
  -o NumberOfPasswordPrompts=1 \
  -o LogLevel=ERROR \
  dusk@100.103.229.74 'COMMAND'
```

Tailscale IP preferred. Public IP `194.163.136.244` (alias `contabo`) is the fallback. If SSH hangs, `tailscale status` on the Mac.

Source of truth (vault): `~/Documents/Claude Vault/Topics/VPS access — Contabo.md`

## EMVY agent roster (live, captured 2026-06-12)

| Profile | Display name | Role | Cron |
|---------|--------------|------|------|
| `mewy` | Mewy | Main orchestrator, cross-vault access | on-demand + 30-min snapshot |
| `builds` | Cartz (Builds) | Lead builder — no Claude Code | daily 04:45 + 06:30 AWST |
| `blando` | Blando | Lead gen + outreach | every 2h (`0 */2 * * *`) |
| `audit` | Sage (Audit) | Daily SMB audit | daily 15:15 AWST |
| `maya` | Maya | Content + X | daily 06:30 AWST |
| `deep-state` | Deep-State | Competitor intel | daily 09:15 AWST |
| `happy-harold` | Happy-Harold | AI research brief | daily 02:00 AWST |
| `salescrm` | SalesCRM | Pipeline health | weekdays 08:30 AWST |
| `seo-marketing` | SEO-Marketing | Site audit | Mondays 10:00 AWST |

**Outside EMVY (do not include in board):** `funic` (Finlay's), `rovan` (parents'), `nunya` (Nunya's refrigeration), `default` (base profile).

## Common tasks

### 1. List all agents

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'ls ~/.hermes/profiles/'
```

### 2. Show an agent's role + responsibilities

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'head -50 ~/.hermes/profiles/$AGENT/AGENTS.md'
```

### 3. Show an agent's cron schedule

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'python3 -c "import json; print(json.dumps(json.load(open(\"/home/dusk/.hermes/profiles/$AGENT/cron/jobs.json\")), indent=2)[:3000])"'
```

### 4. Check if an agent's cron is paused

Look for `"state": "paused"` and `"paused_reason"` in the cron JSON. Common pause targets post 2026-06-05 61-email incident:

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'python3 -c "import json; d=json.load(open(\"/home/dusk/.hermes/profiles/blando/cron/jobs.json\")); [print(j[\"name\"], j.get(\"state\"), j.get(\"paused_reason\")) for j in d.get(\"jobs\",[])]"'
```

### 5. Read or write a skill file

Skills live at `~/.hermes/profiles/$AGENT/skills/<skill-name>/SKILL.md`. Read with `cat` or write with `cat > ... <<'EOF' ... EOF`.

### 6. Read the Blando lead-generation guide

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'cat ~/.hermes/profiles/blando/skills/lead-generation/emvy-lead-generation/references/convex-mutations-guide.md'
```

### 7. Test a Convex write from the VPS

Blando's `.env` line 29 (`BREVO_SENDER_NAME=Jake Marchin-Vincent` unquoted) breaks `source .env`. Workaround — load only the keys you need:

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'export $(grep -E "^(CONVEX_DEPLOY_KEY|HERMES_ACTIONS_TOKEN|NEXT_PUBLIC_CONVEX_URL)=" ~/.hermes/profiles/blando/.env | xargs) && python3 -c "from convex import upsert_lead; print(upsert_lead({\"email\":\"test@emvy.ai\",\"businessName\":\"smoke\",\"stage\":\"discover\"}))"'
```

### 8. Restart an agent gateway

The `dusk` user has no sudo, so can't `systemctl`. Use the user-level restart (path varies — discover first):

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'ls ~/.hermes/bin/ | head && cat ~/.hermes/profiles/$AG/gateway.pid 2>/dev/null'
```

### 9. Tail the gateway log

```bash
SSHPASS='Kevinisking@1923' sshpass -e ssh ... dusk@100.103.229.74 \
  'ls ~/.hermes/logs/ && tail -200 ~/.hermes/logs/<latest>.log'
```

### 10. Push a file from the Mac to the VPS

```bash
SSHPASS='Kevinisking@1923' sshpass -e scp \
  -o StrictHostKeyChecking=accept-new \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o UserKnownHostsFile=/dev/null \
  -o NumberOfPasswordPrompts=1 \
  /local/path dusk@100.103.229.74:/remote/path
```

## Hard rules

- **Never `sudo`** — `dusk` has no passwordless sudo. Tell the user if their request needs root.
- **Destructive ops need explicit confirmation** — `rm -rf`, mass `>`, killing cron jobs, restarting the gateway, editing `~/.hermes/.env` or `~/.hermes/profiles/blando/.env`. Confirm before running.
- **`fail2ban` lockout** — repeated failed `sshpass` attempts cause "Connection refused" for ~3 min. Don't retry tight loops; surface the lockout to the user.
- **Long output** — pipe through `head -200` or `grep` for what you need. Don't dump full log files.
- **One command per Bash call** for non-trivial work. Run a sequence of calls, not a single chained `&&` monstrosity.
- **Always check the .env line-29 bug** before `source`-ing `~/.hermes/profiles/blando/.env`.

## Audit-mode workflow (what the user is most often doing)

When the user says "review all the EMVY agents" or "audit the agent setup", walk the roster in this order:

1. `ls ~/.hermes/profiles/` — confirm roster hasn't changed since 2026-06-12
2. For each EMVY profile: `head -50 AGENTS.md` — capture role
3. For each EMVY profile: read `cron/jobs.json` — capture schedule, state, paused_reason
4. Note any cron that's been paused, failed, or has `last_status != "ok"`
5. Cross-check with Convex (`npx convex data leads | wc -l`) — does Blando's pipeline reflect what crons have run?
6. Report back as a table: profile / role / cron / state / last run / concern

If the user wants a doc update, the canonical place to keep the agent roster is section 21 of `~/Documents/EMVY BRANDING GUIDELINES/EMVY - Board & Operating Processes.pdf` (generated by `~/Documents/build_emvy_agent_roster.py`).
