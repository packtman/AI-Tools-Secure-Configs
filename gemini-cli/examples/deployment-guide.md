# Gemini CLI — Multi-Platform Deployment Guide

## Overview

This guide covers deploying Gemini CLI enterprise settings across Linux, macOS, and Windows environments. The system overrides file is the primary enforcement mechanism — it has the highest precedence and overrides all user and project settings.

---

## Linux Deployment

### System Overrides (Admin-Enforced)

```bash
sudo mkdir -p /etc/gemini-cli

sudo tee /etc/gemini-cli/settings.json > /dev/null << 'EOF'
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "WriteFileTool", "EditFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)", "ShellTool(ls)", "ShellTool(npm test)"]
  },
  "mcp": {
    "allowed": ["corp-tools"]
  },
  "mcpServers": {
    "corp-tools": {
      "command": "/usr/local/bin/corp-mcp-server",
      "timeout": 5000,
      "includeTools": ["search", "query"]
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

sudo chmod 644 /etc/gemini-cli/settings.json
sudo chown root:root /etc/gemini-cli/settings.json
```

### System Defaults (Base Layer)

```bash
sudo tee /etc/gemini-cli/system-defaults.json > /dev/null << 'EOF'
{
  "tools": {
    "sandbox": "docker"
  },
  "privacy": {
    "usageStatisticsEnabled": false
  },
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": false
  },
  "model": {
    "name": "gemini-2.5-pro"
  }
}
EOF

sudo chmod 644 /etc/gemini-cli/system-defaults.json
sudo chown root:root /etc/gemini-cli/system-defaults.json
```

### Configuration Management (Ansible)

```yaml
- name: Deploy Gemini CLI enterprise settings
  hosts: developer_workstations
  become: true
  tasks:
    - name: Create gemini-cli config directory
      file:
        path: /etc/gemini-cli
        state: directory
        mode: '0755'
        owner: root
        group: root

    - name: Deploy system overrides
      copy:
        src: files/gemini-cli-settings.json
        dest: /etc/gemini-cli/settings.json
        mode: '0644'
        owner: root
        group: root

    - name: Deploy system defaults
      copy:
        src: files/gemini-cli-system-defaults.json
        dest: /etc/gemini-cli/system-defaults.json
        mode: '0644'
        owner: root
        group: root
```

---

## macOS Deployment

### Manual Deployment

```bash
sudo mkdir -p "/Library/Application Support/GeminiCli"

sudo cp system-settings-enterprise.json \
  "/Library/Application Support/GeminiCli/settings.json"

sudo chmod 644 "/Library/Application Support/GeminiCli/settings.json"
sudo chown root:wheel "/Library/Application Support/GeminiCli/settings.json"
```

### MDM Deployment (Jamf Pro)

1. Package the settings file into a `.pkg` installer
2. Set install location to `/Library/Application Support/GeminiCli/settings.json`
3. Deploy via Jamf Pro policy to appropriate device groups

### Seatbelt Sandbox Enforcement

For additional macOS isolation, set the environment variable system-wide:

```bash
# Add to /etc/profile.d/gemini-cli.sh or deploy via MDM
export SEATBELT_PROFILE=strict
```

---

## Windows Deployment

### PowerShell Script (Intune / SCCM)

```powershell
$settingsDir = "C:\ProgramData\gemini-cli"
$settingsPath = Join-Path $settingsDir "settings.json"

# Create directory
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force
}

# Deploy settings
$settings = @'
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "WriteFileTool", "EditFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)", "ShellTool(dir)", "ShellTool(npm test)"]
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
'@

Set-Content -Path $settingsPath -Value $settings -Encoding UTF8

# Lock down permissions
$acl = Get-Acl $settingsPath
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\SYSTEM", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Administrators", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Users", "Read", "Allow")))
Set-Acl -Path $settingsPath -AclObject $acl
```

### Group Policy (GPO) via File Copy

1. Place `settings.json` on a network share
2. Create a GPO with Computer Configuration > Preferences > Windows Settings > Files
3. Source: `\\server\share\gemini-cli\settings.json`
4. Destination: `C:\ProgramData\gemini-cli\settings.json`
5. Action: Replace

---

## Verification

### All Platforms

```bash
# Start Gemini CLI and check applied settings
gemini --debug

# Verify which tools are available
gemini -p "list your available tools" --output-format json

# Check sandbox is active
gemini -p "echo test" --sandbox
```

### Troubleshooting

| Issue | Resolution |
|-------|-----------|
| Settings not applied | Verify file exists at correct system path |
| Permission denied on file | Ensure file is readable by all users (644) |
| User overriding settings | System overrides file has highest precedence — check it's at the system path, not user path |
| MCP servers appearing from user config | Ensure `mcp.allowed` is set in system overrides |
| Docker sandbox failing | Verify Docker is installed and user has docker group membership |

---

## Rollout Strategy

### Phase 1: Pilot (1-2 teams)
1. Deploy system defaults only (non-enforcing)
2. Monitor tool usage via telemetry
3. Identify required tools and MCP servers

### Phase 2: Soft Enforcement
1. Deploy system overrides with generous `tools.core` allowlist
2. Define initial MCP server allowlist
3. Collect feedback and adjust

### Phase 3: Full Enforcement
1. Restrict `tools.core` to approved set
2. Enforce Docker sandbox
3. Lock MCP servers to audited list
4. Enable telemetry to corporate OTLP collector
5. Enforce authentication type
