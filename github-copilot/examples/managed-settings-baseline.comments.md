# GitHub Copilot Baseline Managed Settings Rationale

This document accompanies `managed-settings-baseline.json`. Deploy the JSON file as
`managed-settings.json`.

| Key | What it does | Why Baseline uses this value | What breaks if removed or wrong |
|-----|--------------|------------------------------|---------------------------------|
| `permissions.disableBypassPermissionsMode` | Disables Copilot CLI and VS Code bypass, YOLO, and global auto-approve modes. | Even Baseline requires approval before broad command, file, or URL access. | Removing it lets users enable allow-all behavior. The control does not block individual allow-all flags, so endpoint monitoring is still required. |
