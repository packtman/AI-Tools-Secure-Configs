# Windsurf / Devin Desktop, Secure Admin Configuration

This directory contains security-hardened configurations for **Windsurf**, now shipped as **Devin Desktop** (Cognition). Directory and policy registry paths still use the Windsurf name so existing MDM payloads keep working.

**MDM** means Mobile Device Management: software that pushes managed settings to endpoints. **MCP** means Model Context Protocol: a way for AI tools to call external services through MCP servers. **SIEM** means Security Information and Event Management: centralized log collection and alerting.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security policy checklist |
| `examples/enterprise-policy-strict.json` | **Strict**, No extensions, MCP off, Devin CLI sandbox required (regulated) |
| `examples/enterprise-policy-moderate.json` | **Moderate**, Approved extensions, MCP registry enforced, sandbox optional (enterprise) |
| `examples/enterprise-policy-baseline.json` | **Baseline**, Broad extensions, essential restrictions (startups) |
| `examples/enterprise-policy.json` | Enterprise policy reference (Moderate-aligned) |
| `examples/mdm-policy-linux-moderate.json` | Deployable Linux `/etc/windsurf/policies/policy.json` (Moderate) |
| `examples/mdm-policy-linux-strict.json` | Deployable Linux `/etc/windsurf/policies/policy.json` (Strict) |
| `examples/mcp-config-secure.json` | Secure MCP server configuration |
| `examples/cascade-hooks.md` | Cascade / agent hooks for security enforcement |
| `examples/rbac-roles.json` | RBAC role definitions |
| `examples/settings-rationale.md` | Per-setting rationale and tier deltas |

## Product Naming Note

Cognition rebranded Windsurf as Devin Desktop. Enterprise policies still read:

- Windows: `Software\Policies\Windsurf\Windsurf`
- macOS: sample `.mobileconfig` under `Devin.app/Contents/Resources/app/policies`
- Linux: `/etc/windsurf/policies/policy.json`

VS Code policy paths do **not** apply. Devin Desktop and VS Code policies are separate.

## Key Security Concepts

### Enterprise Policies (device MDM)

Device policies control extension publishers, update mode, telemetry, and feedback. `AllowedExtensions` in MDM files is a **JSON string of publishers** (for example `{"ms-python": true}`), not a list of extension IDs. The `AllowedExtensions` arrays in `enterprise-policy-*.json` are an IT allowlist worksheet; copy the publisher map from `MdmPolicies` into the OS policy file.

### Devin CLI Team Settings (admin portal)

Portal controls (not MDM file keys) include:

- Model allowlists and default model
- Web search (disabled by default for enterprise)
- MCP on/off, MCP allowlist, MCP registry URLs and enforcement
- Terminal permissions (`deny` / `ask` / `allow`)
- Sandbox enforcement (`optional` or `required`), domain allow/deny, `sandbox.excluded`
- Attribution filtering (Enterprise, support-enabled)
- Show "Install Devin CLI" (off by default)
- Devin Local Agent (Enterprise: admin must enable)

### Cascade / Devin Local Overlap

Cascade (editor agent) and Devin Local / Devin CLI both run shell and MCP tools. Configure **both** editor auto-execution and Devin CLI terminal/sandbox settings, or you leave a gap. Do not assume Windsurf team settings automatically cover Devin CLI unless the control is listed on the CLI settings page.

### RBAC

| Role | Capabilities |
|------|-------------|
| Admin | Full access: team management, SSO, analytics, service keys |
| User | Standard access: no administrative permissions |
| Custom | Granular permissions across teams, analytics, indexing, SSO |

### MCP Configuration

Global MCP config historically lived at `~/.codeium/windsurf/mcp_config.json`. Prefer team MCP allowlist / registry enforcement so local files cannot widen access.

## Tier Delta (Devin CLI and MDM)

| Setting | Baseline | Moderate | Strict | Reason |
|---------|----------|----------|--------|--------|
| MDM `AllowedExtensions` | Broad publisher map | Curated publisher map | `{}` (none) | Strict removes extension runtime risk |
| MDM `UpdateMode` | `default` | `manual` | `manual` | Enterprise wants tested updates |
| `enableDevinLocalAgent` | `false` | `false` | `false` | Enterprise gate; enable only after pilot |
| `showInstallDevinCli` | `false` | `false` | `false` | Prevents unmanaged CLI installs |
| `mcpServersEnabled` | `true` | `true` | `false` | Strict removes MCP tool surface |
| `mcpRegistryEnforcement` | `false` | `true` | `true` | Moderate+ only allow registry servers |
| `enableWebSearch` (CLI) | `true` | `false` | `false` | Enterprise default is off |
| `sandboxEnforcement` | `optional` | `optional` | `required` | Required breaks Windows until OS sandbox ships |
| `sandboxExcluded.deny` | empty | `Exec(**)` + `gh` carve-out | `Exec(**)` | Limit escape from sandbox |
| Attribution filtering | off | on | on | License / public-code risk |

## Deployment Steps

### Exact file paths

| OS | Path |
|----|------|
| Windows | Registry `HKLM\Software\Policies\Windsurf\Windsurf` (or `WindsurfInsiders`) via ADMX from the install `policies` folder |
| macOS | MDM `.mobileconfig` from `Devin.app/Contents/Resources/app/policies` |
| Linux | `/etc/windsurf/policies/policy.json` (root-owned, mode `644`) |

### MDM guidance

- **Jamf / Intune / Workspace ONE:** Deploy the macOS profile or Windows ADMX/registry values. For Linux, push the JSON with config management (Ansible, Puppet, Chef).
- After deploy, restart Devin Desktop. Managed settings show a lock / "managed by your organization" indicator.
- Validate: Command Palette → **Show Window Log** for policy parse errors; Settings UI for locked keys.

### Admin portal validation

1. Open `app.devin.ai/org/{orgName}/settings/windsurf` (Devin Enterprise) or `https://windsurf.com/team/cli-settings`.
2. Confirm MCP registry enforcement, sandbox mode, web search, and Install CLI toggle match the chosen tier.
3. On a pilot endpoint, attempt an unapproved MCP server and an unsandboxed CLI session; both should fail under Strict.

### Audit logging / SIEM

- Export Admin Portal analytics and audit events via scoped service keys.
- Alert on: policy file changes, MCP allowlist edits, sandbox enforcement flips, SSO disable, service key creation, attribution filter disable.
- Ship Cascade / Devin Local hook post-events to SIEM when hooks are deployed.

## Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Install any marketplace extension (Strict) | Untrusted code in IDE process | Request publisher addition through exception process |
| Custom / non-registry MCP (Moderate+) | Unaudited local tool execution | Publish server to org MCP registry, then allowlist |
| Web search from Devin CLI (Moderate+) | Uncontrolled egress / data leak | Use approved internal docs MCP or ticketed URL fetch |
| Unsandboxed CLI on Strict | Host compromise via agent commands | Run on macOS/Linux with `bwrap`/`socat` installed; keep Windows on Moderate until sandbox exists |
| `Devin Local` without admin enable | Shadow agent with MCP approvals | Enable for a named pilot group after terminal permission review |
| `curl \| bash` / `sudo` via CLI | Remote code execution | Download, inspect, then run; use package managers |

**False-positive friction:** `sandboxEnforcement: required` hard-fails on Windows and on Linux missing `bubblewrap`/`socat`. Keep Moderate on `optional` until the fleet is ready. Exception requests should cite business need, duration, compensating controls (network egress filter, hook deny rules), and an expiry date.

## Deployment Checklist

1. Configure SSO (OIDC/SAML) and SCIM provisioning.
2. Deploy MDM policies (`MdmPolicies` / `mdm-policy-linux-*.json`).
3. Apply Devin CLI team settings for the chosen tier.
4. Restrict extensions to approved publishers.
5. Configure RBAC with least-privilege custom roles.
6. Implement Cascade hooks for secret scanning and audit logging.
7. Keep Devin Local and Install CLI off until pilot exit criteria pass.
8. Enable analytics dashboards and SIEM shipping.
9. Configure proxy settings for corporate networks.
