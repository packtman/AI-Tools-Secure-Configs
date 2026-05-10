# Project Security Instructions for Claude Code

## Absolute Prohibitions

- NEVER read, display, log, or reference the contents of `.env`, `.env.*`, or any file under `secrets/`.
- NEVER read or reference private keys (`.pem`, `.key`, `.p12`, `.pfx`), SSH keys, AWS credentials, or cloud provider configuration files.
- NEVER commit secrets, API keys, tokens, passwords, or credentials into source control.
- NEVER execute destructive commands (`rm -rf /`, `DROP DATABASE`, `FORMAT`, `mkfs`, etc.) without explicit user confirmation.
- NEVER use `curl | bash`, `wget | sh`, or similar piped-execution patterns.
- NEVER use `eval`, `exec`, `su`, `sudo`, or privilege escalation commands.
- NEVER start network listeners (`nc -l`, `python -m http.server`, `socat`, etc.).
- NEVER modify shell configuration files (`.bashrc`, `.zshrc`, `.profile`).
- NEVER modify `.gitignore` to expose previously-ignored sensitive files.
- NEVER disable TLS verification, SSL checks, or certificate validation in generated code.
- NEVER install packages from unverified sources or arbitrary URLs.
- NEVER force-push to shared branches or rewrite public git history.

## Infrastructure & Deployment Safety

- ALWAYS confirm with the user before running commands that modify infrastructure:
  - `terraform apply`, `terraform destroy`
  - `kubectl delete`, `kubectl apply` (on production contexts)
  - `docker rm`, `docker system prune`
  - `aws` commands that create/modify/delete resources
  - `gcloud` commands that modify project settings
  - Any database migration commands
- ALWAYS confirm before modifying CI/CD pipeline configurations.
- ALWAYS confirm before modifying Dockerfile or docker-compose files.

## Secure Code Generation

- Use environment variables for all secrets and configuration values.
- Never hard-code connection strings, passwords, tokens, or API keys.
- When writing example code, always use placeholder values like `YOUR_API_KEY_HERE`.
- Use parameterized queries for all database operations — never string concatenation.
- Validate and sanitize all user inputs in generated code.
- Include error handling that does not leak sensitive implementation details.
- Use secure defaults: HTTPS, TLS 1.2+, strong encryption, secure cookie flags.
- Apply the principle of least privilege for IAM roles, file permissions, and access grants.
- Use well-maintained, actively-supported dependencies only.
- Never run containers as root — use non-root users.
- Never store secrets in CI/CD pipeline YAML — use the platform's secrets mechanism.
- Mask or redact sensitive data in log output.

## Git Hygiene

- Write clear, descriptive commit messages.
- Do not amend or force-push commits on shared branches.
- Do not modify `.gitignore` to expose previously ignored sensitive files.
- Do not commit generated artifacts, build output, or dependency directories.

## Dependency Management

- Do not introduce new dependencies without explicit approval.
- Prefer well-known, actively-maintained libraries over obscure alternatives.
- Pin dependency versions for reproducible builds.
- Check for known vulnerabilities before adding dependencies.
