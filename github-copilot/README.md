# GitHub Copilot — Secure Admin Configuration

This directory contains security-hardened configurations for **GitHub Copilot** (Business and Enterprise), targeting organization and enterprise administrators who need to enforce content exclusion, network controls, and feature policies.

## What Is Covered

| File | Purpose |
|------|---------|
| `copilot-instructions.md` | Secure `.github/copilot-instructions.md` template |
| `content-exclusion.md` | Content exclusion configuration guide |
| `examples/managed-settings-strict.json` | Deployable Strict enterprise managed settings |
| `examples/managed-settings-moderate.json` | Deployable Moderate enterprise managed settings |
| `examples/managed-settings-baseline.json` | Deployable Baseline enterprise managed settings |
| `examples/managed-settings-*.jsonc` | Commented copies with what, why, and breakage rationale |
| `examples/managed-settings-*.comments.md` | Audit rationale for each managed setting |
| `examples/org-policy-strict.json` | **Strict** — Most features disabled, broad exclusions (regulated) |
| `examples/org-policy-moderate.json` | **Moderate** — Core features enabled, sensible exclusions (enterprise) |
| `examples/org-policy-baseline.json` | **Baseline** — Most features enabled, minimal exclusions (startups) |
| `examples/org-policy.json` | Organization-level feature policies (reference) |
| `examples/network-security.md` | Firewall and proxy configuration |
| `examples/content-exclusion-patterns.yml` | Content exclusion pattern examples |
| `examples/settings-vscode.json` | VS Code settings for Copilot security |
| `examples/settings-rationale.md` | Comprehensive rationale for every security setting |

## Configuration Layers

### Enterprise Level (AI Controls)

Enterprise owners manage AI policies at:
**Enterprise Settings → AI Controls tab**

AI Controls categories:
- **Copilot** — Feature policies (IDE, Chat, CLI, Mobile, Vision, code review, model selection)
- **Agents** — Cloud agent, code review agent, custom agents, third-party agents
- **MCP** — MCP server availability, registry URL, strict enforcement

### Enterprise Managed Settings

GitHub Copilot supports a vendor-defined `managed-settings.json` file for Copilot CLI and VS Code.
Use it in addition to AI Controls for client-side permission, plugin marketplace, and OpenTelemetry
policy. OpenTelemetry is a standard for exporting usage events to an approved collector.

Deployment channels, from highest to lowest precedence:

1. Native MDM: `HKLM\SOFTWARE\Policies\GitHubCopilot` on Windows or managed preferences in the
   `com.github.copilot` domain on macOS.
2. Server-managed: `copilot/managed-settings.json` in the selected organization's
   `.github-private` repository.
3. File-based: `/Library/Application Support/GitHubCopilot/managed-settings.json` on macOS,
   `%ProgramFiles%\GitHubCopilot\managed-settings.json` on Windows, or
   `/etc/github-copilot/managed-settings.json` on Linux.
4. User settings.

File-based settings must be root-owned, must not be world-writable, and must not be a symbolic link.
Server and MDM policy refreshes within about one hour. Restart the client, sign in again, or run
`Developer: Sync Account Policy` in VS Code to force a policy refresh during a pilot.

### Organization Level (GitHub Settings)

Organization owners manage Copilot policies at:
**Organization Settings → Copilot → Policies & features**

Key policy controls:
- Enable/disable Copilot for the organization
- Content exclusion rules
- Code review runner configuration
- Feature-level toggles delegated from enterprise

### Repository Level

Repository admins can set content exclusion rules at:
**Repository Settings → Code & automation → Copilot → Content exclusion**

### Project Level

The `.github/copilot-instructions.md` file provides repository-specific instructions to Copilot, including security guidelines. No character limit for code review instructions.

## Content Exclusion

Content exclusion prevents Copilot from accessing or suggesting content from specified files and directories. Exclusions are specified using fnmatch patterns (case insensitive).

### Scope

| Level | Who configures | Applies to |
|-------|---------------|------------|
| Repository | Repository admins | That repository only |
| Organization | Organization owners | All repos in the org (can target specific repos) |
| Enterprise | Enterprise owners | All orgs under the enterprise |

### Limitations

- Does not apply to symbolic links or remote filesystems.
- Does not apply to Copilot cloud agent.
- Does not apply in Edit and Agent modes of Copilot Chat in VS Code and other editors.
- Content exclusion on GitHub.com and GitHub Mobile is in public preview.

## Network Security

### Subscription-Based Network Routing

Control which Copilot plans can access the network:

| Plan | Hostname pattern |
|------|-----------------|
| Copilot Business | `*.business.githubcopilot.com` |
| Copilot Enterprise | `*.enterprise.githubcopilot.com` |
| Copilot Individual/Free | `*.individual.githubcopilot.com` |

**Block individual plan usage on corporate networks** by adding `*.individual.githubcopilot.com` to your firewall's blocklist while allowing `*.business.githubcopilot.com`.

## Deployment Checklist

1. Enable Copilot Business/Enterprise at the organization level.
2. Configure enterprise-level AI Controls (feature, agent, and MCP policies).
3. Configure content exclusion for secrets, credentials, and sensitive files.
4. Deploy `.github/copilot-instructions.md` to all repositories.
5. Configure firewall rules to allow only business/enterprise Copilot traffic.
6. Set agent policies (disable cloud agent, custom agents, and third-party agents for regulated environments).
7. Configure MCP registry and decide on strict enforcement.
8. Keep Copilot code review on a GitHub-hosted runner with its firewall enabled. Self-hosted code
   review runners do not support GitHub's firewall, so use them only with equivalent network controls.
9. Create "Manage enterprise AI controls" custom role for AI governance team.
10. Enable audit log streaming to your SIEM.
11. Review agent session activity and audit Copilot usage regularly.
12. Deploy the selected `managed-settings-*.json` template through server management, MDM, or a
    root-owned file, and validate bypass mode and telemetry behavior.
13. Train developers on responsible Copilot usage and code review practices.
