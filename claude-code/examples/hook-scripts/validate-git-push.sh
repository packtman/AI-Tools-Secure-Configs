#!/usr/bin/env bash
# validate-git-push.sh — PreToolUse hook for Bash(git push *)
# Blocks pushes to protected branches (main, master, production).
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

PROTECTED_BRANCHES=("main" "master" "production" "release")

for branch in "${PROTECTED_BRANCHES[@]}"; do
  if echo "$COMMAND" | grep -qE "git push.*\b${branch}\b"; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("Direct push to protected branch '\'''" + $branch + "'\'' is blocked by security policy. Use a pull request instead.")
      }
    }' --arg branch "$branch"
    exit 0
  fi
done

# Allow the push if no protected branch matched
exit 0
