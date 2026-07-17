# Contributing to AI-Secure-Configs

Thank you for your interest in improving the security of AI coding tools. This guide explains how to contribute new tool configurations, improve existing ones, and ensure your contributions meet the repository's quality standards.

## Getting Started

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/add-tool-name`)
3. Make your changes following the guidelines below
4. Run the validation checks (see [Validation](#validation))
5. Submit a pull request

## Directory Structure for New Tools

Every AI tool in this repository follows a consistent structure. When adding a new tool, create the following:

```
tool-name/
├── README.md                          # Required: deployment checklist and overview
├── [primary-config-file]              # Required: main security config template
├── secure-admin-policy.md             # Required: admin deployment checklist
│   OR secure-org-policy.md
└── examples/
    ├── [config]-strict.[ext]          # Required: strict tier
    ├── [config]-moderate.[ext]        # Required: moderate tier
    ├── [config]-baseline.[ext]        # Required: baseline tier
    └── settings-rationale.md          # Required: rationale for every setting
```

### Required Files

| File | Purpose |
|------|---------|
| `README.md` | Overview, file paths, deployment methods, validation commands |
| Primary config | The main security configuration template with secure defaults |
| Admin/org policy | Checklist-format deployment guide for administrators |
| Strict tier | Maximum security, minimum AI autonomy |
| Moderate tier | Balanced security and productivity |
| Baseline tier | Essential protections only |
| Rationale document | Explains *why* for every setting |

## Configuration Guidelines

### Format Standards

- **JSON:** Use 2-space indentation. Include a `_comment` field at the top explaining deployment location.
- **YAML:** Use 2-space indentation. Include a header comment explaining deployment location.
- **TOML:** Use standard TOML formatting. Include header comments explaining deployment location.
- **Markdown:** Use ATX-style headers (`#`). Use GitHub Flavored Markdown.

### Security Principles

Every configuration MUST follow these principles:

1. **Least Privilege** — Default to the most restrictive settings. Document which settings can be relaxed and under what conditions.
2. **No Secrets in Config** — Never include API keys, tokens, or credentials. Use placeholders like `${{ secrets.API_KEY }}`, `${ENV_VAR}`, or `YOUR_API_KEY_HERE`.
3. **Deny Dangerous Patterns** — Block known-dangerous operations (piped execution, privilege escalation, credential file access).
4. **Audit Trail** — Enable logging and monitoring wherever the tool supports it.
5. **Central Management** — Prefer configurations deployable via MDM, admin console, or config management.

### Tier Definitions

| Tier | Description | Target |
|------|-------------|--------|
| **Strict** | Maximum restrictions. AI has minimal autonomy. Every action requires approval. | Regulated industries, classified environments |
| **Moderate** | Balanced controls. Read-only operations are auto-approved; writes and execution require confirmation. | Most enterprise teams |
| **Baseline** | Essential protections only. Blocks obvious dangers but allows most workflows. | Startups, individual developers |

### Rationale Documents

The `settings-rationale.md` file is the most important documentation artifact. For each setting, include:

```markdown
### setting_name

| Attribute | Detail |
|-----------|--------|
| **What it does** | Clear description of behavior |
| **Why it matters** | The threat it mitigates |
| **Recommended value** | Per-tier recommendation table |
| **Misconfiguration risk** | What goes wrong if set incorrectly |
```

## Validation

Before submitting a PR, ensure:

1. **JSON files parse correctly:**
   ```bash
   find . -name "*.json" -exec python3 -m json.tool {} > /dev/null \;
   ```

2. **YAML files parse correctly:**
   ```bash
   find . -name "*.yaml" -o -name "*.yml" | xargs -I {} python3 -c "import yaml; yaml.safe_load(open('{}'))"
   ```

3. **TOML files parse correctly:**
   ```bash
   find . -name "*.toml" | xargs -I {} python3 -c "import tomllib; tomllib.loads(open('{}').read())"
   ```

4. **No secrets or credentials** are present in any file:
   ```bash
   grep -rn "sk-\|AKIA\|ghp_\|gho_\|password\s*=" --include="*.json" --include="*.yaml" --include="*.toml" .
   ```
   This should return zero results.

5. **Internal links** in Markdown files resolve correctly.

## Pull Request Process

1. **Title format:** `[tool-name] Brief description` (e.g., `[cursor] Add Background Agent security config`)
2. **Description:** Include:
   - What security gap this addresses
   - Which tool version(s) you tested against
   - Any breaking changes from existing configs
3. **Review:** All PRs require at least one security-aware reviewer
4. **Testing:** Describe how you validated the config works as intended

## Reporting Issues

- **Security vulnerabilities:** See [SECURITY.md](./SECURITY.md)
- **Config errors:** Open a GitHub issue with the label `bug`
- **New tool requests:** Open a GitHub issue with the label `new-tool`
- **Improvements:** Open a GitHub issue with the label `enhancement`

## Code of Conduct

Be respectful, constructive, and security-minded. We are all working toward the same goal: making AI coding tools safer for everyone.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).
