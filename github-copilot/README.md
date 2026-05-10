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
| `examples/network-security.md` | Firewall and proxy configuration |
| `examples/content-exclusion-patterns.yml` | Content exclusion pattern examples |
| `examples/settings-vscode.json` | VS Code settings for Copilot security |
| `examples/settings-rationale.md` | Comprehensive rationale for every security setting |

## Configuration Layers

### Organization Level (GitHub Settings)

Organization owners manage Copilot policies at:
**Organization Settings → Copilot → Policies & features**

Key policy controls:
- Enable/disable Copilot for the organization
- Content exclusion rules
- Feature-level toggles (chat, CLI, code review)
- Model selection policies

### Repository Level

Repository admins can set content exclusion rules at:
**Repository Settings → Code & automation → Copilot → Content exclusion**

### Project Level

The `.github/copilot-instructions.md` file provides repository-specific instructions to Copilot, including security guidelines.

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
- May not prevent use of semantic information (e.g., type definitions) from excluded files.
- Maximum ~1,000 lines in instruction files (Copilot code review reads first 4,000 characters).

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
2. Configure content exclusion for secrets, credentials, and sensitive files.
3. Deploy `.github/copilot-instructions.md` to all repositories.
4. Configure firewall rules to allow only business/enterprise Copilot traffic.
5. Set feature policies (enable/disable chat, CLI, code review per org needs).
6. Review and audit Copilot usage through GitHub's audit log.
7. Train developers on responsible Copilot usage and code review practices.
