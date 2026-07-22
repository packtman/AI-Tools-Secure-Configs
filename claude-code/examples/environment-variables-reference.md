# Claude Code — Security-Relevant Environment Variables

Set these in the `env` block of `managed-settings.json` or `settings.json` to enforce organization-wide behavior.

## Authentication & Identity

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `ANTHROPIC_API_KEY` | API key for direct authentication | Use secrets manager; never hard-code |
| `CLAUDE_CODE_USE_BEDROCK` | Route through AWS Bedrock | `1` if using Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Route through GCP Vertex AI | `1` if using Vertex |
| `ANTHROPIC_FOUNDRY_BASE_URL` | Foundry base URL | Your Foundry endpoint URL |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry resource name | Your Foundry resource |
| `ANTHROPIC_FOUNDRY_API_KEY` | Foundry API key | Use secrets manager |
| `ANTHROPIC_BASE_URL` | Custom API endpoint / LLM gateway | Your gateway URL |

## Telemetry & Privacy

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable/disable telemetry | `0` (disable) |
| `OTEL_METRICS_EXPORTER` | OpenTelemetry metrics exporter | `otlp` (if using your own collector) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | Your internal collector URL |
| `OTEL_EXPORTER_OTLP_HEADERS` | OTLP authentication headers | Auth token for collector |

## Memory & Session

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable auto memory writes | `1` for sensitive environments |
| `CLAUDE_CODE_SKIP_PROMPT_HISTORY` | Skip writing session transcripts to disk | `1` for sensitive environments |

## Behavior Controls

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `CLAUDE_CODE_DISABLE_THINKING` | Disable extended thinking | As needed |
| `CLAUDE_CODE_EFFORT_LEVEL` | Set effort level | `medium` or `high` |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | Suppress feedback surveys | `1` |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | Remove built-in git instructions | As needed |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable Bash, subagent, and MCP background tasks, auto-backgrounding, and Ctrl+B | `1` for Strict |
| `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` | Delay before a long MCP call moves to the background, requires Claude Code 2.1.212 or later | `0` for Moderate |
| `CLAUDE_AUTO_BACKGROUND_TASKS` | Force automatic backgrounding, including long MCP calls in non-interactive mode on 2.1.212 or later | Leave unset in managed tiers |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Strip Anthropic beta headers and beta tool fields for incompatible gateways | `1` only when your gateway requires it |
| `DISABLE_AUTOUPDATER` | Disable automatic updates | `1` if controlling updates centrally |

### Background task tier guidance

| Tier | Managed value | What changes |
|------|---------------|--------------|
| Baseline | Neither variable set | Uses the vendor default. On Claude Code 2.1.212 or later, MCP calls longer than two minutes move to the background. |
| Moderate | `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=0` | Long MCP calls stay visible. Developers can still intentionally background work with Ctrl+B. |
| Strict | `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | All automatic and explicit Bash, subagent, and MCP background task paths are disabled. |

Do not set `CLAUDE_AUTO_BACKGROUND_TASKS=1` in an organization policy. It force-enables automatic backgrounding and extends it to non-interactive runs, where a one-shot process can end before the result arrives.

`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` is a gateway compatibility switch, not a general security tier. It disables MCP tool search and loads every MCP tool up front. Add it only when an approved Bedrock, Vertex AI, or proxy gateway rejects Anthropic beta headers or beta tool fields.

## MCP & Tools

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `CLAUDE_CODE_MCP_ALLOWLIST_ENV` | Give stdio MCP servers only a safe baseline plus explicitly configured variables | `1` for all tiers |
| `MCP_TIMEOUT` | MCP server startup timeout (ms) | `10000` |
| `MAX_MCP_OUTPUT_TOKENS` | Max token output from MCP tools | `10000` (default) |
| `MCP_TOOL_TIMEOUT` | MCP tool execution timeout (ms) | `60000` |

## Sandbox

Sandbox is configured via `sandbox.enabled` in `managed-settings.json` or `settings.json`, not via environment variables.

## Network & Proxy

| Variable | Description | Secure value |
|----------|-------------|-------------|
| `HTTPS_PROXY` | HTTPS proxy for API calls | Your corporate proxy URL |
| `HTTP_PROXY` | HTTP proxy | Your corporate proxy URL |
| `NO_PROXY` | Proxy bypass list | `localhost,127.0.0.1` |
| `NODE_EXTRA_CA_CERTS` | Custom CA certificate bundle | Path to corporate CA bundle |

---

## Example: Enterprise env block in managed-settings.json

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1",
    "HTTPS_PROXY": "https://proxy.corp.example.com:8443",
    "NO_PROXY": "localhost,127.0.0.1,.corp.example.com",
    "NODE_EXTRA_CA_CERTS": "/etc/ssl/certs/corp-ca-bundle.crt",
    "MCP_TIMEOUT": "10000",
    "CLAUDE_CODE_MCP_ALLOWLIST_ENV": "1",
    "CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS": "0"
  }
}
```

## Example: High-security env block

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_SKIP_PROMPT_HISTORY": "1",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1",
    "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
    "CLAUDE_CODE_MCP_ALLOWLIST_ENV": "1",
    "DISABLE_AUTOUPDATER": "1"
  }
}
```
