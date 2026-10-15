# Codex CLI Permission Profile Rollout

This guide deploys admin-enforced permission profiles for Codex CLI 0.138.0 or
later. A permission profile is a named set of limits on what the agent may read,
write, and execute. The same managed configuration layer can also affect the
Codex desktop app and IDE extension, so test all installed Codex clients.

## Rollout Plan

### Pre-rollout checklist

- [ ] Confirm every pilot endpoint reports Codex 0.138.0 or later.
- [ ] Verify the cloud, MDM, or system-file delivery path on each operating system.
- [ ] Store deployment credentials in the organization's secrets manager.
- [ ] Test OpenTelemetry (OTel) or Compliance API ingest into the SIEM.
- [ ] Document the current requirements source and its rollback owner.
- [ ] Inventory Codex CLI, desktop app, and IDE extension overlap on pilot devices.

### Phase 1: pilot group

Deploy the chosen tier to 5 to 10 security-aware developers on all supported
operating systems. Include at least one read-only review and one normal edit
workflow.

Exit criteria:

- All clients are version 0.138.0 or later.
- `/debug-config` shows the expected default and allowed profiles.
- Strict users can review but cannot edit; Moderate and Baseline users can edit
  only inside the workspace.
- No endpoint can select `:danger-full-access`.
- SIEM receives approval and tool-result events without raw prompt content.

### Phase 2: expanded pilot

Deploy to one representative engineering group. Include monorepos, remote
development, CI, and dependency-install workflows.

Exit criteria:

- At least 95 percent of managed endpoints load requirements successfully.
- Exception requests identify a business workflow and an owner, not a request
  for unrestricted access.
- Help-desk guidance resolves profile and web-search failures.
- Rollback is tested on one endpoint per operating system.

### Phase 3: organization-wide

Assign the validated policy to the remaining managed population. Roll out by
department and pause if policy-load errors or blocked-workflow tickets exceed
the organization's agreed threshold.

Exit criteria:

- The endpoint inventory shows the intended requirements source and tier.
- Unsupported Codex versions are upgraded or blocked from managed use.
- Security reviews SIEM alerts and approved exceptions on a recurring schedule.

### What will break

| Tier | Expected impact | Developer message |
|------|-----------------|-------------------|
| Strict | Codex cannot edit files, run write-producing tests, or use web search. | "Codex is in review-only mode for this environment. Make changes manually or request a time-bound Moderate assignment for an approved workspace." |
| Moderate | Full-system access, unattended approvals, and live web search are unavailable. | "Codex can edit the active workspace. Use the approved dependency proxy and cached search, and approve supported risky actions when prompted." |
| Baseline | Full-system permission profiles remain unavailable. Live search and unattended operation remain possible. | "Codex is limited to the active workspace. Use a disposable environment for workflows that genuinely require broader host access." |

### Rollback procedure

1. Export the active `/debug-config` output and record the failed workflow.
2. Restore the previously approved `requirements.toml`, rather than deleting
   all requirements.
3. For macOS MDM, replace or remove only
   `com.openai.codex:requirements_toml_base64`, then restart Codex.
4. For Windows or Linux, restore the prior system file and its administrator
   ownership, then restart Codex.
5. For cloud-managed requirements, reassign the previous policy to the affected
   group. Cloud policy can override the system file.
6. Verify the restored effective policy with `/debug-config`.

Communication template:

> We rolled back the Codex permission policy for [group] because [validated
> impact]. The previous approved policy is active again. Restart Codex before
> resuming work. Security will publish a corrected policy after pilot validation.

## Config Files

Choose one tier and deploy it under the exact name `requirements.toml`:

- [`examples/requirements-strict.toml`](examples/requirements-strict.toml)
- [`examples/requirements-moderate.toml`](examples/requirements-moderate.toml)
- [`examples/requirements-baseline.toml`](examples/requirements-baseline.toml)

These files contain no secrets. `config-<tier>.toml` supplies user-facing
defaults, while `requirements-<tier>.toml` enforces limits that local config and
CLI overrides cannot weaken.

## Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|-----------------------|
| `allowed_approval_policies` | `untrusted`, `on-request`, `never` | `untrusted`, `on-request` | `on-request` | Baseline preserves unattended automation; higher tiers require a human approval path. |
| `allowed_web_search_modes` | `cached`, `indexed`, `live` | `cached` | Empty list, so only implicit `disabled` is allowed | Higher tiers reduce external query disclosure and uncontrolled egress. |
| `default_permissions` | `:workspace` | `:workspace` | `:read-only` | Development tiers need workspace edits; Strict is review-only. |
| `allowed_permission_profiles.:read-only` | `true` | `true` | `true` | Every tier needs a non-mutating review mode. |
| `allowed_permission_profiles.:workspace` | `true` | `true` | Omitted, therefore denied | Strict prevents all agent writes; other tiers preserve normal coding. |
| `allowed_permission_profiles.:danger-full-access` | Omitted, therefore denied | Omitted, therefore denied | Omitted, therefore denied | Full host access exposes credentials and files outside version control. |

## Deployment Steps

### Supported paths and precedence

| Platform | System requirements path | Managed delivery |
|----------|--------------------------|------------------|
| macOS | `/etc/codex/requirements.toml` | MDM domain `com.openai.codex`, key `requirements_toml_base64` |
| Linux | `/etc/codex/requirements.toml` | Configuration-management file deployment |
| Windows | `C:\ProgramData\OpenAI\Codex\requirements.toml` | Intune, Group Policy, or Workspace ONE file deployment |

Cloud-managed requirements and macOS MDM can override the local system file.
Do not use `~/.codex/config.toml` for controls that must be non-bypassable.

### macOS, Jamf or Workspace ONE

1. Encode the selected file without line wrapping:

   ```bash
   base64 < examples/requirements-moderate.toml | tr -d '\n'
   ```

2. Create a custom settings profile for preference domain `com.openai.codex`.
3. Set the string key `requirements_toml_base64` to the encoded value.
4. Scope the profile to the pilot smart group and restart Codex after delivery.
5. If MDM is unavailable, deploy the file to `/etc/codex/requirements.toml`
   with owner `root` and mode `0644`.

### Windows, Intune or Workspace ONE

Deploy the selected file to
`C:\ProgramData\OpenAI\Codex\requirements.toml` with a device-context script or
managed application. Grant write access only to `SYSTEM` and Administrators.
Use a detection rule that checks the file hash and the minimum Codex version.

### Linux

Use the endpoint configuration manager to create `/etc/codex`, copy the selected
file as `/etc/codex/requirements.toml`, set owner `root:root`, and set mode
`0644`. A normal user must not be able to replace the file.

### Validation

1. Run `codex --version` and confirm version 0.138.0 or later.
2. Start Codex and enter `/debug-config`.
3. Confirm `default_permissions`, `allowed_permission_profiles`,
   `allowed_approval_policies`, and `allowed_web_search_modes` match the tier.
4. Attempt to select `:danger-full-access`. Codex must reject it or fall back to
   an allowed profile and notify the user.
5. For Strict, attempt a workspace edit and web search. Both must be denied.
6. For Moderate, edit a workspace file, then attempt to read or write outside
   the workspace. The workspace edit must succeed and the host access must fail.

On macOS, `defaults read com.openai.codex requirements_toml_base64 | base64 -d`
can confirm MDM delivery. On Windows, use
`Get-Content "$env:ProgramData\OpenAI\Codex\requirements.toml"`.

### Audit logging and SIEM

Codex OpenTelemetry export is opt-in. Configure OTel in a user or managed
`config.toml`, send it to an organization-controlled collector, and keep
`otel.log_user_prompt = false`. Raw prompts and tool output can contain source
code or secrets. Alternatively, use the ChatGPT Compliance API for auditable
workspace records when the organization's plan supports it.

Alert on:

- attempts to select a denied permission or approval mode;
- repeated requirements parse or policy-load failures;
- denied writes outside the workspace;
- denied or newly enabled MCP servers;
- OTel collector gaps from managed endpoints;
- use of `--yolo` or `--dangerously-bypass-approvals-and-sandbox`.

Local Codex state defaults under `$CODEX_HOME` (normally `~/.codex`). Do not
depend on local plaintext TUI logs as the central audit record because the
plaintext log is opt-in and endpoint files can be altered by the user.

## Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Strict workspace edits | Unreviewed mutation in a regulated environment | Ask Codex for a patch, review it, then apply through the normal code-review process | Assign Moderate only to an approved group and workspace for a fixed period. |
| `:danger-full-access` | Reads credentials and modifies files outside version control | Keep `:workspace`; run required host setup through MDM or a reviewed admin script | Use an isolated disposable VM, never a normal developer endpoint. |
| Moderate live web search | Query text can leave the approved boundary | Use cached search, the internal documentation portal, or an approved browser | Approve a destination through the egress review process before widening policy. |
| Unattended approval in Moderate or Strict | Prompt injection can execute actions without a person reviewing them | Use `on-request`, or run a narrowly scoped CI task in an isolated workspace | Create a separate Baseline automation group with no production credentials. |

Permission allowlists are complete lists. A newly released built-in profile is
denied until an administrator reviews and adds it. This secure default can
cause false-positive friction after upgrades, so test new Codex versions in the
pilot group before organization-wide release.

Codex CLI, the Codex desktop app, and the IDE extension share managed
requirements. Avoid deploying different requirement payloads for each client on
the same endpoint, because the higher-precedence source wins and can create
unexpected behavior.
