# Aider — Enterprise Deployment and Policy Guide

This document covers how to deploy Aider securely at enterprise scale — standardizing configurations, managing API keys, enforcing safe defaults, and maintaining audit trails.

## Deployment Strategy

Aider is a developer-installed CLI tool. Unlike IDE extensions or SaaS platforms, it does not have a central admin console or MDM-managed settings. Enterprise governance is achieved through a combination of:

1. **Repository-level defaults** — `aider.conf.yml` in project roots, committed to git
2. **Organization-wide dotfiles** — `~/.aider.conf.yml` deployed via config management
3. **Environment variable management** — API keys via secrets managers
4. **Supply chain pinning** — Pinned versions in CI/CD and developer toolchains
5. **Network controls** — Proxy routing and egress filtering for LLM API traffic

---

## 1. Repository-Level Configuration

Add `.aider.conf.yml` to every repository with organization-approved security defaults:

```yaml
# .aider.conf.yml — Org-approved Aider security defaults
# Maintained by: Platform Engineering / Security
# Policy: All AI changes must be reviewed before commit; no auto-confirm

model: claude-sonnet-4-6
yes: false
auto-commits: false
dirty-commits: false
git: true
gitignore: true
aiderignore: .aiderignore
attribute-author: true
suggest-shell-commands: true
auto-lint: true
analytics: false
analytics-disable: true
```

Add this to the organization's repository template so all new repos start with safe defaults.

### `.gitignore` Additions

Every repository must add Aider's history files to `.gitignore`:

```
# Aider AI assistant files
.aider.chat.history.md
.aider.input.history
.aider.llm.history
```

---

## 2. Organization-Wide Developer Defaults

Deploy `~/.aider.conf.yml` to all developer workstations via config management (Ansible, Chef, Puppet):

```yaml
# Ansible task: deploy Aider global config
- name: Deploy Aider global security defaults
  copy:
    dest: "{{ ansible_env.HOME }}/.aider.conf.yml"
    content: |
      model: claude-sonnet-4-6
      yes: false
      auto-commits: false
      dirty-commits: false
      attribute-author: true
      analytics: false
      analytics-disable: true
    mode: '0644'
    backup: yes
```

---

## 3. API Key Management

### Vault-Injected Environment Variables (Recommended)

```bash
# Example: HashiCorp Vault
export ANTHROPIC_API_KEY=$(vault kv get -field=api_key secret/ai-tools/anthropic)

# Example: AWS Secrets Manager
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id prod/ai-tools/anthropic-api-key \
  --query SecretString --output text | jq -r .api_key)

# Example: GCP Secret Manager
export ANTHROPIC_API_KEY=$(gcloud secrets versions access latest \
  --secret="anthropic-api-key" --format='get(payload.data)' | base64 -d)
```

### Shell Profile Integration

```bash
# Add to /etc/profile.d/ai-tools.sh for system-wide deployment
# Keys are fetched at login; never stored in dotfiles
if command -v vault &>/dev/null; then
    export ANTHROPIC_API_KEY=$(vault kv get -field=api_key secret/ai-tools/anthropic 2>/dev/null)
fi
```

### Detecting Leaked Keys

Add a pre-commit hook to all repositories:

```bash
#!/bin/bash
# .git/hooks/pre-commit — Check for AI provider key patterns

KEY_PATTERNS=(
    'sk-ant-[a-zA-Z0-9_-]+'     # Anthropic
    'sk-[a-zA-Z0-9]{48}'        # OpenAI
    'AIza[a-zA-Z0-9_-]{35}'     # Google
    'AKIA[A-Z0-9]{16}'          # AWS
)

for pattern in "${KEY_PATTERNS[@]}"; do
    if git diff --cached | grep -qE "$pattern"; then
        echo "ERROR: Potential API key detected in staged changes."
        echo "Pattern: $pattern"
        echo "Remove the key and use environment variables instead."
        exit 1
    fi
done
```

---

## 4. Version Pinning

Pin Aider to a specific version in CI/CD and developer requirements files to prevent supply-chain drift:

```bash
# requirements.txt or requirements-dev.txt
aider-chat==0.68.0

# Or in a Makefile
install-aider:
    pip install aider-chat==0.68.0
```

Review and update the pinned version quarterly, after reviewing the changelog for security-relevant changes.

---

## 5. Network Controls

LLM API traffic from Aider can be routed through a corporate proxy for inspection, logging, and egress control.

### HTTP Proxy

```bash
# Set in shell profile or via config management
export HTTPS_PROXY=https://corporate-proxy.example.com:3128
export HTTP_PROXY=http://corporate-proxy.example.com:3128
export NO_PROXY=localhost,127.0.0.1,.internal.example.com
```

### Egress Firewall Rules

Allow outbound HTTPS only to approved AI provider endpoints:

| Provider | Endpoints to allow |
|----------|-------------------|
| Anthropic | `api.anthropic.com:443` |
| OpenAI | `api.openai.com:443` |
| Google | `generativelanguage.googleapis.com:443` |
| Azure OpenAI | `<your-resource>.openai.azure.com:443` |

Block all other outbound connections from developer workstations to prevent data exfiltration via curl or wget commands that Aider might suggest.

---

## 6. Audit Trail

### LLM Proxy Logging

For comprehensive audit trails without storing sensitive data on endpoints, route all LLM API traffic through a corporate proxy that logs:

- Timestamp
- Developer identity (from auth header or IP)
- Model used
- Token counts (input/output)
- Request/response bodies (encrypted at rest)

Proxies like LiteLLM, OpenAI-compatible proxies, or AWS Bedrock can be configured as pass-through gateways.

### Compliance Reporting

For SOC 2 / ISO 27001 compliance, document:

1. Which models developers are authorized to use
2. How API keys are managed and rotated
3. What data classification is permitted to be sent to AI APIs
4. How AI-generated code is reviewed before production deployment
5. Whether AI contributions are tracked in git history (`attribute-author: true`)

---

## 7. Acceptable Use Policy Template

Include in your AI tools acceptable use policy:

```
Aider Usage Policy

1. API Keys: Store AI provider API keys in the organization's secrets manager.
   Never commit API keys to source control.

2. Code Classification: Do not send code classified as Confidential or higher
   to external AI providers without written approval from Security.

3. Review: All AI-generated changes must be reviewed by a human before committing.
   The 'yes: true' setting is prohibited.

4. Commits: Do not enable auto-commits. Review all diffs before staging.

5. History Files: Ensure .aider.chat.history.md and related files are in .gitignore.
   Do not share history files externally.

6. Vulnerabilities: Review AI-generated code for security vulnerabilities.
   Do not assume AI output is secure. Run SAST tools on all AI-generated code.
```

---

## 8. Incident Response

If an API key is committed to git or a history file contains sensitive code:

1. **Rotate the API key immediately** — The key must be considered compromised.
2. **Remove the key from git history** using `git filter-repo` (not `git filter-branch`).
3. **Force-push the cleaned history** after coordinating with all contributors.
4. **Notify Security** per your organization's incident response procedure.
5. **Review access logs** for the compromised key to identify unauthorized usage.
6. **Update pre-commit hooks** to prevent recurrence.
