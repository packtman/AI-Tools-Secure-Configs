# AI-Secure-Configs

A comprehensive collection of **security-hardened configurations** for popular AI and agentic coding tools. Designed for IT administrators, security teams, and DevOps engineers who need to enforce governance, access control, and data protection policies across their organizations.

## Supported Tools

| Directory | Tool | Key Config Files |
|-----------|------|-----------------|
| [`claude-api/`](./claude-api/) | Anthropic Claude API Platform | Workspace RBAC, rate limits, key policies |
| [`claude-code/`](./claude-code/) | Claude Code (AI coding agent) | `managed-settings.json`, permissions, CLAUDE.md |
| [`claude-desktop/`](./claude-desktop/) | Claude Desktop App | `claude_desktop_config.json`, MDM policies |
| [`cursor/`](./cursor/) | Cursor IDE | `permissions.json`, settings, rules, MDM policies |
| [`openai-platform/`](./openai-platform/) | OpenAI API Platform | Org RBAC, content filters, network security |
| [`codex-cli/`](./codex-cli/) | OpenAI Codex CLI | `config.toml`, sandbox modes, approval policies |
| [`codex-desktop/`](./codex-desktop/) | OpenAI Codex Desktop App | `config.toml`, requirements, MDM policies |
| [`github-copilot/`](./github-copilot/) | GitHub Copilot | Content exclusion, instructions, network routing |
| [`amazon-q-developer/`](./amazon-q-developer/) | Amazon Q Developer | IAM policies, SCPs, KMS encryption |
| [`gemini-cli/`](./gemini-cli/) | Google Gemini CLI | `settings.json`, tool restrictions, sandbox, MCP |
| [`google-gemini/`](./google-gemini/) | Google Gemini | Safety settings, VPC controls, org policies |
| [`windsurf/`](./windsurf/) | Windsurf (Codeium) | Enterprise policies, Cascade Hooks, RBAC |
| [`tabnine/`](./tabnine/) | Tabnine Enterprise | Command permissions, workspace restrictions |
| [`continue-dev/`](./continue-dev/) | Continue.dev | `config.yaml`, permissions, secrets management |

## Quick Start

1. **Choose your tool** — Navigate to the directory for the AI tool you want to secure.
2. **Read the README** — Each directory has a README with a deployment checklist.
3. **Copy configurations** — Adapt the example configs to your organization's requirements.
4. **Deploy** — Use your MDM, config management, or manual deployment to roll out.
5. **Monitor** — Set up audit logging and review regularly.

## Security Principles

Every configuration in this repository follows these core principles:

### 1. Least Privilege
Default to the most restrictive settings. Grant additional permissions only when explicitly required and documented.

### 2. Defense in Depth
Layer security controls — combine tool-level restrictions with network controls, IAM policies, and monitoring.

### 3. No Secrets in Config
API keys, tokens, and credentials are **never** stored in configuration files. Use secrets managers, environment variables, or platform-native secret stores.

### 4. Deny Dangerous Patterns
Block known-dangerous operations by default:
- `curl | bash` / `wget | sh` (piped execution)
- `rm -rf /` (destructive commands)
- `sudo` (privilege escalation)
- Reading `.env`, `.ssh/`, `.aws/` (credential access)

### 5. Audit Everything
Enable logging and monitoring. Export to SIEM. Review regularly.

### 6. Manage Centrally
Use MDM, server-managed settings, or admin consoles to deploy and enforce policies. Local overrides should be restricted.

## Directory Structure

```
AI-Secure-Configs/
├── README.md                    # This file
├── claude-api/                  # Anthropic Claude API Platform
│   ├── README.md
│   ├── secure-org-policy.md
│   └── examples/
├── claude-code/                 # Claude Code (AI coding agent)
│   ├── README.md
│   ├── managed-settings.json
│   ├── settings.json
│   ├── CLAUDE.md
│   └── examples/
├── claude-desktop/              # Claude Desktop App
│   ├── README.md
│   ├── claude_desktop_config.json
│   ├── enterprise-policy.md
│   └── examples/
├── cursor/                      # Cursor IDE
│   ├── README.md
│   ├── permissions.json
│   ├── settings.json
│   ├── rules/security.mdc
│   └── examples/
├── openai-platform/             # OpenAI API Platform
│   ├── README.md
│   ├── secure-org-policy.md
│   └── examples/
├── codex-cli/                   # OpenAI Codex CLI
│   ├── README.md
│   ├── config.toml
│   ├── project-config.toml
│   └── examples/
├── codex-desktop/               # OpenAI Codex Desktop App
│   ├── README.md
│   ├── config.toml
│   ├── enterprise-policy.md
│   └── examples/
├── github-copilot/              # GitHub Copilot
│   ├── README.md
│   ├── copilot-instructions.md
│   ├── content-exclusion.md
│   └── examples/
├── amazon-q-developer/          # Amazon Q Developer
│   ├── README.md
│   ├── secure-admin-policy.md
│   └── examples/
├── gemini-cli/                  # Google Gemini CLI
│   ├── README.md
│   ├── settings.json
│   ├── enterprise-policy.md
│   └── examples/
├── google-gemini/               # Google Gemini
│   ├── README.md
│   ├── secure-admin-policy.md
│   └── examples/
├── windsurf/                    # Windsurf (Codeium)
│   ├── README.md
│   ├── secure-admin-policy.md
│   └── examples/
├── tabnine/                     # Tabnine Enterprise
│   ├── README.md
│   ├── secure-admin-policy.md
│   └── examples/
└── continue-dev/                # Continue.dev
    ├── README.md
    ├── config.yaml
    ├── permissions.yaml
    └── examples/
```

## How to Use

### For Organization Admins

1. Start with the **secure-org-policy.md** or **secure-admin-policy.md** in each tool directory — these are deployment checklists.
2. Read the **settings-rationale.md** in each tool's `examples/` directory — this explains *why* each setting should be enabled or disabled, with per-environment recommendations.
3. Review the example configurations and adapt to your organization's risk profile.
4. Deploy configurations via your MDM, config management tool, or admin console.
5. Train your team on the security policies and provide the documentation.

### For Security Teams

1. Use the deny lists and content exclusion patterns as a baseline.
2. Read the **rationale documents** to understand the threat model behind each setting.
3. Add organization-specific patterns for your sensitive files and paths.
4. Set up monitoring and alerting using the audit logging guides.
5. Schedule quarterly reviews of all AI tool configurations.

### For Developers

1. Review the project-level configs (`.claude/settings.json`, `.cursor/rules/`, `.github/copilot-instructions.md`).
2. Read the rationale docs to understand *why* certain operations are blocked.
3. Commit project-level configs to your repositories for team-wide coverage.
4. Follow the secrets management guides — never hard-code credentials.

## Settings Rationale

Every tool includes a **`settings-rationale.md`** document that explains the reasoning behind each security setting:

- **What it does** — clear description of the setting's behavior
- **Why it matters** — the threat it mitigates or the risk it addresses
- **Recommended value** — per-environment recommendations (Regulated, Standard Enterprise, Developer)
- **What goes wrong** — consequences of misconfiguration

These rationale documents help admins make informed decisions rather than blindly copying configurations. They also serve as documentation for audit and compliance reviews.

## Configuration Strictness Levels

Every tool in this repository provides three configuration tiers — **Strict**, **Moderate**, and **Baseline** — so you can choose the right balance of security and productivity for your environment.

| Level | Description | Use case |
|-------|-------------|----------|
| **Strict** | Maximum restrictions, minimal AI autonomy | Regulated industries, sensitive environments |
| **Moderate** | Balanced security with developer productivity | Most enterprise teams |
| **Baseline** | Essential security only | Startups, individual developers |

### Tier files by tool

| Tool | Strict | Moderate | Baseline |
|------|--------|----------|----------|
| Claude Code | `managed-settings-strict.json` | `managed-settings-moderate.json` | `managed-settings-baseline.json` |
| Codex CLI | `config-strict.toml` | `config-moderate.toml` | `config-baseline.toml` |
| Codex Desktop | `config-strict.toml` / `requirements-strict.toml` | `config-moderate.toml` / `requirements-moderate.toml` | `config-baseline.toml` / `requirements-baseline.toml` |
| Cursor | `permissions-strict.json` | `permissions-moderate.json` | `permissions-baseline.json` |
| Claude Desktop | `config-strict.json` | `config-moderate.json` | `config-baseline.json` |
| Claude API | `org-policy-strict.json` | `org-policy-moderate.json` | `org-policy-baseline.json` |
| Amazon Q Developer | `iam-policy-strict.json` | `iam-policy-moderate.json` | `iam-policy-baseline.json` |
| Continue.dev | `config-strict.yaml` / `permissions-strict.yaml` | `config-moderate.yaml` / `permissions-moderate.yaml` | `config-baseline.yaml` / `permissions-baseline.yaml` |
| GitHub Copilot | `org-policy-strict.json` | `org-policy-moderate.json` | `org-policy-baseline.json` |
| Gemini CLI | `settings-strict.json` | `settings-moderate.json` | `settings-baseline.json` |
| Google Gemini | `safety-settings-strict.json` | `safety-settings-moderate.json` | `safety-settings-baseline.json` |
| OpenAI Platform | `org-policy-strict.json` | `org-policy-moderate.json` | `org-policy-baseline.json` |
| Tabnine | `command-permissions-strict.json` | `command-permissions-moderate.json` | `command-permissions-baseline.json` |
| Windsurf | `enterprise-policy-strict.json` | `enterprise-policy-moderate.json` | `enterprise-policy-baseline.json` |

All tier files are located in each tool's `examples/` directory.

## Contributing

1. Fork this repository.
2. Add or improve configurations for existing or new AI tools.
3. Ensure all examples follow the security principles listed above.
4. Include a README with a deployment checklist for any new tool.
5. Submit a pull request with a clear description of changes.

## Disclaimer

These configurations are provided as **starting points** and should be adapted to your organization's specific security requirements, compliance obligations, and risk tolerance. Always test configurations in a non-production environment before deploying. The authors are not responsible for any security incidents resulting from the use of these configurations.

## License

This project is licensed under the [MIT License](./LICENSE). See individual tool vendor documentation for their respective terms of service and licensing.
