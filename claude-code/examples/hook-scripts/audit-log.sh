#!/usr/bin/env bash
# audit-log.sh — PostToolUse async hook for Bash commands
# Logs all Bash tool executions to a central audit log.
set -euo pipefail

INPUT=$(cat)
LOG_DIR="${CLAUDE_AUDIT_LOG_DIR:-/var/log/claude-code}"
LOG_FILE="$LOG_DIR/audit.jsonl"

mkdir -p "$LOG_DIR" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // "n/a"')
CWD=$(echo "$INPUT" | jq -r '.cwd // "unknown"')

jq -n -c '{
  timestamp: $ts,
  session_id: $sid,
  tool: $tool,
  command: $cmd,
  cwd: $cwd,
  user: $user,
  hostname: $host
}' \
  --arg ts "$TIMESTAMP" \
  --arg sid "$SESSION_ID" \
  --arg tool "$TOOL_NAME" \
  --arg cmd "$COMMAND" \
  --arg cwd "$CWD" \
  --arg user "${USER:-unknown}" \
  --arg host "$(hostname)" >> "$LOG_FILE" 2>/dev/null || true
