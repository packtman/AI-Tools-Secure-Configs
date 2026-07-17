# Gap Analysis: AI-Secure-Configs

This document identifies missing configurations, tooling gaps, and structural improvements for the AI-Secure-Configs repository. It is organized by priority (Critical > High > Medium > Low) and category.

---

## 1. Missing AI Tool Coverage (High Priority)

The following widely-adopted AI coding tools have no configuration templates in this repository. Each represents a significant enterprise adoption surface that security teams need to govern.

### 1.1 Aider (Open-Source AI Pair Programming)

**Why it matters:** Aider is one of the most popular open-source AI coding tools with thousands of active users. It connects to multiple LLM providers (OpenAI, Anthropic, local models) and executes code directly in the developer's environment.

**Config surface:**
- `.aider.conf.yml` — Global and project-level configuration
- `.aiderignore` — Files excluded from AI context (similar to `.gitignore`)
- Environment variables for API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Model selection and token limits
- Auto-commit behavior (can commit code without review)
- Git integration settings

**Security concerns:**
- Auto-commits can push unreviewed AI-generated code
- No built-in sandbox; runs with full user permissions
- API keys typically stored as environment variables with no rotation enforcement
- No enterprise management plane (no MDM, no admin console)
- `.aiderignore` must be manually maintained to prevent credential file access

**Recommended configs to add:**
- `aider/config.yml` — Secure defaults (disable auto-commit, restrict model access)
- `aider/.aiderignore` — Comprehensive exclusion patterns
- `aider/examples/` — Strict/Moderate/Baseline tiers
- `aider/secure-usage-policy.md` — Since Aider has no admin console, provide a usage policy for developers

---

### 1.2 Cline (VS Code AI Agent Extension)

**Why it matters:** Cline (formerly Claude Dev) is among the most installed AI coding extensions for VS Code. It provides full agentic capabilities including file creation, terminal execution, and browser automation directly within the IDE.

**Config surface:**
- VS Code `settings.json` keys (prefixed with `cline.`)
- Custom instructions file
- Auto-approve settings for file read/write/execute
- MCP server configuration
- API key storage (VS Code secrets API)
- Browser automation permissions

**Security concerns:**
- Auto-approve mode can execute shell commands without user confirmation
- Browser automation capability (similar risk to Cursor computer use)
- MCP server support with no centralized management
- No enterprise admin console or MDM support
- Custom instructions can be overridden per-workspace (prompt injection vector)
- Extension marketplace install — no enterprise gating

**Recommended configs to add:**
- `cline/settings-vscode.json` — VS Code settings for Cline with secure defaults
- `cline/custom-instructions.md` — Security-focused agent instructions
- `cline/examples/` — Strict/Moderate/Baseline auto-approve configurations
- `cline/secure-admin-policy.md` — Compensating controls (since no native enterprise admin)

---

### 1.3 JetBrains AI Assistant

**Why it matters:** JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.) have massive enterprise adoption. JetBrains AI Assistant is tightly integrated and configured through both IDE settings and the JetBrains admin portal.

**Config surface:**
- IDE-level settings (`Settings > Tools > AI Assistant`)
- JetBrains organization admin panel
- License server restrictions
- Code completion scope restrictions
- Full-line completion settings
- Chat and inline AI settings
- Cloud/local model selection

**Security concerns:**
- Code context sent to JetBrains cloud or third-party models
- No granular file exclusion (limited `.gitignore` respect)
- Organization admin policies limited in scope compared to Copilot
- Offline mode not enforced — developers can switch to cloud models
- No content exclusion equivalent to Copilot's pattern-based filtering

**Recommended configs to add:**
- `jetbrains-ai/admin-policy.json` — Organization admin settings
- `jetbrains-ai/ide-settings.xml` — IDE-level AI security settings
- `jetbrains-ai/examples/` — Tiered configurations
- `jetbrains-ai/secure-admin-policy.md` — Admin deployment checklist

---

### 1.4 Sourcegraph Cody

**Why it matters:** Sourcegraph Cody is an enterprise-focused AI coding assistant with deep codebase understanding (via Sourcegraph's code graph). It has its own admin console, RBAC, and enterprise deployment model.

**Config surface:**
- Sourcegraph admin site configuration (JSON)
- Cody context filters (repository-level and org-level)
- Embedding policies (which repos are indexed)
- Model provider configuration
- Rate limiting
- RBAC and access policies
- VS Code / JetBrains extension settings

**Security concerns:**
- Codebase indexing means the entire repo content is processed and stored
- Context window can pull code from repos the developer has access to but shouldn't see AI-summarized
- Enterprise context filters are the primary security control
- Model provider selection (Anthropic, OpenAI, custom) affects data residency
- Admin console permissions need careful RBAC

**Recommended configs to add:**
- `sourcegraph-cody/site-config.json` — Secure site configuration
- `sourcegraph-cody/context-filters.json` — Repository and path exclusions
- `sourcegraph-cody/examples/` — Tiered enterprise configurations
- `sourcegraph-cody/secure-admin-policy.md` — Deployment checklist

---

### 1.5 Augment Code

**Why it matters:** Augment Code is gaining enterprise traction as an AI coding assistant with emphasis on codebase understanding and enterprise security features.

**Config surface:**
- Organization admin dashboard
- Context policies (which repos/files are indexed)
- Model selection and data residency
- SSO/SCIM integration
- API access controls

**Recommended configs to add:**
- `augment-code/secure-admin-policy.md` — Admin deployment checklist
- `augment-code/examples/org-policy.json` — Organization security settings

---

## 2. Missing Repository Infrastructure (Critical)

### 2.1 SECURITY.md — Responsible Disclosure Policy

**Status:** Missing (ironic for a security-focused repository)

**Why it matters:** If someone discovers a vulnerability in one of the recommended configurations (e.g., a bypass for a deny rule, or a misconfiguration that exposes credentials), there is no documented way to report it. A `SECURITY.md` file tells researchers how to report issues responsibly.

**Action:** Add `SECURITY.md` with:
- Contact method for vulnerability reports
- Expected response timeline
- Scope (what counts as a vulnerability in config templates)
- Credit policy

---

### 2.2 CONTRIBUTING.md — Contribution Guidelines

**Status:** Missing (only 5-line section in README)

**Why it matters:** Contributors need clarity on:
- How to structure new tool directories
- Required files per tool (README, tiers, rationale, deployment checklist)
- JSON/YAML/TOML style guidelines
- How to document security rationale
- PR review process and security review requirements

**Action:** Add detailed `CONTRIBUTING.md`.

---

### 2.3 CI/CD Pipeline for Config Validation

**Status:** No `.github/workflows/` directory exists

**Why it matters:** Configuration files can have syntax errors, inconsistencies, or drift from documented structure. An automated pipeline catches:
- Invalid JSON (missing commas, trailing commas, bad escapes)
- Invalid YAML (indentation errors, type coercion issues)
- Invalid TOML (type mismatches, missing sections)
- Broken internal links in Markdown
- Consistent file naming across tool directories

**Action:** Add `.github/workflows/validate-configs.yml` with JSON, YAML, TOML linting.

---

### 2.4 GitHub Repository Infrastructure

**Status:** No `.github/` directory at all

**Missing files:**
- `.github/ISSUE_TEMPLATE/bug_report.md` — For reporting config errors
- `.github/ISSUE_TEMPLATE/new_tool_request.md` — For requesting new tool coverage
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template ensuring security review
- `.github/CODEOWNERS` — Assign security reviewers to config changes
- `.github/FUNDING.yml` — If applicable

---

## 3. Missing Cross-Cutting Content (Medium Priority)

### 3.1 Tool Comparison Matrix

**Status:** Missing

**Why it matters:** Admins need to compare security capabilities across tools to make procurement and deployment decisions. A comparison matrix showing feature parity helps answer: "Which tools support managed settings? Which have MDM? Which have audit logging?"

**Recommended content:**

| Capability | Cursor | Claude Code | Copilot | Codex CLI | Gemini CLI | Windsurf | Cline | Aider |
|-----------|--------|-------------|---------|-----------|------------|----------|-------|-------|
| Admin console | Team Dashboard | Claude.ai Admin | GitHub Org | None | None | Enterprise Portal | None | None |
| MDM support | Yes | Yes | N/A (server-side) | No | No | Yes | No | No |
| File exclusion | settings.json | deny rules | Content exclusion | N/A | .geminiignore | Cascade Hooks | Manual | .aiderignore |
| Audit logging | No (compensating) | Hooks | GitHub Audit Log | OTLP | No | Analytics | No | No |
| Sandbox | No | Yes (OS-level) | N/A | Yes (Docker/seatbelt) | Docker | No | No | No |
| MCP support | Yes | Yes | No | No | Yes | Yes | Yes | No |
| Deny rules | Terminal allowlist | Pattern-based | Content exclusion | approval_policy | Tool whitelist | Cascade Hooks | Auto-approve | None |

---

### 3.2 Compliance Mapping Document

**Status:** Missing

**Why it matters:** Many enterprises adopt AI coding tools under compliance frameworks (SOC 2, ISO 27001, NIST 800-53, HIPAA, FedRAMP). A mapping document shows which configs address which compliance controls.

**Example mappings:**
- SOC 2 CC6.1 (Logical Access) → Cursor `AllowedTeamId`, Claude Code `forceLoginOrgUUID`
- SOC 2 CC7.2 (Monitoring) → Claude Code hooks, Copilot audit log
- NIST AC-6 (Least Privilege) → All deny rules, terminal allowlists
- NIST AU-2 (Audit Events) → Audit logging configs across all tools

---

### 3.3 MCP Security Assessment Framework

**Status:** Partial (Claude Code has `mcp-security.md`, but other MCP-capable tools lack guidance)

**Why it matters:** MCP is supported by Cursor, Claude Code, Gemini CLI, Windsurf, and Cline. A unified MCP security assessment framework would help teams evaluate MCP servers consistently regardless of which AI tool connects to them.

**Recommended content:**
- MCP server vetting checklist (applies to all tools)
- Permission scoping guidelines
- Network isolation recommendations
- Approved server registry template

---

### 3.4 Incident Response Playbook

**Status:** Missing (rollout guide has rollback procedures but no IR playbook)

**Why it matters:** When an AI tool is involved in a security incident (credential leak, data exfiltration, unauthorized access), responders need a tool-specific playbook.

**Recommended content:**
- How to identify AI-tool-related incidents
- Evidence collection per tool (where are logs, session transcripts, audit trails)
- Containment steps per tool (revoke access, kill sessions, block network)
- Recovery steps
- Post-incident config hardening

---

### 3.5 Supply Chain Security for AI Tool Extensions/Plugins

**Status:** Not addressed

**Why it matters:** AI coding tools rely on extensions, plugins, and MCP servers that are installed from public registries. There is no guidance on verifying the integrity and safety of these components.

**Recommended content:**
- Extension vetting process (VS Code marketplace, JetBrains marketplace)
- MCP server package verification
- Dependency scanning for tool plugins
- Pinning extension versions in MDM profiles

---

## 4. Gaps Within Existing Tool Configurations (Medium Priority)

### 4.1 Cursor — Missing Configs

| Gap | Description |
|-----|-------------|
| Background Agent policies | Cursor's Background Agent (separate from Cloud Agent) has its own security surface — no config template exists |
| `.cursorrules` legacy format | Some teams still use the legacy root-level `.cursorrules` file; no migration guide provided |
| Extension allowlist template | No template for restricting which VS Code extensions can be installed alongside Cursor |
| Cursor Tab (autocomplete) scope restrictions | No guidance on restricting which files Cursor Tab can read for context |

### 4.2 Claude Code — Minor Gaps

| Gap | Description |
|-----|-------------|
| Max turns / token budget controls | No config for limiting agent autonomy by capping turns or token spend |
| Session isolation guidance | No guidance on isolating Claude Code sessions from each other in multi-project environments |
| CI/CD integration security | No template for securing Claude Code when used in CI pipelines (GitHub Actions, etc.) |

### 4.3 GitHub Copilot — Missing Configs

| Gap | Description |
|-----|-------------|
| Copilot Extensions policy | GitHub Copilot Extensions (third-party agents) are not addressed |
| Copilot Workspace security | No guidance on GitHub Copilot Workspace (the agentic PR environment) |
| Copilot code review policy | Missing detailed config for Copilot's code review feature (model access to PRs) |
| Branch-level exclusions | No template for excluding specific branches from Copilot context |

### 4.4 Gemini CLI — Minor Gaps

| Gap | Description |
|-----|-------------|
| `.geminiignore` template | Referenced in config but no template provided |
| Extensions/plugin security | Gemini CLI supports extensions; no vetting guidance |

### 4.5 Codex CLI / Desktop — Minor Gaps

| Gap | Description |
|-----|-------------|
| Hooks implementation examples | `hooks-config.json` exists for CLI but no example hook scripts (unlike Claude Code which has 6) |
| Network allowlist for `full-auto` mode | No guidance on restricting network when sandbox allows network access |

---

## 5. Structural Improvements (Low Priority)

### 5.1 Versioning

**Status:** No versioning scheme

**Recommendation:** Add semantic versioning or date-based versioning to track config changes. Security teams need to know when configs were last updated and whether they're running the latest recommended version.

### 5.2 Machine-Readable Metadata

**Status:** Configs have `_comment` fields but no structured metadata

**Recommendation:** Consider adding a `metadata.json` to each tool directory with:
- Tool version the config was tested against
- Last review date
- Applicable compliance frameworks
- Breaking changes from previous versions

### 5.3 Config Validation Scripts

**Status:** None

**Recommendation:** Add a `scripts/` directory with:
- `validate-json.sh` — Validates all JSON files (strips comments from JSONC first)
- `validate-yaml.sh` — Validates all YAML files
- `validate-toml.sh` — Validates all TOML files
- `check-links.sh` — Verifies internal Markdown links
- `check-structure.sh` — Verifies each tool dir has required files (README, tiers, rationale)

---

## 6. Summary: Priority Actions

| # | Action | Priority | Effort |
|---|--------|----------|--------|
| 1 | Add `SECURITY.md` | Critical | Low |
| 2 | Add CI/CD config validation workflow | Critical | Low |
| 3 | Add `CONTRIBUTING.md` | High | Low |
| 4 | Add Aider configs (`aider/`) | High | Medium |
| 5 | Add Cline configs (`cline/`) | High | Medium |
| 6 | Add JetBrains AI configs (`jetbrains-ai/`) | High | Medium |
| 7 | Add Sourcegraph Cody configs (`sourcegraph-cody/`) | High | Medium |
| 8 | Add `.github/` infrastructure (templates, CODEOWNERS) | Medium | Low |
| 9 | Add tool comparison matrix | Medium | Low |
| 10 | Add compliance mapping document | Medium | Medium |
| 11 | Add MCP security assessment framework (cross-tool) | Medium | Medium |
| 12 | Add incident response playbook | Medium | Medium |
| 13 | Fill gaps in existing tool configs (Section 4) | Medium | Medium |
| 14 | Add Augment Code configs | Low | Medium |
| 15 | Add versioning and metadata scheme | Low | Low |
