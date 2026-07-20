---
name: end
description: End the current session — run /vault to save artefacts, write a structured handoff file at Vault/Sessions/handoff-latest.json, and spawn a fresh Claude Code session in a new Terminal window. The new session picks up via /cont.
---

# end — end session, save + handoff + new session

See `~/.claude/commands/end.md` for the full flow. This skill body is injected on `/end`.

## Sequence

1. Run the `/vault` flow (read `~/.claude/commands/vault.md`).
2. Write `~/Documents/Claude Vault/Sessions/handoff-latest.json` with the structured state.
3. osascript: open a new Terminal window with `claude` in the same CWD.
4. Output a one-line summary.

## Handoff JSON shape

See `~/.claude/commands/end.md` Step 2 for the schema. The handoff file is the source of truth — `/cont` reads it first in the new session.

## Fallback

If osascript fails, the vault + handoff are still saved. Tell the user to open a new shell manually.
