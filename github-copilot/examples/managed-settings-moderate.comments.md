# GitHub Copilot Moderate Managed Settings Rationale

This document accompanies `managed-settings-moderate.json`. Replace all uppercase placeholders
before deploying the JSON file as `managed-settings.json`.

| Key | What it does | Why Moderate uses this value | What breaks if removed or wrong |
|-----|--------------|------------------------------|---------------------------------|
| `permissions.disableBypassPermissionsMode` | Disables Copilot CLI and VS Code bypass, YOLO, and global auto-approve modes. | Agent workflows remain available, but normal approval boundaries stay active. | Removing it lets users grant broad command, file, and URL access without prompts. Individual allow-all flags are not blocked by this key. |
| `strictKnownMarketplaces` | Limits plugin installation to the listed enterprise marketplace. | A pinned, reviewed source reduces plugin supply-chain risk. | An invalid repository or ref blocks approved plugins. A moving or broad source weakens review. |
| `telemetry.enabled` | Enables OpenTelemetry export. | SIEM visibility is required for enterprise rollout. | A disabled exporter creates an audit gap. |
| `telemetry.endpoint` | Selects the approved OpenTelemetry collector. | Copilot usage metadata must go to an organization-controlled collector. | The example URL is not a production collector and must be replaced. A wrong URL loses events. |
| `telemetry.protocol` | Sends OTLP using HTTP with protobuf encoding. | Protobuf reduces event size and is broadly supported by collectors. | A collector that does not support this protocol rejects events. |
| `telemetry.captureContent` | Excludes prompt and response content from exported events. | Metadata is sufficient for monitoring and avoids copying source code or secrets into the SIEM. | Setting this to `true` can export sensitive content. |
| `telemetry.lockCaptureContent` | Prevents users from enabling content capture. | The privacy boundary must not depend on a user preference. | Setting this to `false` lets users enable sensitive-content export. |
| `telemetry.serviceName` | Labels events as GitHub Copilot telemetry. | A stable name supports routing and dashboards. | A conflicting name can mix Copilot events with another service. |
| `telemetry.resourceAttributes` | Tags events as enterprise deployment data. | The tag supports environment-specific retention and alerting. | Wrong tags can apply the wrong SIEM routing or retention policy. |

Do not commit exporter authentication headers. GitHub does not expand environment variables in
this file. Add headers only through an approved MDM or secrets-delivery process, or use mutual TLS.
