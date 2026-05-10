# Google Gemini — Admin Security Policy

## 1. Identity & Access

- [ ] **Least privilege IAM** — Default to `roles/cloudaicompanion.user`; reserve admin roles.
- [ ] **Service accounts** — Use dedicated service accounts for automated API access.
- [ ] **MFA** — Enforce 2-step verification for all GCP users.
- [ ] **Conditional access** — Use Access Context Manager for context-aware access policies.
- [ ] **Domain restriction** — Apply `constraints/iam.allowedPolicyMemberDomains` org policy.

## 2. Safety & Content Filtering

- [ ] **Safety filters** — Apply `BLOCK_MEDIUM_AND_ABOVE` or stricter for all categories.
- [ ] **Application-layer validation** — Implement content moderation in your application layer.
- [ ] **PII detection** — Enable PII scanning on inputs before sending to the API.
- [ ] **Output validation** — Validate model outputs before presenting to end users.

## 3. Network Security

- [ ] **VPC Service Controls** — Add Gemini APIs to a VPC perimeter.
- [ ] **Private connectivity** — Use Cloud VPN or Cloud Interconnect for dedicated connections.
- [ ] **Firewall rules** — Restrict egress to Gemini API endpoints only.
- [ ] **DNS** — Use private DNS to route Gemini traffic through VPC.

## 4. Data Governance

- [ ] **Logging** — Disable Gemini Code Assist logging unless required (disabled by default).
- [ ] **Data sharing** — Disable prompt/response sharing for Gemini Cloud Assist (disabled by default).
- [ ] **Data residency** — Ensure Gemini data processing occurs in approved regions.
- [ ] **Training opt-out** — Verify Vertex AI API data is not used for training (default for API).
- [ ] **DLP** — Apply Cloud DLP before sending sensitive data to Gemini.

## 5. Organizational Controls

- [ ] **Org policies** — Restrict Gemini API usage to approved projects.
- [ ] **Quota limits** — Set per-project quotas for Gemini API calls.
- [ ] **Budget alerts** — Configure billing budgets with alerts at 50%, 75%, 90%.
- [ ] **Resource hierarchy** — Organize Gemini-using projects under appropriate folders.

## 6. Monitoring & Audit

- [ ] **Cloud Audit Logs** — Enable admin and data access logs for Gemini APIs.
- [ ] **Cloud Monitoring** — Set up alerts for unusual API usage patterns.
- [ ] **Security Command Center** — Integrate Gemini findings.
- [ ] **Incident response** — Document runbook for revoking access and investigating misuse.
