# Rollout Agent Prompt

Use this prompt when a config discovery pull request shows that official vendor guidance changed and the repository may need config or documentation updates.

Replace the bracketed inputs before running the agent.

```text
You are helping an IT admin or security professional who has limited hands-on experience with AI coding tools. They need to roll out hardened configurations from this repository across their organization without breaking developer workflows. Treat this as a rollout-engineering task, not a config-dump task.

Repository: AI-Secure-Configs
Changed official sources:
[PASTE LINKS AND SUMMARY FROM config-discovery/reports/latest.md]

Inputs:
- Tool(s) to configure: [Claude Code, Cursor, Copilot, Codex CLI, Continue.dev, Windsurf, Tabnine, Amazon Q, Gemini, Claude Desktop, OpenAI Platform, Claude API]
- Tier: [Strict, Moderate, or Baseline]
- Environment context: [regulated, standard enterprise, startup, OS mix, MDM available yes/no, SIEM available yes/no]
- Org-specific constraints: [allowed package managers, blocked file reads, allowed MCP servers, egress restrictions]

What to produce, in this order:

1. Rollout Plan
   - Phased rollout: pilot group, expanded pilot, org-wide
   - Exit criteria for each phase
   - Pre-rollout checklist: MDM path verified, secrets manager in place, SIEM ingest tested, rollback plan documented
   - What will break: workflows likely to be impacted by the chosen tier and the developer-facing message to send before rollout
   - Rollback procedure: exact files or keys to revert, MDM steps, communication template

2. Config Files
   - Use the exact filenames from the repo, for example `managed-settings-moderate.json`, `permissions-strict.json`, `config-baseline.toml`
   - Keep only settings necessary for the chosen tier
   - Necessary means the setting blocks a concrete threat the tier is designed to mitigate, or is required for the tool to function under that tier
   - Drop optional, decorative, or duplicative settings
   - Every non-trivial setting must have comments or companion documentation explaining:
     - What it does, one line
     - Why it is set this way for this tier, including the threat or workflow reason
     - What breaks if it is misconfigured or removed
   - For JSON files, keep deployable JSON valid and provide a parallel `.comments.md` mapping each key to its rationale. If a documentation-only JSONC example is needed, use `.jsonc` and also provide valid stripped `.json`
   - For TOML and YAML, use native inline comments
   - No secrets, tokens, or API keys in any file. Reference environment variables or secrets manager paths only
   - No em dashes in prose or comments. Use commas, colons, or parentheses

3. Tier Delta Table
   - Single table showing, for each setting in the file: Baseline value, Moderate value, Strict value, Reason for the difference
   - The table must help the admin understand what they trade off if they move tiers later

4. Deployment Steps, per tool
   - Exact file paths per OS, macOS, Windows, Linux where applicable
   - MDM payload guidance, Jamf, Intune, Workspace ONE, if the tool supports managed settings
   - If the tool does not have managed or MDM enforcement available, say so explicitly and recommend the next best control, such as onboarding script, repo-level config, or network egress filter
   - Validation commands to confirm the policy is active on an endpoint
   - Audit logging: where logs go, how to ship to SIEM, and what events to alert on

5. Workflow-Preservation Notes
   - For each blocked operation, suggest the safe equivalent the developer should use instead
   - Flag any setting that commonly causes false-positive friction and how to handle exception requests
   - If two tools overlap, for example Claude Code and Cursor both run shell commands, call out the overlap so the admin does not double-configure or leave a gap

Constraints:
- Assume the admin has not used these AI tools personally. Avoid jargon without a one-line definition the first time it appears
- Prefer the repo's tiered files as the base
- Do not invent new settings unless the threat model clearly requires it
- If you invent a setting, mark it `CUSTOM:` in the rationale and explain why existing repo settings are insufficient
- Bias toward fewer, well-justified settings over exhaustive coverage
- Preserve developer workflows where the requested tier allows it
- Validate changed JSON, YAML, TOML, and shell examples with the repo validation commands before committing
```
