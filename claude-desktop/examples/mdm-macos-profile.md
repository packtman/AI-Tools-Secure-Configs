# Claude Desktop — macOS MDM Configuration Profile

## Jamf Pro

1. Navigate to **Computers → Configuration Profiles → New**.
2. Select **Application & Custom Settings → External Applications**.
3. Set source to **Custom Schema**.
4. Enter preference domain: `com.anthropic.claudefordesktop`.
5. Upload or paste the following JSON schema:

```json
{
  "title": "Claude Desktop Enterprise Policy",
  "properties": {
    "isLocalDevMcpEnabled": {
      "type": "boolean",
      "default": false,
      "description": "Allow users to configure local MCP servers"
    },
    "isDesktopExtensionEnabled": {
      "type": "boolean",
      "default": false,
      "description": "Allow desktop extensions"
    }
  }
}
```

6. Set both values to `false` for maximum security.
7. Scope the profile to the appropriate computer groups.
8. Deploy.

## Kandji

1. Navigate to **Library → Custom Profiles**.
2. Create a new custom profile with the mobileconfig XML from `enterprise-policy.md`.
3. Assign to the appropriate Blueprint.

## Verification

Run on a managed Mac:

```bash
# Check managed preferences
defaults read com.anthropic.claudefordesktop isLocalDevMcpEnabled
# Expected output: 0

defaults read com.anthropic.claudefordesktop isDesktopExtensionEnabled
# Expected output: 0

# Verify profile is installed
profiles show -type configuration | grep -i claude
```
