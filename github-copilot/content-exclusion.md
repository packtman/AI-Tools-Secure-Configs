# GitHub Copilot — Content Exclusion Configuration Guide

## Repository-Level Exclusion

1. Navigate to **Repository Settings → Code & automation → Copilot → Content exclusion**.
2. Add path patterns to exclude.

### Recommended exclusion patterns

```
- "**/.env"
- "**/.env.*"
- "**/secrets/**"
- "**/*.pem"
- "**/*.key"
- "**/*.p12"
- "**/*.pfx"
- "**/credentials*"
- "**/*secret*"
- "**/token*"
- "**/.aws/**"
- "**/.ssh/**"
- "**/terraform.tfstate"
- "**/terraform.tfstate.backup"
- "**/terraform.tfvars"
```

## Organization-Level Exclusion

1. Navigate to **Organization Settings → Copilot → Content exclusion**.
2. Specify repository and path patterns.

### Example organization exclusion rules

```yaml
# Block secrets across all repositories
"*":
  - "**/.env"
  - "**/.env.*"
  - "**/secrets/**"
  - "**/*.pem"
  - "**/*.key"
  - "**/credentials*"

# Block infrastructure state files
"*":
  - "**/terraform.tfstate"
  - "**/terraform.tfstate.backup"
  - "**/terraform.tfvars"
  - "**/*.auto.tfvars"

# Block specific sensitive repositories entirely
"acme/payroll-service":
  - "**"

"acme/security-configs":
  - "**"
```

## Enterprise-Level Exclusion

Enterprise owners can set exclusions via:
1. **Enterprise Settings → Copilot → Content exclusion**
2. REST API (API version `2026-03-10`):

```bash
curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/enterprises/ENTERPRISE/copilot/content_exclusions \
  -d '{
    "repositories": [
      {
        "name": "acme/*",
        "paths": ["**/.env", "**/.env.*", "**/secrets/**"]
      }
    ]
  }'
```

## CRITICAL: Content Exclusion Does NOT Apply to Agent Mode (as of 2026)

**This is the most important security gap in GitHub Copilot content exclusion.**

As of June 2026, content exclusion rules are **NOT enforced** in the following contexts:

| Context | Exclusion enforced? |
|---------|-------------------|
| IDE completions (Copilot in IDEs) | ✅ Yes |
| Copilot Chat on github.com | ✅ Yes (since January 2025) |
| **GitHub Copilot cloud agent (coding agent)** | ❌ **No** |
| **Copilot CLI** | ❌ **No** |
| **Agent Mode in IDE** | ❌ **No** |

Agentic workflows operate in isolated execution environments that do not inherit repository path-exclusion filters. A file excluded from standard Copilot completions **can still be read by the cloud agent**.

### Workarounds for Agent Mode

1. **Use `excludeAgent` directive** in `.github/instructions/*.instructions.md` files:
   ```yaml
   ---
   applyTo: "**"
   excludeAgent: "coding-agent"
   ---
   Never read or reference files in infra/, .aws/, .ssh/, or secrets/.
   ```

2. **Restrict the GitHub Actions service account permissions** to only the repositories and paths needed — use least-privilege token scopes.

3. **Disable the coding agent** entirely for sensitive repositories:
   - Repository Settings → Copilot → Coding agent → Disable

4. **Use branch protection rules** to require human code review on all agent-generated PRs.

## Agent-Specific Instructions (`.github/instructions/`)

As of July 2025, you can add path-scoped instruction files with `applyTo` and `excludeAgent` frontmatter:

```yaml
---
applyTo: "src/api/**"
excludeAgent: "code-review"
---
Always use parameterized queries. Never log request bodies.
```

These files are reviewed in the same way as source code — include them in mandatory code review policies.

### Security Advisory: CVE-2025-53773 (HIGH — Patched August 2025)

The `.github/copilot-instructions.md` file became an injection vector. Attackers embedded invisible Unicode characters to enable `chat.tools.autoApprove: true` in `.vscode/settings.json`, leading to arbitrary command execution.

**Mitigations (apply even after patching to VS 2022 17.14.12+):**
- Include `.github/copilot-instructions.md` and all `.github/instructions/*.instructions.md` in mandatory code review
- Scan instruction files for invisible Unicode in CI: `grep -rP '[\x{200B}\x{FEFF}]' .github/`
- Never set `chat.tools.autoApprove: true` in any settings file
- Monitor `.vscode/settings.json` for unauthorized `autoApprove` entries

## Verification

After configuring exclusions, verify they are working:

1. Open a file matching an excluded pattern in your IDE.
2. Copilot should not provide suggestions for that file.
3. Check the Copilot status indicator — it should show "Content excluded" or similar.
4. Review audit logs for content exclusion events.
