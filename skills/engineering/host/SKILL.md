---
name: host
description: Start the project's dev server on a specific port. /host → default port (3000 for Next.js, 5173 for Vite). /host 3001 → custom port. Detects project type from package.json and uses the right command. Runs the server in the background and reports the URL.
argument-hint: "[port]"
---

# Host

Start a local dev server for the current project. By default uses the project's standard port; pass a number to override.

## Behaviour

1. **Detect project type** from `package.json`:
   - `next` in `dependencies` or `devDependencies` → Next.js → `next dev -p <port>` (default 3000)
   - `vite` → Vite → `vite --port <port>` (default 5173)
   - `nuxt` → Nuxt → `nuxt dev --port <port>` (default 3000)
   - `astro` → Astro → `astro dev --port <port>` (default 4321)
   - `remix` / `@remix-run/*` → Remix → `remix dev --port <port>` (default 3000)
   - `express` only (no framework) → `node <main entry from package.json>` (no port flag unless `PORT` is read in code)
   - Fallback: `npm run dev` with `PORT=<port>` env var

2. **Port argument**:
   - `/host` → use the project's default port
   - `/host 3001` → use 3001
   - `/host abc` → error: "port must be a number between 1 and 65535"

3. **Run in the background** so the user can keep chatting. Use `Bash` with `run_in_background: true`. Report:
   - The full command being run
   - The expected URL (e.g. `http://localhost:3001`)
   - The background task ID so the user can stop it later

4. **Pre-flight**:
   - Check the port is free (`lsof -i :<port>`). If taken, tell the user which PID is on it and ask to kill or pick another port.
   - If `node_modules` doesn't exist, run `npm install` first and warn it may take a while.
   - If `.env.local` exists and the project uses env vars, mention it in the output.

5. **First-run output**:
   - Wait for the server to print its "ready" line (Next.js: `Ready in`; Vite: `Local:`; etc.). Tail the background task for ~10 seconds and report what the server printed.
   - If it errors out, show the error and ask whether to retry with different settings.

## Examples

```
/host              # Next.js on 3000
/host 3001         # Next.js on 3001
/host 8080         # Next.js on 8080
```

## Don'ts

- Don't run `npm run build && npm start` — that's production mode, not dev. If the user wants prod, confirm first.
- Don't start multiple servers in parallel without asking. If one is already running on the requested port, fail and tell the user.
- Don't run `next dev` in the foreground — the whole point is background so the user can keep working.
- Don't auto-restart on crash — surface the error and let the user decide.

## Stopping

Tell the user to use the `TaskStop` tool with the background task ID, or kill the process: `lsof -ti :<port> | xargs kill`. Don't auto-stop.
