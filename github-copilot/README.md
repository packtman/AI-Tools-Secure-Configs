# GitHub Copilot — Secure Admin Configuration

This directory contains security-hardened configurations for **GitHub Copilot** (Business and Enterprise), targeting organization and enterprise administrators who need to enforce content exclusion, network controls, and feature policies.

## What Is Covered

| File | Purpose |
|------|---------|
| `copilot-instructions.md` | Secure `.github/copilot-instructions.md` template |
| `content-exclusion.md` | Content exclusion configuration guide |
| `examples/org-policy-strict.json` | **Strict** — Most features disabled, broad exclusions (regulated) |
| `examples/org-policy-moderate.json` | **Moderate** — Core features enabled, sensible exclusions (enterprise) |
| `examples/org-policy-baseline.json` | **Baseline** — Most features enabled, minimal exclusions (startups) |
| `examples/org-policy.json` | Organization-level feature policies (reference) |
| `examples/managed-settings-strict.json` | **Strict** enterprise `copilot/managed-settings.json` (MCP allowlist empty, plugins locked) |
| `examples/managed-settings-moderate.json` | **Moderate** enterprise `copilot/managed-settings.json` (GitHub MCP allowlist, org plugin catalog) |
| `examples/managed-settings-baseline.json` | **Baseline** enterprise `copilot/managed-settings.json` (deny root filesystem MCP, block YOLO) |
| `examples/managed-settings-*.jsonc` | Same files with inline comments (strip before deploy) |
| `examples/managed-settings.comments.md` | Key-by-key rationale and tier delta for managed settings |
| `examples/managed-settings-rollout.md` | Rollout plan, deployment paths, MDM, validation, workflow notes |
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
- **MCP**: MCP server availability. Use `copilot/managed-settings.json` `allowedMcpServers` / `deniedMcpServers` as the generally available allowlist (2026-08-06). The AI Controls registry restriction is preview and weaker. GitHub recommends setting registry policy to Allow all when you use managed-settings allowlists.

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

### Enterprise managed settings (client guardrails)

This is a separate control plane from AI Controls. Users cannot loosen most keys.

| Channel | Path | When to use |
|---------|------|-------------|
| Server-managed | `.github-private` repo `copilot/managed-settings.json` | Default. Reviewable in git. Applies after sign-in. |
| MDM | macOS `com.github.copilot`, Windows `HKLM\SOFTWARE\Policies\GitHubCopilot` | Device groups, and policy that must apply before sign-in. Linux has no native MDM. |
| File-based | macOS `/Library/Application Support/GitHubCopilot/managed-settings.json`, Windows `%ProgramFiles%\GitHubCopilot\managed-settings.json`, Linux `/etc/github-copilot/managed-settings.json` | Linux, containers, Codespaces, or when you cannot use `.github-private`. |

MCP allowlists (`allowedMcpServers`, `deniedMcpServers`) are generally available on the GitHub Copilot app, Copilot CLI v1.0.11+, and VS Code v1.109.3+. They are **not** enforced on Copilot cloud agent. Agent Plugins 1.0 are governed with `enabledPlugins`, `extraKnownMarketplaces`, and `strictKnownMarketplaces` in the same file. Full rollout steps: `examples/managed-settings-rollout.md`.

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
7. Deploy `examples/managed-settings-*.json` as `copilot/managed-settings.json` (server-managed, MDM, or file-based). Keep the MCP feature toggle enabled, set registry restriction to Allow all, and use `allowedMcpServers` as the allowlist. See `examples/managed-settings-rollout.md`.
8. Set code review runner configuration at org level (self-hosted for sensitive environments).
9. Create "Manage enterprise AI controls" custom role for AI governance team.
10. Enable audit log streaming to your SIEM.
11. Review agent session activity and audit Copilot usage regularly.
12. Train developers on responsible Copilot usage and code review practices.
