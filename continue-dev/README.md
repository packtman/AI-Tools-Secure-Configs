# Continue.dev: Secure Admin Configuration

Security-hardened Continue.dev configs for IT and security admins rolling out AI coding assistance without breaking developer workflows.

**Continue.dev**: open-source AI coding assistant (IDE extension + CLI `cn`) that can read/edit files, run shell commands, call MCP servers, and load Skills.

**MCP**: Model Context Protocol, a way for AI tools to call external services through MCP servers.

**MDM**: Mobile Device Management, software that pushes managed settings to endpoints. Continue.dev has **no MDM managed-settings path**; use onboarding scripts, Mission Control org configs, and CLI wrappers instead.

**SIEM**: Security Information and Event Management, centralized log collection and alerting.

**Mission Control**: Continue's organization config/secrets surface (formerly Hub) for Teams/Enterprise visibility.

---

## 1. Rollout Plan

### Phased rollout

| Phase | Scope | Exit criteria |
|-------|-------|---------------|
| Pilot | 5-15 volunteer developers on one team | Config loads (`name`/`version`/`schema` present), permissions block `UploadArtifact` and `Skills` per tier, no P1 productivity blockers for 5 business days |
| Expanded pilot | One business unit / 50-100 developers | Exception process works within 2 business days, SIEM or endpoint audit of config presence is green, `--auto` wrapper adopted on managed images |
| Org-wide | All Continue users | Compliance sign-off, rollback drill completed, developer FAQ published |

### Pre-rollout checklist

- [ ] Confirm Continue has **no MDM payload** for permissions; choose distribution path (onboarding script, golden image, Mission Control)
- [ ] Secrets manager / Mission Control **org secrets** ready (no inline API keys)
- [ ] SIEM or MDM inventory check for `~/.continue/config.yaml` and `~/.continue/permissions.yaml` presence
- [ ] Rollback package staged (previous `config.yaml` + `permissions.yaml`)
- [ ] Developer announcement drafted (see "What will break")

### What will break (by tier)

| Tier | Likely friction | Developer message (send before rollout) |
|------|-----------------|-----------------------------------------|
| Baseline | Prompts on Bash, Delete, UploadArtifact, Skills | "Continue will ask before shell, deletes, artifact uploads, and Skills. Use `--readonly` for review; do not use `--auto` on corporate laptops." |
| Moderate | Writes/shell/Skills need approval; UploadArtifact and Delete blocked; MCP empty by default | "File edits and terminal commands need your OK. Artifact upload and Delete are disabled. Request MCP servers through the exception process." |
| Strict | Read-only only; no Bash, Fetch, Skills, UploadArtifact, MCP | "Continue is review-only in Strict. Use `--readonly` intentionally. For edits, switch to a Moderate-tier machine or file an exception." |

### Rollback procedure

1. Restore previous files:
   - macOS/Linux: `~/.continue/config.yaml`, `~/.continue/permissions.yaml`
   - Windows: `%USERPROFILE%\.continue\config.yaml`, `%USERPROFILE%\.continue\permissions.yaml`
   - Workspace override: project `.continuerc.json` if deployed
2. Remove any `cn` wrapper that blocks `--auto` if that wrapper caused the incident.
3. Restart the IDE / CLI session.
4. Communication template: "Continue secure config rolled back to prior version at `<timestamp>`. Resume normal workflow. Reply in `#ai-tooling` if permissions still look wrong."

---

## 2. Config Files

| File | Purpose |
|------|---------|
| `config.yaml` | Secure global configuration template (Moderate-leaning defaults) |
| `permissions.yaml` | Tool permission configuration (Moderate default) |
| `examples/config-strict.yaml` | **Strict** config: empty MCP, indexing off, gateway + proxy |
| `examples/config-moderate.yaml` | **Moderate** config: empty MCP default, indexing on, proxy |
| `examples/config-baseline.yaml` | **Baseline** config: essential controls, empty MCP documented |
| `examples/permissions-strict.yaml` | **Strict** permissions: read-only; exclude write/shell/Fetch/Skills/UploadArtifact |
| `examples/permissions-moderate.yaml` | **Moderate** permissions: ask on write/shell/Skills; exclude Delete/UploadArtifact |
| `examples/permissions-baseline.yaml` | **Baseline** permissions: ask on Bash/Delete/UploadArtifact/Skills |
| `examples/config-enterprise.yaml` | Enterprise proxy template |
| `examples/continuerc-secure.json` | Workspace-level `.continuerc.json` |
| `examples/secrets-management.md` | Secrets management guide |
| `examples/settings-rationale.md` | Detailed setting rationales |

Keep only necessary settings: threat mitigations for the tier, or keys required for Continue schema v1 (`name`, `version`, `schema`).

---

## 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `name` / `version` / `schema` | required | required | required | Current Continue schema v1 requires identity metadata |
| `mcpServers` | `[]` | `[]` | `[]` | Explicit deny-by-default MCP posture; expand only via change control |
| `allowAnonymousTelemetry` | `false` | `false` | `false` | Same privacy floor across tiers |
| `disableIndexing` | `false` | `false` | `true` | Strict avoids indexing untrusted/regulated trees |
| Proxy / private `apiBase` | optional | required in examples | required in examples | Enterprise egress control |
| Permissions: Write/Edit | `allow` | `ask` | `exclude` | Increasing human control over mutations |
| Permissions: Bash | `ask` | `ask` | `exclude` | Strict is review-only |
| Permissions: Fetch | `allow` | `allow` | `exclude` | Strict blocks arbitrary network fetches |
| Permissions: Skills | `ask` | `ask` | `exclude` | Skills can expand tool surface |
| Permissions: UploadArtifact | `ask` | `exclude` | `exclude` | Upload path is an exfil risk |
| Permissions: Delete | `ask` | `exclude` | `exclude` | Destructive filesystem ops |
| Permissions: Checklist/Status/CheckBackgroundJob/ReportFailure | `allow` | `allow` | `allow` | Built-in helpers needed for usable sessions |
| `--auto` mode | discouraged | block via wrapper | block via wrapper | Mode overrides all permissions.yaml rules |

---

## 4. Deployment Steps

### File paths

| OS | Config | Permissions |
|----|--------|-------------|
| macOS / Linux | `~/.continue/config.yaml` | `~/.continue/permissions.yaml` |
| Windows | `%USERPROFILE%\.continue\config.yaml` | `%USERPROFILE%\.continue\permissions.yaml` |
| Workspace | `.continuerc.json` in repo root | (permissions remain user/org scoped) |

### MDM / managed enforcement

Continue.dev does **not** ship Jamf / Intune / Workspace ONE managed settings for tool permissions.

Next-best controls:

1. **Onboarding script / golden image** that installs the tier files to the paths above (root-owned or ACL-locked where possible).
2. **Mission Control** org config + org secrets for Teams/Enterprise.
3. **CLI wrapper** on managed PATH that rejects `cn --auto` / `cn -p ... --allow '*'` for Moderate/Strict.
4. **Network egress filter** for unexpected MCP hosts if MCP is later allowlisted.

### Validation commands

```bash
# Confirm config identity and MCP posture
python3 -c "import yaml; c=yaml.safe_load(open('$HOME/.continue/config.yaml')); print(c.get('name'), c.get('version'), c.get('mcpServers'))"

# Confirm permission exclusions
python3 -c "import yaml; p=yaml.safe_load(open('$HOME/.continue/permissions.yaml')); print('exclude=', p.get('exclude')); print('ask=', p.get('ask'))"

# CLI sanity (Continue CLI)
cn --help | head
# Start a session and confirm Skills/UploadArtifact behave per tier
```

In the IDE: open Continue settings and verify the active config name/version; attempt a blocked tool and confirm prompt or exclusion.

### Audit logging / SIEM

Continue does not provide a first-class enterprise audit stream comparable to Copilot or Claude managed settings.

Practical monitoring:

| Signal | How to collect | Alert on |
|--------|----------------|----------|
| Config drift | MDM/osquery inventory of `~/.continue/*.yaml` hashes | Hash != approved tier package |
| `--auto` usage | Shell history / wrapper deny logs | Any `--auto` on managed endpoints |
| MCP additions | Git diff / file integrity on `config.yaml` `mcpServers` | Non-empty or unexpected server names |
| Secrets | Secret scanning in repos | Inline API keys instead of `${{ secrets.* }}` |

Ship wrapper deny logs and osquery results to SIEM. Alert on config hash mismatches and `--auto` denials.

---

## 5. Workflow-Preservation Notes

| Blocked / gated operation | Risk | Safe equivalent |
|---------------------------|------|-----------------|
| `UploadArtifact` (Moderate/Strict exclude) | Exfiltrates workspace content | Share via approved VCS/PR or corporate file transfer |
| `Skills(*)` (Strict exclude; ask on other tiers) | Loads skill packs that expand tools | Vendor-reviewed skill allowlist + exception request |
| `Bash` (Strict exclude) | Arbitrary code execution | Run commands yourself in a normal terminal; or use Moderate tier |
| `Fetch(*)` (Strict exclude) | Arbitrary network retrieval | Download through approved browser/proxy, then attach files locally |
| `Delete` (Moderate/Strict exclude) | Destructive file removal | Delete manually after review |
| `mcpServers` non-empty (all tiers default `[]`) | Third-party tool bridge | Request named MCP server via exception; store secrets as org secrets |
| `cn --auto` | Ignores permissions.yaml | Use default mode, or `--readonly` for review; CI automation only in isolated runners |

### False-positive friction

| Friction | Handling |
|----------|----------|
| Skills prompts on every load (Baseline/Moderate) | Allowlist specific Skills names in `allow` after review; keep `Skills(*)` in ask/exclude otherwise |
| Fetch needed for package docs on Strict | Temporary Moderate exception or manual download process |
| Developers recreate `--auto` aliases | Wrapper + SIEM; educate that `--auto` is for isolated automation only |

### Overlap with other tools

Continue CLI shell/MCP overlaps with **Claude Code**, **Cursor**, and **Codex CLI**. Enforce the same MCP allowlist philosophy and shell expectations across tools so admins do not double-configure contradictory policies or leave one agent host open.

---

## Key Security Concepts (quick reference)

### Tool permission levels

| Level | Behavior |
|-------|----------|
| `allow` | Tool runs automatically without prompting |
| `ask` | Prompts for approval before each use (TUI) |
| `exclude` | Tool is hidden from the agent |

### Operational modes (absolute overrides)

| Mode | Effect |
|------|--------|
| normal (default) | Uses `permissions.yaml` |
| `--readonly` (plan) | Read-focused override; ignores permissions.yaml |
| `--auto` | Allows everything; ignores permissions.yaml |

### Secrets

Prefer **org secrets** (proxied, not shipped to the IDE) over user secrets. Always reference `${{ secrets.SECRET_NAME }}`. Never commit API keys.
