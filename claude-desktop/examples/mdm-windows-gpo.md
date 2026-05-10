# Claude Desktop — Windows Group Policy / Intune Deployment

## Group Policy (Active Directory)

### Registry-based policy

1. Open **Group Policy Management Console** (gpmc.msc).
2. Create or edit a GPO linked to the target OU.
3. Navigate to **Computer Configuration → Preferences → Windows Settings → Registry**.
4. Add the following registry items:

| Action | Hive | Key path | Value name | Type | Data |
|--------|------|----------|------------|------|------|
| Create | HKLM | `SOFTWARE\Policies\Claude` | `isLocalDevMcpEnabled` | REG_DWORD | `0` |
| Create | HKLM | `SOFTWARE\Policies\Claude` | `isDesktopExtensionEnabled` | REG_DWORD | `0` |

5. Run `gpupdate /force` on target machines or wait for the next policy refresh.

## Microsoft Intune

### Option A: Configuration Profile (OMA-URI)

1. Navigate to **Devices → Configuration profiles → Create profile**.
2. Platform: **Windows 10 and later**.
3. Profile type: **Templates → Custom**.
4. Add OMA-URI settings:

| Name | OMA-URI | Data type | Value |
|------|---------|-----------|-------|
| Disable MCP | `./Device/Vendor/MSFT/Policy/Config/Anthropic~Policy~Claude/isLocalDevMcpEnabled` | Integer | `0` |
| Disable Extensions | `./Device/Vendor/MSFT/Policy/Config/Anthropic~Policy~Claude/isDesktopExtensionEnabled` | Integer | `0` |

5. Assign to the appropriate device group.

### Option B: PowerShell script deployment

Deploy the following script via Intune Scripts:

```powershell
$regPath = "HKLM:\SOFTWARE\Policies\Claude"

if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}

Set-ItemProperty -Path $regPath -Name "isLocalDevMcpEnabled" -Value 0 -Type DWord
Set-ItemProperty -Path $regPath -Name "isDesktopExtensionEnabled" -Value 0 -Type DWord

Write-Output "Claude Desktop enterprise policies applied successfully."
```

## Verification

```powershell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude"

# Expected output:
# isLocalDevMcpEnabled    : 0
# isDesktopExtensionEnabled : 0
```
