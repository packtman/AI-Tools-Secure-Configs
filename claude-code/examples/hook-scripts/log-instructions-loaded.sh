#!/usr/bin/env bash
# log-instructions-loaded.sh - InstructionsLoaded audit hook
# Records which instruction files entered context without logging their contents.
set -euo pipefail

umask 077

INPUT=$(cat)
LOG_DIR="${CLAUDE_AUDIT_LOG_DIR:-/var/log/claude-code}"
LOG_FILE="${LOG_DIR}/instructions-audit.jsonl"

mkdir -p "$LOG_DIR" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

jq -n -c \
  --arg timestamp "$TIMESTAMP" \
  --arg session_id "$(jq -r '.session_id // "unknown"' <<< "$INPUT")" \
  --arg cwd "$(jq -r '.cwd // "unknown"' <<< "$INPUT")" \
  --arg file_path "$(jq -r '.file_path // "unknown"' <<< "$INPUT")" \
  --arg memory_type "$(jq -r '.memory_type // "unknown"' <<< "$INPUT")" \
  --arg load_reason "$(jq -r '.load_reason // "unknown"' <<< "$INPUT")" \
  '{
    timestamp: $timestamp,
    event: "instructions_loaded",
    session_id: $session_id,
    cwd: $cwd,
    file_path: $file_path,
    memory_type: $memory_type,
    load_reason: $load_reason
  }' >> "$LOG_FILE" 2>/dev/null || true

exit 0
