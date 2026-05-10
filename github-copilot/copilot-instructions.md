# Copilot Instructions — Security-Focused Template

> Deploy this file as `.github/copilot-instructions.md` in each repository.

## Security Requirements

- Never generate code that contains hard-coded secrets, API keys, passwords, or tokens.
- Always use environment variables or a secrets manager for sensitive configuration.
- Use parameterized queries for all database operations — never string concatenation.
- Validate and sanitize all user inputs before processing.
- Use HTTPS for all network requests; never disable TLS verification.
- Apply the principle of least privilege for IAM roles, file permissions, and access grants.
- Never generate code that runs as root in containers — use a non-root user.

## Code Quality

- Follow the existing code style and conventions in this repository.
- Write comprehensive error handling that does not expose internal details.
- Include input validation on all public APIs and user-facing functions.
- Use well-maintained, actively-supported dependencies only.
- Generate code that passes SAST tools (CodeQL, Semgrep, Bandit).

## Sensitive Data

- Never reference or include contents from `.env`, `.env.*`, or `secrets/` directories.
- Use placeholder values like `YOUR_API_KEY_HERE` in examples.
- Mask sensitive data in log output and error messages.
- Do not log request/response bodies that may contain PII.

## Infrastructure as Code

- Use the latest stable provider versions in Terraform/OpenTofu.
- Enable encryption at rest and in transit for all cloud resources.
- Never use `0.0.0.0/0` in security group ingress rules for production.
- Enable logging and monitoring on all cloud resources.
- Use private subnets for databases and internal services.
