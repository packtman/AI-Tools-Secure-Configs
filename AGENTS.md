# AGENTS.md

## Cursor Cloud specific instructions

This is a **documentation and configuration reference repository** (AI-Secure-Configs). It contains security-hardened configuration templates and deployment guides for AI coding tools. There is no runnable application or build system. The only package installs are validation tools used by the automation workflows.

### Repository structure

Each top-level directory (e.g. `claude-code/`, `cursor/`, `github-copilot/`) provides config templates and markdown guides for a specific AI tool. The `rollout-guide/` directory contains a cross-tool deployment plan.

### File types

- `.md` — Documentation and deployment checklists
- `.json` / `.jsonc` — Configuration templates (70 JSON + 4 JSONC files)
- `.yaml` / `.yml` — Configuration templates (10 files)
- `.toml` — Configuration templates (14 files)
- `.sh` — Example hook scripts in `claude-code/examples/hook-scripts/`
- `.mdc` — Cursor rule files

### Development workflow

There is no dev server. Development consists of editing documentation, config files, and the lightweight config-discovery automation. To validate changes:

```bash
# Validate all deployable JSON, YAML, TOML, and shell examples
python3 scripts/validate_config_files.py

# Validate changed deployable files only
python3 scripts/validate_config_files.py --changed

# Validate JSON files
python3 -c "import json; json.load(open('path/to/file.json'))"

# Validate YAML files
yamllint -d relaxed path/to/file.yaml

# Validate TOML files
python3 -c "import toml; toml.load('path/to/file.toml')"

# Validate shell scripts
bash -n path/to/script.sh
```

### Tools available in the environment

- `python3` with `yaml`, `toml` packages for config validation
- `yamllint` at `~/.local/bin/yamllint`
- `bash -n` for shell script syntax checking
- `git` for version control

### Automation workflows

- `.github/workflows/config-discovery.yml` runs the scheduled upstream config scanner, builds an agent scope report, and opens a config-maintenance PR when watched sources change.
- `.github/workflows/config-validation.yml` validates deployable config examples and automation scripts on PRs.
- If `ANTHROPIC_API_KEY` is unavailable to the discovery workflow, it should open a discovery handoff PR for Cursor Automation or human review instead of failing the run.

### Notes

- JSONC files (`.jsonc`) contain comments and cannot be validated with standard JSON parsers; they are documentation-oriented config examples.
- The `claude-code/CLAUDE.md` file is a security instructions template (not project documentation for this repo itself).
- Generated discovery files live under `automation/config-discovery/reports/` and `automation/config-discovery/state/`.
