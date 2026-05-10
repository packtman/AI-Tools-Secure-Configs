# Windsurf — Cascade Hooks for Security

## Overview

Cascade Hooks allow enterprise teams to execute custom shell commands at key workflow points. Pre-hooks can **block** actions, making them ideal for enforcing security policies.

## Hook Types

| Type | Timing | Can block? | Use case |
|------|--------|------------|----------|
| Pre-hook | Before action | Yes (exit code 2 = block) | Validation, policy enforcement |
| Post-hook | After action | No | Logging, audit trail, notifications |

## Security Hook Examples

### Pre-hook: Block secrets in generated code

```bash
#!/bin/bash
# pre-hook-scan-secrets.sh
# Scans staged content for potential secrets before committing.

PATTERNS=(
  'AKIA[0-9A-Z]{16}'           # AWS Access Key
  'sk-[a-zA-Z0-9]{48}'         # OpenAI API Key
  'sk-ant-[a-zA-Z0-9-]+'       # Anthropic API Key
  'ghp_[a-zA-Z0-9]{36}'        # GitHub PAT
  'password\s*=\s*["\x27][^"\x27]+'  # Hardcoded passwords
)

for pattern in "${PATTERNS[@]}"; do
  if echo "$CONTENT" | grep -qP "$pattern"; then
    echo "BLOCKED: Potential secret detected matching pattern: $pattern"
    exit 2
  fi
done

exit 0
```

### Post-hook: Audit logging

```bash
#!/bin/bash
# post-hook-audit-log.sh
# Logs Cascade actions to a central audit log.

LOG_FILE="/var/log/windsurf/cascade-audit.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "${TIMESTAMP} | user=${USER} | action=${HOOK_ACTION} | workspace=${WORKSPACE_PATH}" >> "$LOG_FILE"
```

### Pre-hook: Restrict file modifications

```bash
#!/bin/bash
# pre-hook-restrict-paths.sh
# Blocks modifications to sensitive paths.

RESTRICTED_PATHS=(
  ".env"
  ".env.*"
  "secrets/"
  "*.pem"
  "*.key"
  ".ssh/"
  ".aws/"
)

for rpath in "${RESTRICTED_PATHS[@]}"; do
  if echo "$TARGET_FILE" | grep -q "$rpath"; then
    echo "BLOCKED: Modification to restricted path: $TARGET_FILE"
    exit 2
  fi
done

exit 0
```

## Deployment

1. Create hook scripts and place in a central, read-only directory.
2. Configure hooks in Windsurf enterprise settings.
3. Test hooks in a staging environment before production deployment.
4. Monitor hook execution logs for blocked actions.
