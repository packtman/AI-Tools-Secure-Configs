## Summary

<!-- Brief description of what this PR adds or changes -->

## Type of Change

- [ ] New tool configuration
- [ ] Bug fix (config syntax, bypass, or misconfiguration)
- [ ] Improvement to existing configs
- [ ] Documentation update
- [ ] Repository infrastructure (CI, templates, etc.)

## Tool(s) Affected

<!-- Which tool directories are modified? -->

## Security Review Checklist

- [ ] No secrets, API keys, tokens, or credentials in any file
- [ ] Follows least-privilege principle (defaults are restrictive)
- [ ] Dangerous patterns are denied/blocked
- [ ] Rationale documented for non-obvious settings
- [ ] Tested against the tool version specified in the config comments
- [ ] Tier files (strict/moderate/baseline) are consistent with each other

## Validation

- [ ] JSON files pass `python3 -m json.tool`
- [ ] YAML files pass `yaml.safe_load()`
- [ ] TOML files pass `tomllib.loads()`
- [ ] Internal Markdown links resolve correctly

## Testing

<!-- How did you validate this config works as intended? -->

## Breaking Changes

<!-- Does this change any existing config in a way that would affect users who have already deployed it? -->
