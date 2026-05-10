#!/usr/bin/env bash
# session-summary-audit.sh — Stop hook
# Logs a session-end summary to the audit log.
set -euo pipefail

INPUT=$(cat)

LOG_DIR="${CLAUDE_AUDIT_LOG_DIR:-/var/log/claude-code}"
LOG_FILE="${LOG_DIR}/session-audit.jsonl"

mkdir -p "$LOG_DIR" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
USER_NAME="${USER:-unknown}"

jq -n \
  --arg ts "$TIMESTAMP" \
  --arg sid "$SESSION_ID" \
  --arg user "$USER_NAME" \
  --arg event "session_end" \
  '{timestamp: $ts, session_id: $sid, user: $user, event: $event}' \
  >> "$LOG_FILE" 2>/dev/null || true

exit 0
