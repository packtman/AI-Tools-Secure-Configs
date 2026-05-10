#!/usr/bin/env bash
# block-destructive-rm.sh — PreToolUse hook for Bash(rm *)
# Blocks rm -rf targeting dangerous paths. Place in .claude/hooks/
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

DANGEROUS_PATTERNS=(
  'rm -rf /'
  'rm -rf /*'
  'rm -rf ~'
  'rm -rf ~/'
  'rm -rf $HOME'
  'rm -rf /etc'
  'rm -rf /usr'
  'rm -rf /var'
  'rm -rf /home'
  'rm -rf /root'
  'rm -rf .git'
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qF "$pattern"; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("Destructive rm command blocked by security hook: " + $pattern)
      }
    }' --arg pattern "$pattern"
    exit 0
  fi
done

exit 0
