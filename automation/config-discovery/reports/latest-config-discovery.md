# Config Discovery Report

This report was generated because one or more watched upstream sources changed or local coverage changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude API | Anthropic admin API documentation | local-coverage-changed | 200 | https://platform.claude.com/docs/en/api/admin.md |
| Claude API | Anthropic API release notes | local-coverage-changed | 200 | https://platform.claude.com/docs/en/release-notes/api.md |

## Review Details

### Claude API: Anthropic admin API documentation

- Change type: `local-coverage-changed`
- Source URL: https://platform.claude.com/docs/en/api/admin.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... erDeleteResponse object { id, type }` - `id: string` ID of the User. - `type: "user_deleted"`
Deleted object type. For Users, this is always `"user_deleted"`. - `"user_deleted"` # Workspaces ##
Create Workspace **post** `/v1/organizations/workspaces` Create Workspace ### Header Parameters -
`"anthropic-beta": optional array of string` Optional header to specify the b ...

> ... ways `"organization"`. - `"organization"` # Invites ## Create Invite **post**
`/v1/organizations/invites` Create Invite ### Body Parameters - `email: string` Email of the User. -
`role: "billing" or "claude_code_user" or "developer" or "user"` Role for the invited User. Cannot
be "admin". - `"billing"` - `"claude_code_user"` - `"developer"` - `"user"` ### Return ...

> # Admin # Organizations ## Get Current Organization **get** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. ### Returns -
`Organization object { id, name, type }` - `id: string` ID of the Organization. - `name: string`
Name of the Organization. - `type: "organization"` Object type. For ...

> ... Workspace Members, this is always `"workspace_member_deleted"`. - `"workspace_member_deleted"` -
`user_id: string` ID of the User. - `workspace_id: string` ID of the Workspace. # Rate Limits ##
List Workspace Rate Limits **get** `/v1/organizations/workspaces/{workspace_id}/rate_limits` List
rate-limit overrides configured for a workspace. Returns only the groups and ...

> # Admin # Organizations ## Get Current Organization **get** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. ### Returns - `Or ...

Potential config terms found upstream are already present in local tool files.

### Claude API: Anthropic API release notes

- Change type: `local-coverage-changed`
- Source URL: https://platform.claude.com/docs/en/release-notes/api.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... [Claude Opus 4.8](/docs/en/about-claude/models/migration-guide). Read more in [Fast
mode](/docs/en/build-with-claude/fast-mode#supported-models). ### June 26, 2026 * We've raised [rate
limits](/docs/en/api/rate-limits) across the Claude API. Claude Sonnet and Claude Haiku rate limits
now match Claude Opus at every usage tier, and usage tiers have been consolidated int ...

> ... t API moved from `/v1/organizations/tunnels` on the Admin API to `/v1/tunnels` on the Claude
API. The new surface uses the `anthropic-beta: mcp-tunnels-2026-06-22` header and the
`workspace:manage_tunnels` WIF scope. The previous surface remains available during a migration
window. See the [Tunnels API reference](/docs/en/api/beta/tunnels). ### June 18, 2026 * The Py ...

> ... ine. See [CMEK content preservation](/docs/en/manage-claude/access-transparency#cmek-content-
preservation). ### July 8, 2026 * You can now set an expiration when you create an API key or an
Admin API key in the [Claude Console](https://platform.claude.com/settings/keys). Choose a preset, a
custom duration, or **Never**. For keys with a lifetime of at least 7 da ...

> ... ks-libraries/cli/quickstart). ### April 7, 2026 * We announced [Claude Mythos
Preview](https://anthropic.com/glasswing) is available as a gated research preview for defensive
cybersecurity work as part of [Project Glasswing](https://anthropic.com/glasswing). Access is
invitation-only. * The [Messages API](/docs/en/api/messages) is now available on Amazon Bedrock as
...

Potential config terms found upstream are already present in local tool files.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.
