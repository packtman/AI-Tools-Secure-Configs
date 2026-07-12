# GitHub Copilot — Admin Controls Reference

## Overview

GitHub provides centralized admin controls for Copilot through the **AI Controls** tab in enterprise settings and organization settings on GitHub.com. Available to organizations on **Copilot Business** and **Copilot Enterprise** plans. Enterprise administrators manage AI policies, agent governance, MCP server controls, content exclusions, and audit logging from a single consolidated view.

GitHub Copilot features span multiple surfaces: **IDE** (VS Code, JetBrains, Vim/Neovim, Xcode, Eclipse), the **GitHub website** (github.com), **Copilot CLI**, **GitHub Mobile**, and **Copilot cloud agent**. Policies control feature availability across these surfaces.

---

## Admin Interface Access

| Interface | URL | Plans |
|-----------|-----|-------|
| Enterprise AI Controls | Enterprise Settings → AI Controls tab | Enterprise (all orgs) |
| Organization Copilot Settings | Organization Settings → Copilot | Business, Enterprise |
| Content Exclusion | Organization/Repository Settings → Copilot → Content exclusion | Business, Enterprise |

### Roles

| Role | Capabilities |
|------|-------------|
| **Enterprise Owner** | Full AI Controls access: policies, agents, MCP, audit logs |
| **AI Controls Custom Role** | Manage enterprise AI controls via fine-grained permission |
| **Organization Owner** | Manage org-level Copilot policies and content exclusion |
| **Repository Administrator** | Configure repo-level content exclusion and custom instructions |

---

## 1. Policy Structure

### Enterprise-Level Enforcement

| Enforcement Option | Effect |
|--------------------|--------|
| Enabled | Feature enabled for all organizations |
| Disabled | Feature disabled for all organizations |
| Let organizations decide | Delegate to individual org owners |
| Select organizations (agents only) | Explicitly choose which orgs receive access |

### Policy Precedence

- Enterprise policies override organization policies
- Most restrictive policy applies when user has licenses from multiple enterprises
- Within the same enterprise, least restrictive policy applies across organizations
- "Policies for enterprise-assigned users" controls defaults for direct-enterprise users

---

## 2. Copilot Feature Policies

Location: `Enterprise Settings → AI Controls → Copilot`

| Policy | Surfaces | Effect |
|--------|----------|--------|
| Copilot in the IDE | VS Code, JetBrains, Vim, Xcode, Eclipse | Enable/disable code completions and inline suggestions |
| Copilot Chat in the IDE | VS Code, JetBrains | Enable/disable conversational AI in IDE |
| Copilot Chat in GitHub.com | GitHub website | Enable/disable Copilot Chat on github.com |
| Copilot in GitHub Mobile | Mobile app | Enable/disable Copilot in mobile |
| Copilot CLI | Terminal | Enable/disable CLI assistant |
| Copilot in Windows Terminal | Windows Terminal | Enable/disable Windows Terminal integration |
| Copilot code review | GitHub website | Enable/disable AI-powered PR code review |
| Editor inline chat | IDEs | Enable/disable inline chat within editor |
| Copilot vision | VS Code | Enable/disable image understanding in chat |
| Model selection | IDEs, GitHub.com | Allow users to choose models or lock to default |
| User feedback collection | GitHub.com | Opt in/out of feedback data collection |

---

## 3. Agent Policies

Location: `Enterprise Settings → AI Controls → Agents`

| Policy | Effect |
|--------|--------|
| Copilot cloud agent | Enable/disable cloud-based coding agent (per-org selection) |
| Copilot code review (agent) | Enable/disable agentic code review architecture |
| Custom agents | Enable/disable custom agent creation and usage |
| Third-party agents | Allow/block third-party agent access to enterprise repos |
| Agent session visibility | Control who can view agent session activity |

### Custom Agent Management

| Setting | Location | Effect |
|---------|----------|--------|
| Custom agent definitions | `.github-private/agents/*.md` in canonical repo | Define enterprise-wide custom agents |
| Source organization | AI Controls → Agents | Set which org hosts canonical agent definitions |
| Agent API access | AI Controls → Agents | Programmatic custom agent management |
| Agent builder permissions | AI Controls → Agents | Control who can manage enterprise-level custom agents |

### Agent Session Activity

| Capability | Description |
|------------|-------------|
| Session dashboard | View active and recent agent sessions (last 24 hours) |
| Session filtering | Filter by agent type, organization, user, third-party agents |
| Audit log integration | Full audit trail of agent actions with `actor_is_agent` identifier |
| Session details | Trace individual sessions to granular action level |

---

## 4. MCP (Model Context Protocol) Policies

Location: `Enterprise Settings → AI Controls → MCP`

| Policy | Effect |
|--------|--------|
| MCP server availability | Allow or block MCP server usage entirely |
| MCP registry URL | Set enterprise-wide registry for approved MCP servers |
| Strict registry enforcement | Only allow MCP servers from the approved registry (preview) |
| Per-repository MCP config | Allow repo-level `.github/copilot/mcp.json` configuration |

### MCP Governance Scope

| Surface | Governance Method |
|---------|-------------------|
| Copilot CLI | Enterprise MCP registry (private registries) |
| IDEs (VS Code, etc.) | Enterprise MCP registry (private registries) |
| Copilot cloud agent | Repository-level config or enterprise custom agent profiles |

> **Note:** Enterprise MCP policies do not control access to the GitHub MCP Server in third-party applications (Cursor, Windsurf, Claude). That is governed by the GitHub MCP Server's own Policies and Governance documentation.

---

## 5. Content Exclusion

Content exclusion prevents Copilot from accessing specified files or directories.

### Configuration Levels

| Level | Who Configures | Scope |
|-------|----------------|-------|
| Repository | Repository admin | Affects all users working in that repo |
| Organization | Organization owner | Affects all users with a seat from that org |
| Enterprise | Enterprise owner | Affects all users across the enterprise |

### Exclusion Effects

| Copilot Feature | Content Exclusion Respected |
|-----------------|----------------------------|
| Inline suggestions | ✓ |
| Copilot Chat (IDE) | ✓ |
| Copilot Chat (GitHub.com) | ✓ (preview) |
| Copilot code review | ✓ |
| Copilot cloud agent | ✗ (not currently supported) |
| Edit/Agent mode in IDE | ✗ (not currently supported) |

### Configuration

```yaml
# Repository Settings → Copilot → Content exclusion
# Organization Settings → Copilot → Content exclusion
# Paths support glob patterns

- "**/*.env"
- "**/secrets/**"
- "config/production.yml"
- "internal/proprietary/**"
```

---

## 6. Code Review Controls

Location: `Organization Settings → Copilot → Code review`

| Setting | Level | Effect |
|---------|-------|--------|
| Runner type | Organization | Set default runner (GitHub-hosted, self-hosted, or large) |
| Lock runner setting | Organization | Override repository-level runner configurations |
| Content exclusion | Repository/Org/Enterprise | Exclude files from code review context |
| Custom instructions | Repository (`.github/copilot-instructions.md`) | Guide review behavior (no character limit) |
| Auto-review on PR | Repository | Automatically request Copilot review on new PRs |

---

## 7. Identity & Access Management

### License Management

| Setting | Location | Effect |
|---------|----------|--------|
| Organization enablement | Enterprise AI Controls | Enable/disable Copilot for specific orgs |
| Seat assignment | Organization → Copilot → Access | Assign licenses to users or teams |
| Seat type | Organization settings | Copilot Business vs. Copilot Enterprise |
| Enterprise-direct assignment | Enterprise settings | Assign seats directly from enterprise (bypasses org) |

### Access Control

GitHub Copilot relies on GitHub's existing identity platform:

| Capability | Method |
|------------|--------|
| SSO (SAML) | Enterprise/Organization SAML SSO |
| SCIM provisioning | Enterprise/Organization directory sync |
| Team-based access | Assign Copilot to GitHub Teams |
| IP allowlisting | Enterprise IP policy |
| Custom roles | "Manage enterprise AI controls" permission |

---

## 8. Monitoring & Audit

### Audit Logs

| Event Category | Examples |
|----------------|----------|
| Policy changes | AI Controls settings modified |
| License actions | Seat assigned, revoked, plan changed |
| Agent sessions | `agent_session.task` (started, finished, failed) |
| Agentic actions | All agent actions with `actor_is_agent` flag |
| Content exclusion | Exclusion rules created, modified, removed |
| Organization enablement | Copilot enabled/disabled for orgs |

### Audit Log Features

| Capability | Description |
|------------|-------------|
| Retention | 180 days in GitHub; stream for long-term |
| Streaming | Export to SIEM (Splunk, Datadog, Azure Sentinel, etc.) |
| Search | `action:copilot` for plan events; `actor:Copilot` for agent events |
| Agent pre-filter | Agents page automatically filters agentic events |
| Session activity | View all cloud agent sessions from last 24 hours |

### Usage Metrics

| Metric | Plan |
|--------|------|
| Suggestions accepted/rejected | Business+ |
| Active users | Business+ |
| Language breakdown | Business+ |
| Per-org/team usage | Enterprise |
| Agent session metrics | Enterprise |
| API-accessible analytics | Enterprise |

### Compliance Certifications

| Certification | Status |
|---------------|--------|
| SOC 2 Type II | ✓ |
| FedRAMP (via GHEC) | ✓ (Enterprise) |
| HIPAA (via GHEC BAA) | Available |

---

## 9. Deployment

### Plan Comparison

| Capability | Copilot Business | Copilot Enterprise |
|------------|-----------------|-------------------|
| IDE completions | ✓ | ✓ |
| Copilot Chat (IDE) | ✓ | ✓ |
| Copilot Chat (GitHub.com) | ✓ | ✓ |
| Copilot CLI | ✓ | ✓ |
| Content exclusion | ✓ | ✓ |
| Code review | ✓ | ✓ |
| Copilot cloud agent | ✗ | ✓ |
| Custom agents | ✗ | ✓ |
| MCP governance | ✓ | ✓ |
| Enterprise AI Controls tab | ✗ | ✓ |
| Agent session monitoring | ✗ | ✓ |
| Audit log streaming | ✗ | ✓ (GHEC) |
| Knowledge bases (repo indexing) | ✗ | ✓ |
| Custom model fine-tuning | ✗ | ✓ |

---

## 10. Recommended Admin Configuration

### For regulated environments (finance, healthcare)

- [ ] Enforce enterprise SAML SSO with MFA
- [ ] Assign Copilot seats via SCIM-synced teams only
- [ ] Configure comprehensive content exclusion (secrets, proprietary code, compliance-sensitive repos)
- [ ] Disable Copilot cloud agent or restrict to approved orgs
- [ ] Disable third-party agents
- [ ] Set MCP registry with strict enforcement (approved tools only)
- [ ] Lock code review runner to self-hosted for network isolation
- [ ] Stream audit logs to SIEM
- [ ] Disable model selection — lock to approved model
- [ ] Create "Manage enterprise AI controls" custom role for AI governance team
- [ ] Review agent session activity daily
- [ ] Disable Copilot in GitHub Mobile if not needed

### For standard enterprise teams

- [ ] Enable Copilot across all organizations
- [ ] Configure content exclusion for sensitive directories
- [ ] Enable Copilot code review with custom instructions
- [ ] Allow MCP servers from approved registry
- [ ] Enable cloud agent for approved organizations
- [ ] Set up custom agents for common workflows
- [ ] Stream audit logs for compliance
- [ ] Review usage metrics quarterly
- [ ] Allow model selection for developer flexibility

### For developer-focused organizations

- [ ] Enable all Copilot features
- [ ] Configure minimal content exclusion (secrets only)
- [ ] Enable cloud agent and custom agents
- [ ] Allow MCP servers broadly with denylist for known-risky ones
- [ ] Enable code review auto-trigger on PRs
- [ ] Monitor adoption via usage metrics
- [ ] Allow model selection

---

## Cross-References

- **GitHub Copilot config files:** [`../github-copilot/`](../github-copilot/) — IDE settings, content exclusion templates
- **Enterprise AI Controls changelog:** [GitHub Blog — AI Controls GA](https://github.blog/changelog/2026-02-26-enterprise-ai-controls-agent-control-plane-now-generally-available/)
- **MCP governance:** [GitHub MCP Server — Policies and Governance](https://github.com/github/github-mcp-server)
