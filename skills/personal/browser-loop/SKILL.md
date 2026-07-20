---
name: browser-loop
description: >
  Run a natural-language browser task using the ~/browser-use setup and
  return the screenshot paths so Claude can Read them. Use when the user
  wants to drive a browser task, check a UI state, scrape a page, or
  schedule recurring browser checks. Invoke with a task string:
  /browser-loop "go to example.com and tell me the H1".
---

# /browser-loop

Run a browser task via the local browser-use setup (MiniMax M3-driven,
headless Chromium, screenshots saved to disk).

## When to use

- "Check the homepage"
- "Screenshot the lead detail page"
- "Click X and tell me what happens"
- Any task that's better answered by actually visiting a page

## Invocation

```
/browser-loop "<natural-language task>"
```

Optional flags (parsed from the task string or as a leading prefix):
- `--max-steps N` — cap agent steps (default 25)
- `--headed` — show the browser window (default headless)
- `--out PATH` — custom screenshot dir

## What the skill does

1. Activate the venv: `cd ~/browser-use && source .venv/bin/activate`
2. Run: `python run.py "<task>" --headless` (with any extra flags)
3. Parse the JSON output for the screenshot directory
4. **Read the most recent screenshot** with the Read tool so Claude sees
   the page
5. Report back: what the task found + the screenshot path for follow-up

## Recurring / looped use

Compatible with `/loop` for scheduled runs:

```
/loop 30m /browser-loop "check the lead queue at /actions and tell me new ones"
/loop 5m  /browser-loop "screenshot https://emvyai.com homepage"
```

`/loop` handles the scheduling; this skill handles the work.

## Cross-project

This skill is the single entry point for browser automation across all
projects (EMVY, TeachWise, LepepAI, anything web). Don't reinvent
per-project browser scripts — route through here.

## Reference

- Setup: `~/browser-use/`
- Workflow doc: `~/Documents/Claude Vault/Topics/Claude Core Workflows.md`
- Technical deep-dive: `~/Documents/Claude Vault/Projects/browser-use/README.md`
