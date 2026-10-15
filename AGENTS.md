# AGENTS.md

## Cursor Cloud specific instructions

This is a **documentation and configuration reference repository** (AI-Secure-Configs). It contains security-hardened configuration templates and deployment guides for AI coding tools. There is no runnable application, no build system, and no application package dependencies.

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
```

You can also validate all deployable config files with:

```bash
python3 scripts/validate_config_files.py
```

To validate only branch, staged, and unstaged config changes relative to a base ref:

```bash
python3 scripts/validate_config_files.py --changed origin/main
```

### Tools available in the environment

- `python3` with `yaml`, `toml` packages for config validation
- `yamllint` at `~/.local/bin/yamllint`
- `bash -n` for shell script syntax checking
- `git` for version control

### Notes

- JSONC files (`.jsonc`) contain comments and cannot be validated with standard JSON parsers; they are documentation-oriented config examples.
- The `claude-code/CLAUDE.md` file is a security instructions template (not project documentation for this repo itself).
- GitHub workflows under `.github/workflows/` run config discovery and syntax validation. The config discovery workflow opens discovery-only PRs when `ANTHROPIC_API_KEY` is unavailable, so Cursor Automation or a human reviewer can finish the config update.
