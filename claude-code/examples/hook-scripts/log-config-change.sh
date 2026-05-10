#!/usr/bin/env bash
# log-config-change.sh — ConfigChange hook
# Logs configuration changes for audit trail and tampering detection.
set -euo pipefail

INPUT=$(cat)

LOG_DIR="${CLAUDE_AUDIT_LOG_DIR:-/var/log/claude-code}"
LOG_FILE="${LOG_DIR}/config-audit.jsonl"

mkdir -p "$LOG_DIR" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
USER_NAME="${USER:-unknown}"

echo "$INPUT" | jq \
  --arg ts "$TIMESTAMP" \
  --arg user "$USER_NAME" \
  '{timestamp: $ts, user: $user, event: "config_change", details: .}' \
  >> "$LOG_FILE" 2>/dev/null || true

exit 0
