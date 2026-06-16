# AGENTS.md

## Cursor Cloud specific instructions

This is a **documentation and configuration reference repository** (AI-Secure-Configs). It contains security-hardened configuration templates and deployment guides for AI coding tools. There is no runnable application, no build system, and no package dependencies.

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

There is no build, test suite, or dev server. Development consists of editing documentation and config files. To validate changes:

```bash
# Validate JSON files
python3 -c "import json; json.load(open('path/to/file.json'))"

# Validate YAML files
yamllint -d relaxed path/to/file.yaml

# Validate TOML files
python3 -c "import toml; toml.load('path/to/file.toml')"

# Validate shell scripts
bash -n path/to/script.sh

# Validate all deployable configs and workflow YAML
python3 scripts/validate_config_files.py

# Validate only changed deployable configs against a base ref
python3 scripts/validate_config_files.py --changed origin/main
```

### Tools available in the environment

- `python3` with `yaml`, `toml` packages for config validation
- `yamllint` at `~/.local/bin/yamllint`
- `bash -n` for shell script syntax checking
- `git` for version control

### Automation workflow

The scheduled config-maintenance loop lives in `automation/config-discovery/` and `.github/workflows/config-discovery.yml`.

- `discover_configs.py` watches official upstream vendor sources and writes discovery reports.
- `build_agent_scope.py` limits each maintenance run to a small set of affected tools.
- `agent-prompt.md` tells the maintenance agent how to update tiered configs, rollout docs, rationale, and validation notes.
- `scripts/validate_config_files.py` validates deployable JSON, YAML, TOML, and shell files.
- `.github/workflows/config-validation.yml` runs syntax validation on pull requests and manual dispatch.

If `ANTHROPIC_API_KEY` is unavailable to the scheduled workflow, the workflow still opens a discovery-only PR so Cursor Automation or a human reviewer can apply the config-maintenance prompt.

### Notes

- JSONC files (`.jsonc`) contain comments and cannot be validated with standard JSON parsers; they are documentation-oriented config examples.
- The `claude-code/CLAUDE.md` file is a security instructions template (not project documentation for this repo itself).
- There is no runnable app CI. The configured GitHub workflows are for config discovery and syntax validation only.
