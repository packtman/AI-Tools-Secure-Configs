# Codex Desktop App — macOS MDM Deployment Guide

## Overview

On macOS, administrators can push managed configuration for the Codex Desktop App via MDM solutions (Jamf Pro, Kandji, Fleet, Mosyle). Codex reads these values from macOS managed preferences on launch.

---

## Preference Domain

```
com.openai.codex
```

## Available Keys

| Key | Type | Description |
|-----|------|-------------|
| `config_toml_base64` | String | Base64-encoded managed defaults (TOML format) |
| `requirements_toml_base64` | String | Base64-encoded admin-enforced requirements (TOML format) |

---

## Deployment Steps

### Step 1: Create Requirements TOML

```toml
# /tmp/codex-requirements.toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[features]
browser_use = false
computer_use = false
```

### Step 2: Create Managed Defaults TOML

```toml
# /tmp/codex-managed-config.toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
cli_auth_credentials_store = "keyring"

[sandbox_workspace_write]
network_access = false
```

### Step 3: Encode Payloads

```bash
REQUIREMENTS_B64=$(base64 -i /tmp/codex-requirements.toml | tr -d '\n')
CONFIG_B64=$(base64 -i /tmp/codex-managed-config.toml | tr -d '\n')
```

### Step 4: Create MDM Profile

Use your MDM solution to create a configuration profile targeting `com.openai.codex`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>requirements_toml_base64</key>
  <string>PASTE_REQUIREMENTS_B64_HERE</string>
  <key>config_toml_base64</key>
  <string>PASTE_CONFIG_B64_HERE</string>
</dict>
</plist>
```

### Step 5: Deploy and Verify

1. Push the profile to target devices via your MDM solution
2. Ask users to restart Codex
3. Verify the startup config summary reflects managed values

```bash
# Verify managed preferences are applied
defaults read com.openai.codex

# Decode and inspect requirements
defaults read com.openai.codex requirements_toml_base64 | base64 -d
```

---

## Jamf Pro Configuration

1. Navigate to **Computers > Configuration Profiles > New**
2. Select **Application & Custom Settings > External Applications**
3. Set source to **Custom Schema**
4. Preference domain: `com.openai.codex`
5. Add string properties for `requirements_toml_base64` and `config_toml_base64`
6. Scope to appropriate device groups

---

## Kandji Configuration

1. Go to **Library > Custom Profiles**
2. Upload a `.mobileconfig` file containing the `com.openai.codex` payload
3. Assign to appropriate blueprints

---

## Updating Policies

When revoking or changing policy, update the managed payload in your MDM. Codex reads the refreshed preference the next time it launches.

**Best practices:**
- Avoid embedding secrets or high-churn dynamic values in the payload
- Treat the managed TOML like any other MDM setting under change control
- Test profile changes on a pilot group before broad deployment
- Keep a version history of your TOML payloads in source control
