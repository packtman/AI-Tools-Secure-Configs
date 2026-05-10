# Claude Code — Server-Managed Settings Guide

## Overview

Server-managed settings allow administrators to centrally configure Claude Code through the **Claude.ai Admin Console** without requiring MDM or device management infrastructure. Settings are delivered from Anthropic's servers when users authenticate.

**Requirements:**
- Claude for Teams or Claude for Enterprise plan
- Claude Code ≥ 2.1.38 (Teams) or ≥ 2.1.30 (Enterprise)
- Network access to `api.anthropic.com`

---

## How to Configure

1. Navigate to **Claude.ai → Admin Settings → Claude Code → Managed settings**.
2. Enter your JSON configuration (same format as `managed-settings.json`).
3. Save. Clients receive settings on next startup or hourly poll.

### Who can manage

- Primary Owner
- Owner

Restrict access to trusted administrators — changes apply to **all users** in the organization.

---

## Server-Managed vs. Endpoint-Managed

| Approach | Best for | Security model |
|----------|----------|---------------|
| Server-managed | No MDM, unmanaged devices | Delivered from Anthropic's servers at auth time |
| Endpoint-managed (MDM) | Managed devices with MDM | Deployed via OS policies, protected by OS from user tampering |

If both are configured, **server-managed settings win**. Sources do not merge — if server-managed delivers any keys, endpoint-managed is ignored entirely.

---

## Recommended Configuration

### Minimal security baseline

```json
{
  "permissions": {
    "deny": [
      "Bash(curl * | bash)",
      "Bash(curl * | sh)",
      "Bash(wget * | bash)",
      "Bash(wget * | sh)",
      "Bash(rm -rf /)",
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
  "forceLoginOrgUUID": "YOUR_ORG_UUID"
}
```

### With hooks for audit logging

```json
{
  "permissions": {
    "deny": [
      "Bash(curl * | bash)",
      "Bash(sudo *)",
      "Bash(eval *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "https://hooks.corp.example.com/claude-code/audit",
            "timeout": 5,
            "headers": {
              "Authorization": "Bearer $AUDIT_HOOK_TOKEN"
            },
            "allowedEnvVars": ["AUDIT_HOOK_TOKEN"]
          }
        ]
      }
    ]
  },
  "allowedHttpHookUrls": ["https://hooks.corp.example.com/*"],
  "httpHookAllowedEnvVars": ["AUDIT_HOOK_TOKEN"]
}
```

### With auto mode configuration

```json
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts",
      "Trusted internal domains: *.corp.example.com"
    ],
    "hard_deny": [
      "Never run terraform destroy",
      "Never run kubectl delete namespace",
      "Never push to main or master branches"
    ]
  }
}
```

---

## Fail-Closed Enforcement

By default, if the settings fetch fails at startup, Claude Code continues without managed settings. For maximum security:

```json
{
  "forceRemoteSettingsRefresh": true
}
```

When enabled:
- CLI blocks at startup until settings are fetched.
- If the fetch fails, CLI **exits** instead of proceeding.
- The setting self-perpetuates via local cache.

**WARNING:** Ensure `api.anthropic.com` is reachable from all developer machines before enabling.

---

## Security Considerations

| Scenario | Behavior |
|----------|----------|
| User edits cached settings file | Tampered settings apply until next fetch restores correct version |
| User deletes cache | First-launch behavior: brief unenforced window |
| API unavailable | Cached settings apply if available; without cache, settings not enforced |
| User authenticates with wrong org | Settings not delivered |
| Third-party model provider | Server-managed settings bypassed entirely |

For stronger enforcement, use **endpoint-managed settings** on MDM-enrolled devices.

---

## Verification

Ask a user to run:
- `/permissions` — View effective permission rules and their source.
- `/status` — See which managed settings source is active.
- Restart Claude Code — Triggers security approval dialog if hooks/env vars are present.

---

## Limitations

- Settings apply uniformly to all users (no per-group support yet).
- MCP server configurations cannot be distributed via server-managed settings.
- `policyHelper` and `wslInheritsWindowsSettings` are not honored (use MDM).
- Not available with Bedrock, Vertex, Foundry, or custom `ANTHROPIC_BASE_URL`.
