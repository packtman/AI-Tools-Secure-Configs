# Aider Security Settings — Complete Rationale Guide

This document provides the definitive security reasoning behind every setting in the AI-Secure-Configs Aider configuration. For each setting, it explains what it does, why it matters, the recommended value across three environment tiers, and the consequences of misconfiguration.

## Environment Tiers

| Tier | Description | Risk tolerance |
|------|-------------|----------------|
| **Regulated** | Healthcare, finance, government, defense — HIPAA, SOC 2, FedRAMP, PCI-DSS | Zero tolerance |
| **Standard Enterprise** | Corporate engineering with IP protection requirements | Low tolerance |
| **Developer** | Startups, open-source, individual developers | Moderate tolerance |

---

## 1. Auto-Confirm (`yes`)

### `yes`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider automatically answers "yes" to all confirmation prompts — file edits, command suggestions, commit confirmations, and destructive actions. |
| **Why it matters** | This is the single most dangerous Aider setting. It transforms Aider from a review-gated tool into a fully autonomous agent with no human in the loop. A single prompt injection in a file that Aider reads is sufficient to trigger unbounded file modifications, command execution, and git commits — all without any approval step. |
| **Misconfiguration risk** | With `yes: true`, an attacker who can inject content into a file Aider reads (e.g., a malicious dependency's README, a crafted docstring, a file in a cloned repo) can direct Aider to make arbitrary changes, run arbitrary commands, and commit the results — all silently. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `false` | Non-negotiable. There is no environment where `yes: true` should be deployed. |

---

## 2. Git Commit Controls

### 2.1 `auto-commits`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider automatically commits every change it makes to the repository with a generated commit message. Changes go directly into git history without developer review. |
| **Why it matters** | Auto-commits bypass the code review gate. In a team environment, this means AI-generated code is committed without peer review, potentially introducing bugs, security vulnerabilities, or licensing issues. In an audit context, it makes it harder to distinguish human from AI contributions. |
| **Misconfiguration risk** | With `auto-commits: true`, every AI-generated change becomes a permanent git artifact immediately. If the AI makes a mistake or is misdirected via prompt injection, the erroneous commit is already in history and may trigger CI/CD pipelines before it can be reviewed. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Non-negotiable; all commits must go through review |
| Standard Enterprise | `false` | Require developer to stage and review changes before committing |
| Developer | `false` | Strongly recommended; review all AI changes before committing |

### 2.2 `dirty-commits`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider commits AI changes even when the working tree has uncommitted modifications. This mixes AI and human changes in the same commit. |
| **Why it matters** | Dirty commits obscure provenance. When reviewing commit history, it becomes impossible to determine which changes were made by the developer versus the AI. This complicates security audits, code reviews, and incident response. |
| **Misconfiguration risk** | In an audit, mixed-provenance commits make it difficult to establish what code was human-reviewed. For compliance frameworks that require separation of AI-generated code, dirty commits can make compliance reporting inaccurate. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Required for provenance tracking |
| Standard Enterprise | `false` | Best practice for code review clarity |
| Developer | `false` | Recommended; clean commit history is easier to review |

### 2.3 `attribute-author`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider adds `[aider]` to commit messages for AI-generated commits. This allows git log filtering to identify AI contributions. |
| **Why it matters** | AI attribution is increasingly required by compliance frameworks and governance policies. It allows teams to audit how much code was AI-generated, filter AI commits in code reviews, and satisfy regulatory requirements for human oversight. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `true` | Enables AI contribution tracking; no downside |

---

## 3. History and Audit Files

### 3.1 `chat-history-file`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Specifies the file where Aider saves the conversation history between the developer and the AI. Defaults to `.aider.chat.history.md`. |
| **Why it matters** | Chat history files contain the full conversation context — including the prompts the developer typed, the AI's responses, and the code that was sent as context. In regulated environments, this file may contain IP-sensitive code, PII, or other sensitive data. |
| **Misconfiguration risk** | If this file is committed to git (not in `.gitignore`), all AI conversation history including code is shared with everyone who can access the repository, including external contributors and code hosting platforms. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | Set to `.aider.chat.history.md` and ensure it is in `.gitignore` | Never commit history files |

### 3.2 `llm-history-file`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When set, Aider writes the full API request and response log to this file — every message sent to and received from the LLM API, including all code context. |
| **Why it matters** | LLM history files are the most sensitive logs Aider generates. They contain the complete content of all files sent to the AI (which may include proprietary code, configuration, and data), plus the AI's full responses. In regulated environments, this data must be protected, retained per policy, and not left in plaintext on developer workstations. |
| **Misconfiguration risk** | An LLM history file that grows unbounded can consume significant disk space. If not in `.gitignore`, it will be committed — exposing proprietary code to the git remote. If not encrypted at rest, it is sensitive data on an endpoint. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Disabled (commented out) | If audit trail is needed, route via corporate LLM proxy that logs server-side |
| Standard Enterprise | Optional; if enabled, must be in `.gitignore` with log rotation | Consider corporate proxy logging instead |
| Developer | Optional; ensure it is in `.gitignore` | Useful for debugging |

---

## 4. Shell Command Suggestions

### `suggest-shell-commands`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider can suggest shell commands for the developer to run (e.g., `npm install`, `git rebase`). The commands are displayed; the developer runs them manually. When `false`, Aider never suggests shell commands. |
| **Why it matters** | Even suggested-but-not-auto-executed commands are a social engineering risk. A developer habit of copy-pasting Aider's command suggestions can be exploited via prompt injection: malicious content in a file under analysis causes Aider to suggest a harmful command that the developer runs without scrutinizing. |
| **Misconfiguration risk** | With `yes: true` (in addition to suggestions enabled), suggestions are auto-executed. Even without `yes`, developers who habitually run suggestions without reading them are vulnerable to prompt injection attacks. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Remove the attack surface entirely |
| Standard Enterprise | `true` | Train developers to read suggestions carefully before running |
| Developer | `true` | Be aware of prompt injection risk in untrusted repositories |

---

## 5. Linting and Testing Automation

### 5.1 `auto-lint`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider runs the configured lint command after each code change and feeds lint output back to the AI for self-correction. |
| **Why it matters** | Auto-lint is generally safe — it runs a deterministic, read-only analysis tool and provides output to the AI. The main risk is if the `lint-cmd` is misconfigured to run something with side effects or network access. |
| **Misconfiguration risk** | Low if `lint-cmd` is set to a standard linter. Risk increases if `lint-cmd` runs a script with side effects (e.g., `npm run build && npm publish`). |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` (or explicitly configured) | Disable to reduce automated tool invocations |
| Standard Enterprise | `true` with explicit `lint-cmd` | Set `lint-cmd` to a specific, reviewed command |
| Developer | `true` | Accelerates iteration; low risk with standard linters |

### 5.2 `auto-test`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Aider runs the configured test command after each code change and feeds results back to the AI. |
| **Why it matters** | Tests may have side effects: seeding databases, calling external APIs, writing to shared resources, or running slow integration tests that time out. Auto-test can cause unexpected state changes and consume resources. |
| **Misconfiguration risk** | If `test-cmd` is not configured or points to a broad test suite, auto-test can be slow and produce noise. Integration tests that call external services are particularly risky to auto-run. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Disable; run tests explicitly as part of review |
| Standard Enterprise | `false` by default | Enable only for unit test suites with no side effects |
| Developer | `true` with fast unit tests | Verify `test-cmd` runs only unit tests |

---

## 6. API Key Security

Aider supports several providers: Anthropic, OpenAI, Google, Azure OpenAI, and others. API keys must **never** be placed in `.aider.conf.yml` or any file that could be committed to git.

| Setting | Safe approach | Unsafe approach |
|---------|--------------|-----------------|
| `ANTHROPIC_API_KEY` | Environment variable in shell profile or secrets manager | `api-key: sk-ant-...` in `.aider.conf.yml` |
| `OPENAI_API_KEY` | Environment variable | Inline in config file |
| Any provider key | OS keychain or vault-injected env var | Any config file |

### Checking for accidentally committed keys

```bash
# Scan git history for API key patterns
git log -p | grep -E '(sk-ant-|sk-|AIza|AKIA|ya29\.)'
```

If a key is found in git history, rotate it immediately — it must be considered compromised. Removing it from the current branch is not sufficient; it remains in git history.

---

## 7. `.aiderignore` — Protecting Sensitive Files

The `.aiderignore` file is the primary mechanism for preventing sensitive files from being read into AI context. It must be maintained alongside `.gitignore`.

**Key patterns and why they matter:**

| Pattern | What it blocks | Threat |
|---------|----------------|--------|
| `.env`, `.env.*` | Environment files | API keys, DB passwords, secrets |
| `**/*.pem`, `**/*.key` | Private keys and certificates | TLS/SSH private key exfiltration |
| `**/.aws/credentials` | AWS credential file | Cloud account takeover |
| `**/.kube/config` | Kubernetes config | Cluster access exfiltration |
| `**/*secret*`, `**/*token*` | Secret/token files by name pattern | Broad credential protection |
| `.aider.llm.history` | LLM conversation logs | Prevent recursive context exposure |

Never remove patterns from `.aiderignore` without a documented justification. The default posture should be to add patterns, not remove them.
