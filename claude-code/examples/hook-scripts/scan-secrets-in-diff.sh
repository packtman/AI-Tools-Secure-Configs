#!/usr/bin/env bash
# scan-secrets-in-diff.sh — PostToolUse hook for Write|Edit|MultiEdit
# Scans recently written/edited file for common secret patterns.
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

SECRET_PATTERNS=(
  'AKIA[0-9A-Z]{16}'                          # AWS Access Key ID
  'sk-[a-zA-Z0-9]{20,}'                       # OpenAI / generic API key
  'sk-ant-[a-zA-Z0-9-]+'                      # Anthropic API key
  'ghp_[a-zA-Z0-9]{36}'                       # GitHub PAT (classic)
  'github_pat_[a-zA-Z0-9_]+'                  # GitHub PAT (fine-grained)
  'gho_[a-zA-Z0-9]{36}'                       # GitHub OAuth token
  'glpat-[a-zA-Z0-9_-]{20}'                   # GitLab PAT
  'xox[bpors]-[a-zA-Z0-9-]+'                  # Slack token
  'ya29\.[a-zA-Z0-9_-]+'                      # Google OAuth token
  'AIza[a-zA-Z0-9_-]{35}'                     # Google API key
  'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}' # SendGrid API key
  'sq0atp-[a-zA-Z0-9_-]{22}'                  # Square access token
  'sk_live_[a-zA-Z0-9]{24,}'                  # Stripe live secret key
  'rk_live_[a-zA-Z0-9]{24,}'                  # Stripe restricted key
  'pk_live_[a-zA-Z0-9]{24,}'                  # Stripe publishable key
)

FOUND_SECRETS=()
for pattern in "${SECRET_PATTERNS[@]}"; do
  if grep -qE "$pattern" "$FILE_PATH" 2>/dev/null; then
    FOUND_SECRETS+=("$pattern")
  fi
done

if [ ${#FOUND_SECRETS[@]} -gt 0 ]; then
  PATTERNS_LIST=$(printf '%s, ' "${FOUND_SECRETS[@]}")
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      outputToModel: ("WARNING: Potential secret(s) detected in " + $file + ". Matching patterns: " + $patterns + ". Please remove any secrets and use environment variables instead.")
    }
  }' --arg file "$FILE_PATH" --arg patterns "${PATTERNS_LIST%, }"
else
  exit 0
fi
