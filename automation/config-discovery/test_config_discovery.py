#!/usr/bin/env python3
"""Smoke tests for the config discovery automation helpers."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


def load_module(module_name: str, file_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / file_name)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {file_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


discover_configs = load_module("discover_configs", "discover_configs.py")
build_agent_scope = load_module("build_agent_scope", "build_agent_scope.py")


class ExtractConfigCandidatesTest(unittest.TestCase):
    def test_finds_backtick_quoted_json_and_cli_candidates(self) -> None:
        text = """
        Use `mcpServers` for approved MCP servers.
        Set "disableWorkflows": true in managed settings.
        Block --dangerously-skip-permissions for enterprise users.
        Set CLAUDE_CODE_DISABLE_WORKFLOWS=1 for startup enforcement.
        Ignore "theme" because it is not a security config term.
        """

        candidates = discover_configs.extract_config_candidates(text)

        self.assertIn("mcpServers", candidates)
        self.assertIn("disableWorkflows", candidates)
        self.assertIn("--dangerously-skip-permissions", candidates)
        self.assertIn("CLAUDE_CODE_DISABLE_WORKFLOWS", candidates)
        self.assertNotIn("theme", candidates)


class BuildAgentScopeTest(unittest.TestCase):
    def test_groups_multiple_sources_under_one_tool_limit(self) -> None:
        report = """
### Claude Code: Managed settings documentation

Potential config terms not found in local tool files:

`disableWorkflows`, `permissionMode`

### Claude Code: Hooks documentation

Potential config terms not found in local tool files:

`ConfigChange`

### Cursor: MCP documentation

Potential config terms not found in local tool files:

`mcpAllowlist`
"""

        scope = build_agent_scope.build_scope(report, max_tools=1)

        self.assertIn("## Tools to process (1 of 2 with missing terms)", scope)
        self.assertIn("- Source: Managed settings documentation", scope)
        self.assertIn("- Source: Hooks documentation", scope)
        self.assertIn("## Deferred (1 tools)", scope)
        self.assertIn("- Cursor (MCP documentation)", scope)


if __name__ == "__main__":
    unittest.main()
