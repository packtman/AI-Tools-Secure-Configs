# AGENTS.md

## Cursor Cloud specific instructions

This is a **documentation and configuration reference repository** (AI-Secure-Configs). It contains security-hardened configuration templates, deployment guides, and a scheduled config-discovery automation for AI coding tools. There is no runnable application, no build system, and no package dependencies.

### Repository structure

Each top-level directory (e.g. `claude-code/`, `cursor/`, `github-copilot/`) provides config templates and markdown guides for a specific AI tool. The `rollout-guide/` directory contains a cross-tool deployment plan. The `automation/config-discovery/` directory and `.github/workflows/config-discovery.yml` keep the repo aware of upstream vendor config changes.

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

# Validate config-discovery source registry
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report automation/config-discovery/reports/latest-config-discovery.md \
  --check

# Run config-discovery helper tests
python3 -m unittest automation/config-discovery/test_config_discovery.py
```

### Tools available in the environment

- `python3` with `yaml`, `toml` packages for config validation
- `yamllint` at `~/.local/bin/yamllint`
- `bash -n` for shell script syntax checking
- `git` for version control

### Notes

- JSONC files (`.jsonc`) contain comments and cannot be validated with standard JSON parsers; they are documentation-oriented config examples.
- The `claude-code/CLAUDE.md` file is a security instructions template (not project documentation for this repo itself).
- `.github/workflows/config-discovery.yml` is the scheduled maintenance workflow. It should only change discovery state, reports, and scoped config updates produced by the maintenance agent.
