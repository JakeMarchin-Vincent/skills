---
name: vault
description: Save notes, decisions, and quick captures to the user's Obsidian vault at ~/Documents/Claude Vault/. Use when the user wants to write to the vault, capture an idea, save a session decision, or sync project notes. Sub-commands: /vault note "text" → Inbox.md; /vault <topic-name> "text" → Topics/<Title Case>.md (create or append); /vault sync → update project INDEX.md from current session context; /vault status → show last write time and where the vault points.
argument-hint: "[note|topic|sync|status] [text]"
---

# Vault

User's Obsidian vault: `~/Documents/Claude Vault/`

## Structure

```
Claude Vault/
├── Projects/<ProjectName>/     # project-specific notes + INDEX.md
├── Topics/                      # cross-project ideas
├── Inbox.md                     # quick captures (chronological)
├── Scripts/                     # automation
└── README.md                    # vault structure docs
```

Active projects live in `Projects/`. Each has its own `INDEX.md` (per `Projects/TEMPLATE.md`) and dated session notes (`Session YYYY-MM-DD.md`).

## Sub-commands

### `/vault note "text"`

Append a timestamped line to `~/Documents/Claude Vault/Inbox.md`. Use for quick captures that don't yet belong to a project or topic.

```markdown
## [YYYY-MM-DD HH:MM]

- <text>
```

If `Inbox.md` doesn't exist, create it with the vault header from `Projects/TEMPLATE.md` style.

### `/vault <topic-name> "text"`

Write or append to `~/Documents/Claude Vault/Topics/<Title Case Topic>.md`. Use for ideas, references, decisions that span projects. Title Case the topic name (e.g. `/vault "API registry"` → `Topics/Api Registry.md`).

If the file exists, append a dated section at the bottom. If not, create it with a one-line description and the captured text.

### `/vault sync`

Refresh the current project's `INDEX.md` from session context. Detect the project from CWD (read `package.json` `name` field; map common names → vault folder name). Update the file list and last-updated timestamp. Don't rewrite the full file — only patch the changed entries.

Default project mapping if `package.json` name is one of: `emvy-booking`, `emvy-website-v2` → `EMVY AI Website`. Fall back to other `emvy-*` names → `emvy-*` folder. For anything else, ask.

### `/vault status`

Show:
- Vault path
- Inbox.md last-modified time
- Current project's INDEX.md last-modified time
- Any unsynced session notes (files newer than INDEX.md)

Don't write anything.

## Conventions

- **Title Case** for note filenames (`Session 2026-06-02.md`, not `session-2026-06-02.md`)
- **Dated sections** within files for chronological capture
- **Wikilinks** `[[Note Title]]` for cross-references (the vault renders these as Obsidian links)
- **No folder hierarchies** within `Topics/` — keep flat, use wikilinks and INDEX-style aggregations instead

## Don'ts

- Don't write secrets, API keys, or tokens to the vault
- Don't duplicate the existing `obsidian-vault` skill's `/mnt/d/Obsidian Vault/AI Research/` target — this is a different vault
- Don't move or rename existing files in the vault without asking
- Don't strip existing content from notes when appending — add a new dated section

## Related skills

- `obsidian-vault` — the original Matt Pocock skill targeting the WSL vault. Keep both; the user's two vaults serve different purposes.
