# Codex Desktop App — Windows Enterprise Deployment Guide

## Overview

On Windows, Codex Desktop App policies are enforced through system-level configuration files. Unlike macOS, Windows does not use registry-based managed preferences for Codex. Instead, deploy `requirements.toml` and `managed_config.toml` to protected system paths.

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| Requirements | `%ProgramData%\OpenAI\Codex\requirements.toml` | Admin-enforced constraints (cannot be overridden) |
| Managed Config | `%USERPROFILE%\.codex\managed_config.toml` | Managed defaults (reapplied on restart) |

---

## Deployment via Group Policy (GPO)

### Step 1: Create Policy Files

Create `requirements.toml`:

```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[features]
browser_use = false
computer_use = false
```

### Step 2: Deploy via GPO File Distribution

1. Place the file on a network share accessible by target machines
2. Create a GPO that copies the file to `C:\ProgramData\OpenAI\Codex\requirements.toml`
3. Use a startup script or Preferences > Files to deploy

### Step 3: Set File Permissions

Restrict the file so users cannot modify it:

```powershell
$path = "C:\ProgramData\OpenAI\Codex\requirements.toml"

# Remove inherited permissions
$acl = Get-Acl $path
$acl.SetAccessRuleProtection($true, $false)

# Grant access only to SYSTEM and Administrators
$systemRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\SYSTEM", "FullControl", "Allow")
$adminRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Administrators", "FullControl", "Allow")
$usersRead = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Users", "Read", "Allow")

$acl.AddAccessRule($systemRule)
$acl.AddAccessRule($adminRule)
$acl.AddAccessRule($usersRead)
Set-Acl -Path $path -AclObject $acl
```

---

## Deployment via Microsoft Intune

### Option 1: Win32 App Package

1. Package `requirements.toml` into an `.intunewin` file
2. Set install command: `copy requirements.toml "C:\ProgramData\OpenAI\Codex\requirements.toml"`
3. Set detection rule: file exists at `C:\ProgramData\OpenAI\Codex\requirements.toml`
4. Assign to appropriate device groups

### Option 2: PowerShell Script

Deploy via Intune > Devices > Scripts:

```powershell
$requirementsDir = "C:\ProgramData\OpenAI\Codex"
$requirementsPath = Join-Path $requirementsDir "requirements.toml"

# Create directory if needed
if (-not (Test-Path $requirementsDir)) {
    New-Item -ItemType Directory -Path $requirementsDir -Force
}

# Write requirements
$content = @"
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[features]
browser_use = false
computer_use = false
"@

Set-Content -Path $requirementsPath -Value $content -Encoding UTF8

# Lock down permissions
$acl = Get-Acl $requirementsPath
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\SYSTEM", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Administrators", "FullControl", "Allow")))
$acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\Users", "Read", "Allow")))
Set-Acl -Path $requirementsPath -AclObject $acl
```

---

## Windows Sandbox Mode

For Windows-native Codex usage, configure the sandbox mode in the `[windows]` table:

```toml
[windows]
sandbox = "elevated"   # Recommended — requires admin for setup
# sandbox = "unelevated" # Fallback if admin permissions unavailable
```

The `elevated` mode provides stronger isolation. Use `unelevated` only as a fallback.

---

## Verification

```powershell
# Check file exists and is readable
Get-Content "C:\ProgramData\OpenAI\Codex\requirements.toml"

# Verify file permissions
Get-Acl "C:\ProgramData\OpenAI\Codex\requirements.toml" | Format-List

# Check Codex applies the policy (look for startup config summary)
codex --version
```

---

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| Policy not applied | Ensure user restarted Codex after file deployment |
| File permission denied | Run deployment script as Administrator |
| Codex ignores requirements | Verify file path exactly matches `%ProgramData%\OpenAI\Codex\requirements.toml` |
| Conflict with cloud-managed policy | Cloud-managed requirements take precedence over system file |
