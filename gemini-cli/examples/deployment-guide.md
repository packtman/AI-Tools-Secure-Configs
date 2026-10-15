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
  "security": {
    "disableYoloMode": true,
    "disableAlwaysAllow": true,
    "environmentVariableRedaction": {
      "enabled": true,
      "allowed": []
    }
  },
  "hooksConfig": {
    "enabled": true
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

# Deploy the matching tier policy. Moderate is shown.
sudo install -d -o root -g root -m 0755 /etc/gemini-cli/policies
sudo install -o root -g root -m 0644 admin-policy-moderate.toml \
  /etc/gemini-cli/policies/enterprise.toml
```

### System Defaults (Base Layer)

```bash
sudo tee /etc/gemini-cli/system-defaults.json > /dev/null << 'EOF'
{
  "tools": {
    "sandbox": "docker"
  },
  "security": {
    "disableYoloMode": true,
    "environmentVariableRedaction": {
      "enabled": true,
      "allowed": []
    }
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

    - name: Create protected admin policy directory
      file:
        path: /etc/gemini-cli/policies
        state: directory
        mode: '0755'
        owner: root
        group: root

    - name: Deploy moderate admin policy
      copy:
        src: files/admin-policy-moderate.toml
        dest: /etc/gemini-cli/policies/enterprise.toml
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

sudo install -d -o root -g wheel -m 0755 \
  "/Library/Application Support/GeminiCli/policies"
sudo install -o root -g wheel -m 0644 admin-policy-moderate.toml \
  "/Library/Application Support/GeminiCli/policies/enterprise.toml"
```

### MDM Deployment (Jamf Pro)

1. Package the settings file into a `.pkg` installer
2. Set install location to `/Library/Application Support/GeminiCli/settings.json`
3. Deploy via Jamf Pro policy to appropriate device groups

### Seatbelt Sandbox Enforcement

For additional macOS isolation, set the environment variable system-wide:

```bash
# Add to /etc/profile.d/gemini-cli.sh or deploy via MDM
export SEATBELT_PROFILE=strict-proxied
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
  "security": {
    "disableYoloMode": true,
    "disableAlwaysAllow": true,
    "environmentVariableRedaction": {
      "enabled": true,
      "allowed": []
    }
  },
  "hooksConfig": {
    "enabled": true
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

# Deploy the matching tier policy in the protected ProgramData directory.
$policyDir = Join-Path $settingsDir "policies"
New-Item -ItemType Directory -Path $policyDir -Force | Out-Null
Copy-Item ".\admin-policy-moderate.toml" (Join-Path $policyDir "enterprise.toml") -Force
$policyAcl = Get-Acl $policyDir
$policyAcl.SetAccessRuleProtection($true, $false)
$policyAcl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\SYSTEM", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")))
$policyAcl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Administrators", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")))
$policyAcl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Users", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")))
Set-Acl -Path $policyDir -AclObject $policyAcl
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

# Confirm the installed version before rollout
gemini --version

# Request a blocked command and confirm the enterprise policy message appears
gemini -p "run sudo id" --output-format json
```

Confirm that Strict and Moderate endpoints reject `gemini --yolo`. On endpoints where hooks are enabled, open `/hooks panel` and verify only expected hooks appear. Ship Gemini CLI telemetry from the configured OTLP collector to the SIEM (Security Information and Event Management, a central security log system). Alert on repeated denied tool calls, attempted YOLO use, unexpected MCP server names, and admin policy ownership warnings.

### Troubleshooting

| Issue | Resolution |
|-------|-----------|
| Settings not applied | Verify file exists at correct system path |
| Permission denied on file | Ensure file is readable by all users (644) |
| User overriding settings | System overrides file has highest precedence — check it's at the system path, not user path |
| MCP servers appearing from user config | Ensure `mcp.allowed` is set in system overrides |
| Docker sandbox failing | Verify Docker is installed and user has docker group membership |
| Admin policy ignored | Verify the standard policy directory is root or administrator owned and not writable by standard users |

---

## Rollout Plan

### Pre-Rollout Checklist

- [ ] Verify the settings and admin policy paths on each managed OS.
- [ ] Confirm the MDM (Mobile Device Management, software that pushes files and settings to endpoints) package preserves root or administrator ownership.
- [ ] Store API credentials in the organization secrets manager, never in Gemini settings, policy TOML, or hook files.
- [ ] Test metadata-only telemetry ingest from the OTLP collector into the SIEM.
- [ ] Document the previous settings and policy package versions and test rollback on one endpoint.
- [ ] Inventory builds, tests, hooks, MCP servers, and shell commands used by the pilot group.

### Phase 1: Pilot

Deploy system defaults, environment-variable redaction, and the matching admin policy to a small volunteer group. Keep hooks enabled except in Strict.

Exit criteria:

- Every endpoint loads the protected admin policy without an ownership warning.
- Approved builds and tests complete with no unexplained denial.
- Denied commands and MCP calls arrive in the SIEM without prompt contents or secret values.
- The help desk can complete the rollback procedure below.

### Phase 2: Expanded Pilot

Deploy system overrides, the tier tool allowlist, MCP restrictions, and YOLO-mode disablement to representative teams on each OS.

Exit criteria:

- At least one full development cycle completes on every operating system in scope.
- All required MCP servers and hooks have named owners and security review records.
- False-positive denials have a documented safe alternative or approved exception.
- No endpoint can enter YOLO mode or modify the protected admin policy as a standard user.

### Phase 3: Organization-Wide

Deploy the versioned MDM package to production device groups. Monitor denials, policy-load failures, and exception volume.

Exit criteria:

- Target endpoints report the approved Gemini CLI, settings, and policy versions.
- SIEM alerts and help-desk routing are active.
- The exception owner and next review date are recorded for every deviation.

## What Will Break

| Blocked or changed workflow | Affected tier | Safe equivalent |
|-----------------------------|---------------|-----------------|
| `--yolo` and no-confirmation execution | All managed tiers | Use normal mode and approve each sensitive tool call. |
| Permanent "always allow" approvals | Moderate, Strict | Add a narrowly scoped, reviewed admin policy rule when repeated approval is justified. |
| Shell, file writes, and MCP tools | Strict | Use read-only analysis, then have an authorized developer apply the reviewed change. |
| `sudo`, broad root deletion, disk formatting, or world-writable permissions | Baseline, Moderate | Run a reviewed manual change through the privileged operations process. |
| Project or extension hooks | Strict | Use CI validation or an IT-deployed hook after security review. |
| Hooks requiring redacted environment variables | All tiers | Add only the required variable name to `security.environmentVariableRedaction.allowed`, with an exception owner and expiry. |

Developer message:

> Gemini CLI policy is changing on DATE. YOLO mode and destructive shell commands will be blocked. Strict users will also lose shell, file-write, MCP, and hook execution. Use normal approval mode, CI for privileged changes, and the approved MCP catalog. Report a blocked business workflow through SUPPORT_CHANNEL with the command or tool name, business purpose, repository, and requested expiry. Do not include secrets or prompt contents.

## Rollback Procedure

1. In Jamf, Intune, Workspace ONE, Ansible, or GPO, assign the previous signed settings and admin-policy package.
2. Restore the previous OS settings file and `policies/enterprise.toml` from the versioned package. Do not delete the protected policy directory.
3. Restart Gemini CLI and verify the previous tool behavior with `gemini --debug`.
4. Confirm the SIEM receives the rollback event and the endpoint reports the expected package version.
5. Send: "Gemini CLI policy was rolled back to VERSION at TIME while IT investigates ISSUE. Existing approval prompts and data-handling rules remain in effect. Next update: TIME."

Emergency rollback may remove only the newly introduced keys `security.disableYoloMode`, `security.disableAlwaysAllow`, `security.environmentVariableRedaction`, and `hooksConfig.enabled`, plus restore the prior `enterprise.toml`. Do not remove sandbox, authentication, telemetry privacy, or MCP controls unless the incident commander explicitly authorizes that broader rollback.

## Exception Handling

Settings most likely to cause friction are `security.disableAlwaysAllow`, Strict hook disablement, and the Moderate shell-prefix deny list. Require the requester to provide the exact tool or command, business reason, repository scope, data classification, owner, and expiry. Prefer a narrow TOML rule at a lower risk tier or a separate managed device group. Never grant an exception by making the admin policy directory user-writable.
