---
name: vault
description: Populate the Obsidian vault (decisions, mistakes, knowledge, notes, session log) for the current session. Use when the user runs /vault, or when committing session artefacts to the vault. Central session logs at Vault/Sessions/YYYY-MM-DD — [project].md; per-project files at Projects/<project>/{decisions,mistakes,knowledge,notes}.md.
---

# vault — populate the Obsidian vault for the current session

See `~/.claude/commands/vault.md` for the full flow. This skill is the body that gets injected when the user invokes `/vault`.

## When to invoke

- The user types `/vault` directly.
- The user asks to "save this to the vault" / "write up the session" / "commit decisions to the vault" / "log this".
- The user asks to "close out" a session with proper artefacts.

## Vault layout (verify before writing)

- Vault root: `~/Documents/Claude Vault/`
- Per-project folder: `~/Documents/Claude Vault/Projects/<slug>/`
- Central session logs: `~/Documents/Claude Vault/Sessions/` (create on first run)
- Per-project files maintained: `decisions.md` (existing), `mistakes.md` (new), `knowledge.md` (new), `notes.md` (new).

## Files written per project touched

| File | What goes in it |
|---|---|
| `<project>/decisions.md` | Locked decisions (past tense, with why + source) |
| `<project>/mistakes.md` | Incidents, regressions, near-misses (factual, root cause, fix, status) |
| `<project>/knowledge.md` | Stable knowledge — vendor info, env quirks, "things I forget but shouldn't" |
| `<project>/notes.md` | In-session observations, follow-ups, parking lot — lower bar than decisions |
| `Vault/Sessions/YYYY-MM-DD — <slug>.md` | Session log: what changed, decisions, mistakes, knowledge, notes, open TBDs, handoff |
| **Push to `VPS:~/.hermes/claude-briefing.md`** | After writing Obsidian vault, push a TLDR (What changed + Decisions + Open TBDs) to Mewy's VPS briefing. Mewy reads it on startup (STEP 0 of her sequence). Helper: `~/.claude/bin/push-briefing.sh`. Best-effort — warn on failure, don't block the /vault write. |

## Style rules

- Per `feedback_short-no-recap`: no preamble, no recap, just deliver.
- Per `feedback_brevity`: keep prompts short; don't expand the operator's clicks.
- Per `feedback_review-before-send`: if the user hasn't explicitly invoked /vault, ask before editing vault files.
- Per `feedback_new-project-explicit-confirmation`: before creating a new `Projects/<slug>/` folder, ask the operator to confirm. Migration of an existing project (consolidation, rename, content merge) doesn't count; net-new project folders do.
- Never skip a file. If a section has nothing to add, write `_(none this session)_`.
- After writing, list the touched paths in one line: `Wrote: <paths>`. If the VPS push ran, add `Pushed: VPS:~/.hermes/claude-briefing.md`. If it failed, add `VPS push: FAILED (warning only)`.
