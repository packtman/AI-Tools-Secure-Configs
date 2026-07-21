# Tabnine CLI hardened settings rollout

This guide deploys the valid JSON system settings in `examples/settings-strict.json`, `examples/settings-moderate.json`, or `examples/settings-baseline.json`. System settings are admin-enforced and take precedence over user and workspace settings.

## Rollout Plan

### Pre-rollout checklist

- [ ] Confirm the target tier and document exceptions.
- [ ] Verify the MDM file path, ownership, and restart behavior on one endpoint per operating system.
- [ ] Verify the endpoint has a supported sandbox runtime. Test Docker or Podman on Linux and Windows, and the supported OS sandbox on macOS.
- [ ] Store Tabnine and model credentials in the organization secrets manager. Do not place credentials in `settings.json`.
- [ ] Configure an organization-owned OpenTelemetry collector before enabling local telemetry.
- [ ] Test SIEM ingestion without prompt logging.
- [ ] Configure MCP Governance in the Tabnine Admin Console. Strict uses `Block all`, Moderate uses `Allow-list only`, and Baseline uses `Allow only remote` or `Allow-list only`.
- [ ] Export the current system settings and Admin Console policy.
- [ ] Document the rollback owner, help-desk route, and emergency MDM exclusion group.

### Phase 1: pilot

Deploy to 5 to 10 security-aware developers across the supported operating systems.

Exit criteria:

- Settings load from the system path and cannot be overridden by user or workspace files.
- No secret value appears in sampled context or telemetry.
- Sandboxed test and build commands complete on at least 95 percent of pilot endpoints.
- Strict endpoints correctly block edits, MCP, hooks, skills, and interactive shells.
- Every blocking event has a documented safe replacement or approved exception route.

### Phase 2: expanded pilot

Deploy to one complete engineering team plus CI-like developer workflows. Keep a control group on the previous policy.

Exit criteria:

- The team completes a normal development cycle without an unresolved severity-1 workflow outage.
- False-positive blocks stay below the organization's agreed threshold.
- Help-desk staff can identify the active settings source and complete rollback.
- SIEM alerts distinguish policy changes, repeated YOLO attempts, MCP denials, and unusual tool activity.

### Phase 3: organization-wide

Deploy by operating-system rings. Hold each ring until endpoint compliance and support metrics are stable.

Exit criteria:

- At least 95 percent of active endpoints report the expected file hash and restrictive ownership.
- All exceptions have an owner, scope, reason, and expiry date.
- Admin Console MCP policy and endpoint system settings are reviewed together.
- Rollback packages remain available for the previous known-good policy.

### What will break

| Tier or control | Likely impact | Developer message |
|-----------------|---------------|-------------------|
| Strict `plan` mode | File creation and edits are unavailable. | "Tabnine is read-only in this environment. Use it to plan, then apply reviewed changes through your normal editor or approved automation." |
| Sandboxing | Docker, Podman, filesystem mounts, network calls, or commands that expect host access may fail. | "Commands now run in an isolated environment. Request a narrow path or network exception if the sandbox blocks a required tool." |
| Strict interactive-shell block | REPLs, debuggers, login prompts, and interactive installers fail. | "Use non-interactive flags, a developer-owned terminal, or an approved task runner." |
| Remote Code Search disabled | Cross-repository context is unavailable. | "Only local workspace context is available until the repository is approved for remote indexing." |
| Persistent approval disabled | Users see repeated confirmation prompts. | "Repeated prompts are expected for state-changing actions. Request a reviewed policy rule instead of selecting a permanent approval." |
| Strict MCP block | Database, ticketing, browser, and other MCP integrations disappear. | "MCP is disabled in this tier. Use the approved first-party client or request review of a specific server." |
| Hooks disabled | Automation and compliance hooks do not run inside Tabnine. | "Run the approved checks through CI or the managed task runner." |
| Skills disabled | Built-in, extension, user, and workspace skills are unavailable. | "Use approved static instructions or request a skill security review." |

### Rollback procedure

1. In MDM, replace the deployed `settings.json` with the exported previous file. If no prior file existed, remove only the MDM-managed file.
2. Restore the previous Tabnine Admin Console MCP policy and allowlist.
3. Restart Tabnine CLI sessions. Settings marked as restart-required do not change in an active session.
4. Verify the effective policy with the checks in Deployment Steps.
5. Keep telemetry prompt logging disabled during rollback.
6. Record the affected policy hash, endpoints, reason, and approving incident owner.

Rollback communication:

> We rolled back the Tabnine CLI system policy because it interrupted an approved workflow. Restart Tabnine before retrying. Existing code and user settings were not removed. Security will publish a corrected policy or a time-bounded exception after review.

## Config Files

Choose one file and deploy it as the platform system `settings.json`:

| Tier | Source file | Intended environment |
|------|-------------|----------------------|
| Strict | `examples/settings-strict.json` | Regulated or high-assurance endpoints |
| Moderate | `examples/settings-moderate.json` | Standard enterprise endpoints |
| Baseline | `examples/settings-baseline.json` | Lower-risk teams that prioritize workflow continuity |

The files contain only documented Tabnine CLI keys. Explanations for every non-trivial key are in `examples/settings.comments.md`.

## Tier Delta Table

`Omitted` means Tabnine's default or an organization-specific Admin Console policy applies.

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|-----------------------|
| `general.defaultApprovalMode` | `auto_edit` | `default` | `plan` | Higher tiers require more human control and Strict is read-only. |
| `general.debugKeystrokeLogging` | `false` | `false` | `false` | Keystrokes can contain sensitive input. |
| `general.devtools` | `false` | `false` | `false` | The debugging surface is unnecessary on managed endpoints. |
| `tools.enableRemoteCodeSearch` | `true` | `false` | `false` | Baseline keeps cross-repository context. Higher tiers require explicit indexing approval. |
| `tools.sandbox` | `true` | `true` | `true` | Host isolation is required in every tier. |
| `tools.shell.enableInteractiveShell` | Omitted | Omitted | `false` | Strict removes long-lived, hard-to-audit shell sessions. |
| `security.disableYoloMode` | `true` | `true` | `true` | No tier permits a complete approval bypass. |
| `security.disableAlwaysAllow` | `false` | `true` | `true` | Baseline permits lower-friction local exceptions. |
| `security.enablePermanentToolApproval` | `false` | `false` | `false` | Durable grants are disabled in every tier. |
| `security.autoAddToPolicyByDefault` | `false` | `false` | `false` | Permanent policy changes must be intentional. |
| `security.blockGitExtensions` | `true` | `true` | `true` | Direct Git installation is a supply-chain risk. |
| `security.allowedExtensions` | Omitted | Omitted | `[]` | Strict has no implicit extension exceptions. |
| `security.folderTrust.enabled` | `true` | `true` | `true` | Untrusted repositories must not load workspace settings or skills. |
| `security.enableConseca` | `false` | `true` | `true` | Higher tiers accept more friction for context-aware security checks. |
| `security.environmentVariableRedaction.enabled` | `true` | `true` | `true` | Secret redaction is required in every tier. |
| `security.environmentVariableRedaction.allowed` | `[]` | `[]` | `[]` | No environment variable receives a blanket redaction bypass. |
| `security.environmentVariableRedaction.blocked` | Four common credential variables | Four common credential variables | Four common credential variables | Explicit blocking supplements automatic secret detection. |
| `context.fileFiltering.respectGitIgnore` | `true` | `true` | `true` | Ignored local files should not enter model context. |
| `context.fileFiltering.respectGeminiIgnore` | `true` | `true` | `true` | `.tabnineignore` remains effective in every tier. |
| `telemetry.enabled` | `false` | `false` | `false` | Enable only after an organization collector and retention policy are ready. |
| `telemetry.logPrompts` | `false` | `false` | `false` | Prompts can contain code, secrets, and personal data. |
| `mcp.allowed` | Omitted | Omitted | `[]` | Strict adds endpoint defense in depth. Other tiers use the organization MCP allowlist. |
| `hooksConfig.enabled` | `true` | `true` | `false` | Strict blocks unmanaged command hooks. |
| `skills.enabled` | `true` | `true` | `false` | Strict blocks skill instructions and bundled scripts. |

## Deployment Steps

### Exact system paths

| OS | Admin-enforced system settings path |
|----|-------------------------------------|
| Windows | `C:\ProgramData\tabnine-cli\settings.json` |
| macOS | `/Library/Application Support/TabnineCli/settings.json` |
| Linux | `/etc/tabnine-cli/settings.json` |

Use the system settings path, not `system-defaults.json`. System defaults are user-overridable.

### MDM delivery

1. Select one tier file and rename it to `settings.json`.
2. Deliver it atomically with administrator ownership.
3. Windows: use Intune or Workspace ONE to create `C:\ProgramData\tabnine-cli`, write the file, and grant standard users read-only access.
4. macOS: use Jamf or Workspace ONE to create `/Library/Application Support/TabnineCli`, write the file as `root:wheel`, and set mode `0644`.
5. Linux: use the organization's configuration manager to write `/etc/tabnine-cli/settings.json` as `root:root` with mode `0644`.
6. Restart Tabnine CLI. Do not set `TABNINE_CLI_SYSTEM_SETTINGS_PATH` unless the MDM package also protects that alternate path.
7. Configure MCP Governance separately in the Admin Console. The JSON file does not replace the organization policy.

### Endpoint validation

Run the JSON parser before deployment:

```bash
python3 -m json.tool settings.json >/dev/null
```

Confirm the expected file exists and is not user-writable:

```bash
# macOS
stat -f '%Su:%Sg %Sp %N' '/Library/Application Support/TabnineCli/settings.json'

# Linux
stat -c '%U:%G %A %n' /etc/tabnine-cli/settings.json
```

On Windows PowerShell:

```powershell
Get-Item 'C:\ProgramData\tabnine-cli\settings.json' | Format-List FullName,Length,LastWriteTime
Get-Acl 'C:\ProgramData\tabnine-cli\settings.json' | Format-List
```

Start a new Tabnine session and attempt these checks:

- `--yolo` is rejected.
- An untrusted test repository does not load workspace skills or settings.
- A harmless command runs in the sandbox.
- Strict cannot edit a file, start an interactive shell, load a skill, run a hook, or enable an MCP server.
- Moderate requests approval for state-changing tools.
- Baseline can edit a disposable file but still cannot enter YOLO mode.

### Audit logging and SIEM

Tabnine CLI can export OpenTelemetry data. Keep `telemetry.logPrompts` false. When the collector is ready, set `telemetry.enabled` true through a separately reviewed overlay and configure `telemetry.otlpEndpoint` to an internal collector. Environment variables override file values, so inventory `TABNINE_TELEMETRY_*` and `OTEL_EXPORTER_OTLP_ENDPOINT` through MDM.

Alert on:

- Attempts to use YOLO mode.
- Repeated denied shell, MCP, hook, skill, or extension actions.
- Changes to the system settings file or its ownership.
- Admin Console MCP policy or allowlist changes.
- New privileged Tabnine administrators.
- Unexpected remote code search or prompt telemetry.

## Workflow-Preservation Notes

| Blocked or restricted operation | Safe equivalent |
|---------------------------------|-----------------|
| Strict file edits | Generate a plan, review it, then edit in the normal IDE or approved automation. |
| Interactive shell | Use a non-interactive command with explicit flags, or run the interactive tool in a developer-owned terminal. |
| Host filesystem or network access | Add the narrowest sandbox path or domain after review. Do not disable the sandbox globally. |
| Remote Code Search | Clone the approved repository locally or request indexing approval. |
| Permanent approval | Add a narrowly matched admin policy rule with an owner and expiry date. |
| MCP server | Use the vendor's first-party client or request a server entry with exact transport, URL or command, arguments, and tool scope. |
| Hook | Run the same check in CI or package it as an administrator-managed endpoint task. |
| Skill | Convert the workflow to reviewed static guidance, or approve a pinned skill package after inspecting its scripts. |

Common friction:

- Sandboxing can fail when Docker or Podman is absent, paths are mounted differently, or tests need network access. Pilot by language stack and grant narrow exceptions.
- `security.enableConseca` can block unusual but legitimate commands. Capture the exact decision, command, and repository trust state before requesting an exception.
- `respectGitIgnore` can hide generated fixtures needed by tests. Prefer a narrow `.tabnineignore` adjustment over disabling ignore processing.
- Repeated approval prompts are expected in Moderate. Consolidate only well-understood read-only operations into reviewed policy rules.

Exception requests must identify the user or group, repository, blocked control, business need, least-permissive replacement, owner, and expiry date. Never approve a permanent organization-wide bypass to resolve a single endpoint problem.
