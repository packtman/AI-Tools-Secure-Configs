# GitHub Copilot Strict Managed Settings Rationale

This document accompanies `managed-settings-strict.json`. Replace the collector URL before
deploying the JSON file as `managed-settings.json`.

| Key | What it does | Why Strict uses this value | What breaks if removed or wrong |
|-----|--------------|----------------------------|---------------------------------|
| `permissions.disableBypassPermissionsMode` | Disables Copilot CLI and VS Code bypass, YOLO, and global auto-approve modes. | Strict requires an approval boundary for every covered agent action. | Removing it lets users grant broad command, file, and URL access without prompts. Individual allow-all flags are not blocked by this key. |
| `strictKnownMarketplaces` | An empty array blocks installation from every plugin marketplace. | No plugin code is allowed until security approves and pins a source. | Existing marketplace plugins become unavailable. Removing the key permits unreviewed marketplaces. |
| `telemetry.enabled` | Enables OpenTelemetry export. | Centralized monitoring is required for regulated rollout. | A disabled exporter creates an audit gap. |
| `telemetry.endpoint` | Selects the approved OpenTelemetry collector. | Copilot usage metadata must go to an organization-controlled collector. | The example URL must be replaced. A wrong URL loses events. |
| `telemetry.protocol` | Sends OTLP using HTTP with protobuf encoding. | Protobuf reduces event size and is broadly supported by collectors. | A collector that does not support this protocol rejects events. |
| `telemetry.captureContent` | Excludes prompt and response content from exported events. | Metadata supports monitoring without copying regulated data to the SIEM. | Setting this to `true` can export code, prompts, or secrets. |
| `telemetry.lockCaptureContent` | Prevents users from enabling content capture. | Privacy controls must not depend on user preferences. | Setting this to `false` lets users weaken the content boundary. |
| `telemetry.serviceName` | Labels events as GitHub Copilot telemetry. | A stable name supports routing and dashboards. | A conflicting name can mix Copilot events with another service. |
| `telemetry.resourceAttributes` | Tags events as regulated deployment data. | The tag supports strict retention and alerting. | Wrong tags can apply the wrong SIEM controls. |

Do not commit exporter authentication headers. GitHub does not expand environment variables in
this file. Add headers only through an approved MDM or secrets-delivery process, or use mutual TLS.
