# Gemini CLI — Enterprise Policy Deployment Guide

## Overview

Gemini CLI supports enterprise-managed policies through **system-level settings files** that override user and project configurations. The system overrides file has the highest precedence and cannot be overridden by users.

> **Note on Security:** These configurations are designed to prevent accidental misuse and enforce corporate policy in a managed environment. A determined user with local administrative rights may still circumvent these configurations. These are policy controls, not security boundaries.

---

## Architecture: System Settings Files

Gemini CLI reads settings from four levels (merged in precedence order):

| Level | File | Precedence | Purpose |
|-------|------|------------|---------|
| System Defaults | `system-defaults.json` | Lowest | Base defaults for all users |
| User Settings | `~/.gemini/settings.json` | Low | Per-user preferences |
| Project Settings | `.gemini/settings.json` | Medium | Project-specific overrides |
| System Overrides | `settings.json` (system path) | **Highest** | Admin-enforced policies |

For single-value settings, **system overrides win**. For arrays/objects (`mcpServers`, `includeDirectories`), values are **merged** across all levels.

---

## File Locations

### System Overrides (Admin-Enforced)

| OS | Path | Env Override |
|----|------|-------------|
| Linux | `/etc/gemini-cli/settings.json` | `GEMINI_CLI_SYSTEM_SETTINGS_PATH` |
| macOS | `/Library/Application Support/GeminiCli/settings.json` | `GEMINI_CLI_SYSTEM_SETTINGS_PATH` |
| Windows | `C:\ProgramData\gemini-cli\settings.json` | `GEMINI_CLI_SYSTEM_SETTINGS_PATH` |

### System Defaults

| OS | Path | Env Override |
|----|------|-------------|
| Linux | `/etc/gemini-cli/system-defaults.json` | `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` |
| macOS | `/Library/Application Support/GeminiCli/system-defaults.json` | `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` |
| Windows | `C:\ProgramData\gemini-cli\system-defaults.json` | `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` |

---

## Deployment: Linux

```bash
# Create system overrides directory
sudo mkdir -p /etc/gemini-cli

# Deploy system overrides (admin-enforced)
sudo tee /etc/gemini-cli/settings.json > /dev/null << 'EOF'
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)"]
  },
  "mcp": {
    "allowed": ["corp-tools"]
  },
  "mcpServers": {
    "corp-tools": {
      "command": "/usr/local/bin/corp-mcp-server",
      "timeout": 5000
    }
  },
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": false
  },
  "privacy": {
    "usageStatisticsEnabled": false
  }
}
EOF

# Protect the file
sudo chmod 644 /etc/gemini-cli/settings.json
sudo chown root:root /etc/gemini-cli/settings.json
```

---

## Deployment: macOS

```bash
# Create system overrides directory
sudo mkdir -p "/Library/Application Support/GeminiCli"

# Deploy system overrides
sudo tee "/Library/Application Support/GeminiCli/settings.json" > /dev/null << 'EOF'
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)"]
  },
  "mcp": {
    "allowed": ["corp-tools"]
  },
  "mcpServers": {
    "corp-tools": {
      "command": "/usr/local/bin/corp-mcp-server",
      "timeout": 5000
    }
  },
  "security": {
    "auth": {
      "enforcedType": "oauth-personal"
    }
  },
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": false
  },
  "privacy": {
    "usageStatisticsEnabled": false
  }
}
EOF

# Protect the file
sudo chmod 644 "/Library/Application Support/GeminiCli/settings.json"
sudo chown root:wheel "/Library/Application Support/GeminiCli/settings.json"
```

### macOS Seatbelt Sandbox Profile

For additional macOS isolation, set the `SEATBELT_PROFILE` environment variable:

```bash
export SEATBELT_PROFILE=strict
```

Or deploy a custom `.sb` profile in project `.gemini/` directories.

---

## Deployment: Windows

```powershell
# Create system overrides directory
$settingsDir = "C:\ProgramData\gemini-cli"
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force
}

# Deploy system overrides
$settings = @"
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)"]
  },
  "mcp": {
    "allowed": ["corp-tools"]
  },
  "mcpServers": {
    "corp-tools": {
      "command": "C:\\Program Files\\corp-tools\\mcp-server.exe",
      "timeout": 5000
    }
  },
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": false
  },
  "privacy": {
    "usageStatisticsEnabled": false
  }
}
"@

Set-Content -Path "$settingsDir\settings.json" -Value $settings -Encoding UTF8

# Restrict permissions
$acl = Get-Acl "$settingsDir\settings.json"
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\SYSTEM", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Administrators", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Users", "Read", "Allow")))
Set-Acl -Path "$settingsDir\settings.json" -AclObject $acl
```

---

## Authentication Enforcement

Force all users to authenticate with a specific method:

```json
{
  "security": {
    "auth": {
      "enforcedType": "oauth-personal"
    }
  }
}
```

If a user has a different authentication method configured, they will be prompted to switch. In non-interactive mode, the CLI exits with an error.

Available auth types:
- `oauth-personal` — Google login (recommended for enterprise)
- `api-key` — API key authentication
- `service-account` — Service account credentials (CI/CD)

---

## MCP Server Governance

### Secure Pattern: Define + Allowlist

The most secure MCP configuration requires both steps:

1. **Define** approved servers in the system overrides `mcpServers` object
2. **Allowlist** those server names in `mcp.allowed`

```json
{
  "mcp": {
    "allowed": ["corp-data-api", "source-code-analyzer"]
  },
  "mcpServers": {
    "corp-data-api": {
      "command": "/usr/local/bin/start-corp-api.sh",
      "timeout": 5000,
      "includeTools": ["search", "query"]
    },
    "source-code-analyzer": {
      "command": "/usr/local/bin/start-analyzer.sh",
      "includeTools": ["analyze", "lint"]
    }
  }
}
```

This prevents users from adding unauthorized MCP servers, and restricts each server to only approved tools.

### Disabling All MCP Servers

```json
{
  "mcp": {
    "allowed": []
  },
  "mcpServers": {}
}
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Deploy system overrides with `tools.core` allowlist (read-only tools only)
2. Set `tools.sandbox = "docker"` for container isolation
3. Set `mcp.allowed = []` to disable all MCP servers
4. Set `security.auth.enforcedType` to require corporate auth
5. Set `telemetry.logPrompts = false` 
6. Disable auto-updates if IT must approve versions
7. Use `SEATBELT_PROFILE=strict` on macOS for additional isolation

### For Development Environments

1. Allow write tools in `tools.core` but restrict dangerous shell commands
2. Enforce Docker sandbox for all tool execution
3. Define an MCP server allowlist with only audited servers
4. Enable telemetry for audit purposes (without prompt logging)
5. Allow Google login authentication only
6. Deploy project-level `.geminiignore` to protect sensitive file patterns
