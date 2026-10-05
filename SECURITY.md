# Security Policy

## Reporting a Vulnerability

If you discover a security issue in any configuration template in this repository — such as a bypass for a deny rule, a misconfiguration that could expose credentials, or a pattern that fails to protect sensitive data — please report it responsibly.

### How to Report

**Email:** Open a [GitHub Security Advisory](https://github.com/packtman/AI-Tools-Secure-Configs/security/advisories/new) (preferred) or email the repository maintainers directly.

**Do NOT** open a public GitHub issue for security vulnerabilities. Public disclosure before a fix is available puts users of these configs at risk.

### What to Include

- Which config file(s) are affected
- Description of the vulnerability or misconfiguration
- Steps to reproduce (how an attacker could exploit it)
- Suggested fix (if you have one)
- Which tool version(s) you tested against

### Scope

The following are in scope for security reports:

- Deny rules that can be bypassed (e.g., a glob pattern that fails to match a dangerous path)
- Configurations that, when deployed as documented, expose credentials or sensitive data
- Missing protections that the documentation claims are present
- Template values that, if deployed literally, would create a security weakness
- Race conditions or ordering issues in hook scripts

The following are **out of scope**:

- Vulnerabilities in the AI tools themselves (report those to the tool vendor)
- Feature requests for new tool coverage
- Typos or documentation issues (use regular GitHub issues for these)

### Response Timeline

- **Acknowledgment:** Within 3 business days
- **Assessment:** Within 7 business days
- **Fix:** Within 14 business days for confirmed vulnerabilities
- **Disclosure:** Coordinated disclosure after fix is merged

### Credit

We will credit reporters in the commit message and release notes (unless you prefer to remain anonymous). Let us know your preference when reporting.

## Security Design Principles

All configurations in this repository follow the principles documented in [README.md](./README.md#security-principles):

1. Least Privilege
2. Defense in Depth
3. No Secrets in Config
4. Deny Dangerous Patterns
5. Audit Everything
6. Manage Centrally

## Supported Versions

This repository does not use traditional versioning. All configurations on the `main` branch are considered current. We recommend pulling the latest configs quarterly and comparing against your deployed versions.
