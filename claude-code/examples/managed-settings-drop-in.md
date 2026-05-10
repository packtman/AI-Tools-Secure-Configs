# Claude Code — Drop-in Settings Directory

## Overview

Claude Code supports a `managed-settings.d/` directory alongside `managed-settings.json`. This lets separate teams deploy independent policy fragments without coordinating edits to a single file.

## How It Works

| OS | Base path |
|----|-----------|
| macOS | `/Library/Application Support/ClaudeCode/` |
| Linux / WSL | `/etc/claude-code/` |
| Windows | `C:\Program Files\ClaudeCode\` |

1. `managed-settings.json` is merged first as the base.
2. All `*.json` files in `managed-settings.d/` are sorted alphabetically and merged on top.
3. **Scalars** — later files override earlier ones.
4. **Arrays** — concatenated and de-duplicated.
5. **Objects** — deep-merged.
6. Hidden files (`.*.json`) are ignored.

## Naming Convention

Use numeric prefixes to control merge order:

```
managed-settings.json              ← base policy
managed-settings.d/
├── 10-identity.json               ← identity & login restrictions
├── 20-permissions.json            ← permission deny rules
├── 30-sandbox.json                ← sandbox configuration
├── 40-hooks.json                  ← audit hooks
├── 50-mcp.json                    ← MCP server restrictions
└── 60-telemetry.json              ← telemetry & environment
```

## Example Files

### `10-identity.json`

```json
{
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": "YOUR_ORG_UUID",
  "minimumVersion": "2.1.38",
  "autoUpdatesChannel": "stable"
}
```

### `20-permissions.json`

```json
{
  "permissions": {
    "deny": [
      "Bash(curl * | bash)",
      "Bash(sudo *)",
      "Bash(eval *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "disableAutoMode": "disable",
  "allowManagedPermissionRulesOnly": false
}
```

### `30-sandbox.json`

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/.ssh", "~/.aws", "~/.gnupg"],
      "denyWrite": ["~/", "//etc/"]
    }
  }
}
```

### `40-hooks.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "https://hooks.corp.example.com/claude-code/audit",
            "timeout": 5,
            "headers": { "Authorization": "Bearer $AUDIT_TOKEN" },
            "allowedEnvVars": ["AUDIT_TOKEN"]
          }
        ]
      }
    ]
  },
  "allowedHttpHookUrls": ["https://hooks.corp.example.com/*"],
  "httpHookAllowedEnvVars": ["AUDIT_TOKEN"]
}
```

### `50-mcp.json`

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "internal-tools" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" },
    { "serverName": "shell" }
  ],
  "allowManagedMcpServersOnly": false
}
```

### `60-telemetry.json`

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.corp.example.com:4318"
  }
}
```

## Benefits

- **Team ownership** — Security team owns `20-permissions.json`, platform team owns `30-sandbox.json`.
- **Incremental deployment** — Add or update policy fragments without touching the base file.
- **Audit trail** — Each file can be version-controlled and deployed independently.
- **Conflict avoidance** — No need to coordinate merges to a single monolithic JSON file.
