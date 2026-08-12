# Claude Code: Corporate Launcher, Policy Helper, and Sandbox Binary Paths

Rollout engineering for three managed controls that keep Claude Code aligned with endpoint security tooling:

- `processWrapper` / `CLAUDE_CODE_PROCESS_WRAPPER`: corporate launcher (a mandatory wrapper that starts Claude Code's own background processes)
- `policyHelper`: MDM-only executable that computes managed settings at startup
- `sandbox.bwrapPath` / `sandbox.socatPath`: pinned Linux/WSL2 sandbox binaries

Audience: IT admins who have not used Claude Code personally. Prefer MDM or system `managed-settings.json` for these keys. Server-managed settings do **not** honor `policyHelper` or `wslInheritsWindowsSettings`.

---

## 1. Rollout Plan

### Phased rollout

| Phase | Scope | Exit criteria |
|-------|-------|---------------|
| Pilot | 5-15 Linux and/or WSL2 machines that already run your corporate launcher (or sandbox packages) | `/status` shows managed source; Self-exec matches launcher; `bwrap --version` and `socat -V` succeed; no unexplained start refusals for 1 week |
| Expanded pilot | One BU / OS mix including macOS (Seatbelt, no bwrap) and Windows (launcher ignored) | Same checks; exception queue < 5% of users; SIEM shows expected daemon restart events |
| Org-wide | All Claude Code endpoints | MDM compliance green; rollback package tested; developer FAQ published |

### Pre-rollout checklist

- [ ] MDM path verified (Jamf / Intune / Workspace ONE can write managed settings)
- [ ] Secrets manager ready (policy helper signing secrets or launcher credentials never live in JSON)
- [ ] SIEM ingest tested for Claude Code debug / daemon mismatch warnings
- [ ] Rollback plan documented (remove keys, restart daemon, communicate)
- [ ] Confirm Claude Code >= 2.1.210 on pilot (`processWrapper` key; env form needs >= 2.1.208)
- [ ] Confirm Linux/WSL2 images ship `bubblewrap` and `socat` at the pinned paths

### What will break

| Control | Likely impact | Developer message before rollout |
|---------|---------------|----------------------------------|
| `processWrapper` wrong or missing binary | Background sessions, agent view, and some self-spawns refuse to start (fail closed, not unwrapped) | "Claude Code background processes now start through the corporate launcher at `/opt/corp/launcher`. If agent view fails, run `claude daemon stop --any`, then reopen Claude Code. File tickets with the Self-exec line from `/status`." |
| `policyHelper` non-zero exit | Claude Code refuses to start | "Claude Code now loads policy from the MDM policy helper. If it fails to start, connect to the corp network (or wait for the helper cache) and retry. Do not uninstall the helper." |
| Wrong `bwrapPath` / `socatPath` | Linux/WSL2 sandbox fails; Strict with `failIfUnavailable: true` blocks work | "Linux sandbox binaries are pinned. If sandbox errors appear, install `bubblewrap` and `socat`, or ask IT to update the managed paths." |
| Windows + `processWrapper` | Setting is ignored; processes start unwrapped | Plan Windows separately (EDR / AppLocker). Do not claim launcher coverage on Windows. |

### Rollback procedure

1. Remove `processWrapper`, `policyHelper`, `sandbox.bwrapPath`, and `sandbox.socatPath` from the MDM payload or managed file (or restore previous JSON).
2. Run `claude daemon stop --any` (or `claude daemon stop` for an installed service).
3. Ask users to restart Claude Code sessions.
4. Validate `/status` no longer shows a Self-exec mismatch warning for the old launcher.
5. Communication template: "We rolled back the Claude Code launcher/policy helper change. Restart Claude Code once. Reply in this thread if `/status` still shows a launcher warning."

---

## 2. Config Files

Use the tier files under `claude-code/examples/`. Exact filenames:

- `managed-settings-baseline.json`
- `managed-settings-moderate.json`
- `managed-settings-strict.json`

### Deployable pins (safe defaults)

Moderate and Strict ship:

```json
{
  "minimumVersion": "2.1.210",
  "wslInheritsWindowsSettings": true,
  "sandbox": {
    "bwrapPath": "/usr/bin/bwrap",
    "socatPath": "/usr/bin/socat"
  }
}
```

Adjust absolute paths if your image installs the binaries elsewhere.

### Optional: corporate launcher (add only when mandatory)

```json
{
  "processWrapper": "/opt/corp/launcher"
}
```

Or via env (takes precedence if both are set):

```json
{
  "env": {
    "CLAUDE_CODE_PROCESS_WRAPPER": "/opt/corp/launcher"
  }
}
```

Launcher contract (summary):

- Absolute path; end with `exec "$@"`
- Do not drop inherited environment variables
- Reach `exec` quickly (about 3 seconds); cache slow SSO work
- Tolerate nested invocation
- Do not print to the terminal before `exec`

### Optional: policy helper (MDM / system file only)

```json
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000,
    "refreshIntervalMs": 300000
  }
}
```

Helper stdout must wrap settings:

```json
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  }
}
```

A bare settings object (no `managedSettings` key) applies nothing. When the helper emits `managedSettings`, that object is the **only** managed source for the run (remote, MDM, and file sources are ignored for that run). Cache on outage and exit `0` for resilience.

---

## 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `minimumVersion` | `2.1.210` | `2.1.210` | `2.1.210` | Floor for `processWrapper` and current managed sandbox path behavior |
| `wslInheritsWindowsSettings` | unset | `true` | `true` | Enterprise Windows+WSL fleets need one MDM payload |
| `sandbox.bwrapPath` | unset | `/usr/bin/bwrap` | `/usr/bin/bwrap` | Pin Linux sandbox binary for locked PATH; Baseline keeps auto-detect |
| `sandbox.socatPath` | unset | `/usr/bin/socat` | `/usr/bin/socat` | Same for network proxy helper |
| `processWrapper` | unset | unset (document optional) | unset in template; **required** when org mandates a launcher | Wrong path fails closed; do not invent a fake path in the template |
| `policyHelper` | unset | unset (MDM guide only) | unset (MDM guide only); use for posture-based policy | Helper becomes sole managed source; high blast radius if wrong |
| `CLAUDE_CODE_PROCESS_WRAPPER` | unset | unset | same as `processWrapper` guidance | Env form for older 2.1.208-2.1.209 or env-only delivery; env wins over key |

---

## 4. Deployment Steps

### File paths

| OS | Managed settings path |
|----|----------------------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux / WSL | `/etc/claude-code/managed-settings.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` or `HKLM\SOFTWARE\Policies\ClaudeCode` `Settings` REG_SZ |

### MDM guidance

**Jamf (macOS):** Deploy managed preferences domain `com.anthropic.claudecode` or the managed file. Use for `processWrapper` and sandbox keys. `bwrapPath`/`socatPath` are no-ops on macOS Seatbelt hosts.

**Intune (Windows):** Write HKLM policy JSON including `wslInheritsWindowsSettings: true`. Expect `processWrapper` to be ignored on native Windows. For WSL, confirm WSL sessions inherit Windows policy after the flag is set in HKLM (and HKCU if you also use user policy).

**Workspace ONE / Linux MDM:** Place system `managed-settings.json` root-owned `644`. Deploy `/opt/corp/launcher` and optional `/usr/local/bin/claude-policy` as separate packages before enabling the keys.

**Server-managed (Admin Console):** Can deliver `processWrapper` (shows on security approval dialog) and sandbox path keys when they are in the winning managed source. Cannot deliver `policyHelper` or `wslInheritsWindowsSettings`. Prefer MDM for those two.

### Validation

```bash
claude --version   # >= 2.1.210
# Inside a session:
# /status  -> Setting sources includes Enterprise managed settings (...)
# /status  -> Self-exec matches your launcher when processWrapper is set
claude daemon status
# Linux/WSL2:
bwrap --version
socat -V
test -x /usr/bin/bwrap && test -x /usr/bin/socat
```

### Audit logging / SIEM

- Alert on repeated launcher mismatch warnings from `/status` or `claude daemon status`
- Alert on policy helper startup refusals (users cannot start Claude Code)
- Alert on sandbox unavailable events on Strict hosts (`failIfUnavailable: true`)
- Ship Claude Code debug logs per your endpoint logging agent; do not log launcher secrets

---

## 5. Workflow-Preservation Notes

| Blocked / failing operation | Risk | Safe equivalent |
|-----------------------------|------|-----------------|
| Starting agent view without a working launcher | Unwrapped background processes bypass corp controls | Fix launcher path; `claude daemon stop --any`; restart session |
| Project `.claude/settings.json` setting `processWrapper` | Repo could hijack every self-spawn | Keep launcher only in managed / user settings; ignore project attempts |
| Using `policyHelper` from server-managed settings | Setting silently not honored | Deploy helper via MDM or system managed file |
| Replacing `~/.local/bin/claude` symlink with the launcher | Double-wrap and externally managed install state | Restore installer symlink; use `processWrapper` instead |
| Relying on `processWrapper` on Windows | False sense of coverage | Use Windows EDR / AppLocker; track Windows as unwrapped for this control |
| `UserPromptExpansion` / `MessageDisplay` hooks from projects under Strict | Hook surface for prompt injection or UI spoofing | Keep `allowManagedHooksOnly: true` on Strict; ship approved hooks via managed settings |

### False-positive friction

- **Launcher too slow:** SSO on every spawn trips restart loops. Cache tokens; keep cold path under ~3 seconds.
- **bwrap path differs by distro:** Exception process updates `bwrapPath`/`socatPath` per image SKU via `managed-settings.d/` drop-ins.
- **policyHelper + parent embedder:** While a policy helper is configured, parent settings (for example Claude Desktop embedder) are never merged. Do not enable helper and Desktop parent merge on the same fleet without a deliberate design.

### Overlap callout

Claude Code `processWrapper` covers Claude Code self-spawns only. Cursor, Codex CLI, and Copilot have separate shell/sandbox controls. Enabling a launcher here does not wrap those tools. Sandbox `bwrapPath`/`socatPath` also do not replace permission deny rules or MCP allowlists.
