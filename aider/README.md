# Aider — Secure Admin Configuration

This directory contains security-hardened configurations for **Aider** (the open-source AI pair programming CLI), targeting administrators and developers who need to enforce safe defaults, prevent credential exposure, and maintain auditability.

## What Is Covered

| File | Purpose |
|------|---------|
| `aider.conf.yml` | Recommended project-level `.aider.conf.yml` template |
| `aiderignore` | Template `.aiderignore` to block sensitive files from AI context |
| `examples/aider-strict.yml` | **Strict** — No auto-commits, no auto-confirm, full audit trail |
| `examples/aider-moderate.yml` | **Moderate** — Balanced settings for development teams |
| `examples/aider-baseline.yml` | **Baseline** — Sensible defaults for individual developers |
| `examples/settings-rationale.md` | Comprehensive security reasoning for every setting |
| `examples/enterprise-policy.md` | Enterprise deployment guide and policy controls |

## What Is Aider

Aider is a CLI AI coding assistant that integrates directly with git. It reads files from the repository into its context window and uses LLMs to generate and apply code changes. Key capabilities:

- Reads source files and git history into AI context
- Writes code changes directly to files (with or without developer review)
- Commits changes to git (with or without developer review)
- Executes lint, test, and build commands automatically
- Runs in "architect" mode (planning agent) and "code" mode (implementation agent)

Aider operates as a privileged process with full read/write access to the project directory and, unless restricted, the entire filesystem the user has access to.

## Configuration File Locations

Aider reads configuration from multiple locations in order of precedence (highest first):

| Location | Scope | Notes |
|----------|-------|-------|
| CLI flags | Per-invocation | Highest precedence |
| `.aider.conf.yml` in project root | Per-project | Committed to repo; visible to all contributors |
| `~/.aider.conf.yml` | Per-user global | Personal defaults; not committed |
| Environment variables | System-wide | `AIDER_MODEL`, `ANTHROPIC_API_KEY`, etc. |

## Critical Security Settings

| Setting | Risk when misconfigured | Safe default |
|---------|------------------------|--------------|
| `yes: true` | Auto-confirms all prompts — AI can make unbounded changes silently | `false` |
| `auto-commits: true` | Commits AI changes to git without developer review | `false` |
| `dirty-commits: true` | Allows committing when there are uncommitted changes (masks provenance) | `false` |
| `llm-history-file` enabled | Stores full LLM conversations including code content to disk | Disable or restrict |
| API keys in config file | Credentials committed to git | Use environment variables |
| `subtree-only: false` | Allows access to entire git tree, not just current directory | Set `true` in monorepos |

## File Locations for Ignore Patterns

Create a `.aiderignore` file at the project root to prevent Aider from reading sensitive files into AI context. It follows `.gitignore` syntax.

**Minimum recommended `.aiderignore` patterns:**
```
.env
.env.*
**/*.pem
**/*.key
**/*.p12
**/.aws/
**/.ssh/
**/secrets/
**/*secret*
**/*credential*
**/*token*
```

See the `aiderignore` template in this directory for a complete list.

## Deployment Checklist

1. Add `aider.conf.yml` to the project root with `auto-commits: false` and `yes: false`.
2. Add `.aiderignore` to the project root with credential and secret patterns.
3. Store API keys in environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) — never in config files.
4. Add `aider.conf.yml` to `.gitignore` if it contains any user-specific settings.
5. Add `.aider.chat.history.md` and `.aider.input.history` to `.gitignore` (may contain sensitive prompts).
6. If `llm-history-file` is used, ensure the file is in `.gitignore` and apply log rotation.
7. For regulated environments, set `no-suggest-shell-commands: true` and review all shell command suggestions manually.
8. Pin the Aider version (`pip install aider-chat==X.Y.Z`) in CI/CD to prevent supply-chain drift.
