# Plugin & Hooks Audit Rules

## Table of Contents

- [Plugin System Audit](#plugin-system-audit)
- [Hooks Audit](#hooks-audit)
- [Hook Scripts Audit](#hook-scripts-audit)

---

## Plugin System Audit

> Source: Claude Code official documentation (github.com/anthropics/claude-code)
> For complete plugin structure specifications, see `plugin-structure-spec.md`

### Plugin-Level Validation

| Check | Rule | Severity |
|-------|------|----------|
| plugin.json exists | Must be in `.claude-plugin/` directory | Fatal |
| plugin.json valid JSON | Parseable, no syntax errors | Fatal |
| name field | Required, kebab-case | Severe |
| version field | Semver format if present | Warning |
| Component dirs at root | Not inside `.claude-plugin/` | Fatal |

### Cross-Component Validation

| Check | Rule | Severity |
|-------|------|----------|
| Path references | Use `${CLAUDE_PLUGIN_ROOT}` everywhere | Severe |
| Command→Agent refs | Referenced agents exist | Severe |
| Agent→Skill refs | Referenced skills exist | Severe |
| Hook→Script refs | Referenced scripts exist | Fatal |
| Naming consistency | Consistent naming across components | Warning |
| No circular refs | No circular dependencies | Severe |

### Common Plugin Issues

**Should Flag:**
- plugin.json not in `.claude-plugin/`
- Component directories inside `.claude-plugin/`
- Hardcoded paths (not using `${CLAUDE_PLUGIN_ROOT}`)
- Referenced components don't exist
- hooks.json missing wrapper format
- Invalid JSON in any config file

**Should NOT Flag:**
- Missing optional components (not all plugins need all types)
- Custom directory names (if properly configured in plugin.json)
- Style variations within components

---

## Hooks Audit

> Source: Claude Code official documentation (github.com/anthropics/claude-code)

### Hook Events

| Event | Description | Matcher Support |
|-------|-------------|-----------------|
| PreToolUse | Before tool execution, can approve/deny/modify | Yes |
| PostToolUse | After tool succeeds, for feedback/logging | Yes |
| Stop | When main agent considers stopping | Yes |
| SubagentStop | When subagent considers stopping | Yes |
| SessionStart | At session beginning | Yes |
| Notification | On notification events | Yes |

### hooks.json Format (Plugin Context)

> Source: Claude Code hook-development SKILL.md

**Plugin hooks.json MUST use wrapper format:**
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...]
  }
}
```

**NOT direct format (that's for settings.json):**
```json
{
  "PreToolUse": [...],
  "Stop": [...]
}
```

### Hook Configuration Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
            "timeout": 30
          },
          {
            "type": "prompt",
            "prompt": "Validate file write safety: system paths, credentials, path traversal"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion: tests run, build succeeded"
          }
        ]
      }
    ]
  }
}
```

### Hook Definition Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| matcher | string | Yes | Regex or wildcard to match tool name |
| hooks | array | Yes | Array of hook configurations |
| hooks[].type | string | Yes | `command`, `prompt`, or `agent` |
| hooks[].command | string | For command | Shell command to execute |
| hooks[].prompt | string | For prompt/agent | Natural language prompt |
| hooks[].timeout | number | No | Timeout in seconds (default: 60 for command, 30 for prompt) |

### Hook Types

| Type | Description | Use Case |
|------|-------------|----------|
| `command` | Execute shell command | Scripts, validation |
| `prompt` | LLM-based evaluation | Complex decisions |
| `agent` | Agentic verifier | Multi-step verification |

### Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `Write` | Only Write tool |
| `Edit\|Write` | Edit or Write |
| `Notebook.*` | All Notebook tools |
| `*` or `""` | All tools |
| `mcp__server__tool` | Specific MCP tool |
| `mcp__server__.*` | All tools from MCP server |

### Hook Output Formats

> Source: Claude Code hook-development SKILL.md

**Standard output (all hooks):**
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

**PreToolUse specific output:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

**Stop/SubagentStop specific output:**
```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

### Environment Variables Available to Hooks

| Variable | Description |
|----------|-------------|
| `CLAUDE_PLUGIN_ROOT` | Plugin root directory |
| `CLAUDE_PROJECT_DIR` | Current project directory |
| `CLAUDE_ENV_FILE` | Path to persistent environment file |

### Hooks Validation

| Check | Rule | Severity |
|-------|------|----------|
| Wrapper format | `{"hooks": {...}}` in plugin context | Fatal |
| Valid JSON | Parseable, no syntax errors | Fatal |
| Event names valid | Known event names only | Severe |
| Hook types valid | `command`, `prompt`, or `agent` | Severe |
| Path references | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |
| Scripts exist | Referenced scripts must exist | Fatal |
| Matcher syntax | Valid regex pattern | Severe |
| Timeout values | Positive numbers | Warning |

### Common Hook Issues

**Should Flag:**
- Missing wrapper format in plugin hooks.json
- Hardcoded paths instead of `${CLAUDE_PLUGIN_ROOT}`
- Invalid event names
- Referenced scripts don't exist
- Invalid matcher regex syntax
- Missing timeout for long-running operations

**Should NOT Flag:**
- Missing description field (optional)
- Using command type instead of prompt (design choice)
- Using agent type for complex verification

---

## Hook Scripts Audit

> Source: Claude Code hook-development SKILL.md

### Script Requirements

**Bash scripts should:**
```bash
#!/bin/bash
set -euo pipefail

# Read JSON input from stdin
input=$(cat)

# Parse with jq
tool_name=$(echo "$input" | jq -r '.tool_name')

# Output valid JSON
echo '{"continue": true}'
```

**Python scripts should:**
```python
#!/usr/bin/env python3
import sys
import json

# Read JSON input from stdin
input_data = json.load(sys.stdin)

# Process...

# Output valid JSON
print(json.dumps({"continue": True}))
```

### Script Input Format (stdin)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "hook_type": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "..."
  }
}
```

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Read stdout for decision |
| 2 | Blocking error | Operation blocked, read stderr for reason |
| Other | Hook failed | Operation continues with default behavior |

### Script Validation Rules

| Check | Rule | Severity |
|-------|------|----------|
| Shebang line | `#!/bin/bash` or `#!/usr/bin/env python3` | Warning |
| Error handling | `set -euo pipefail` for bash | Warning |
| Input parsing | Read from stdin as JSON | Severe |
| Output format | Valid JSON to stdout | Severe |
| Variable quoting | All variables quoted in bash | Warning |
| Exit codes | Use 0 for success, 2 for blocking | Warning |
| Path references | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |
| No hardcoded paths | Avoid absolute paths | Severe |

### Script Best Practices

**Should have:**
- Proper shebang line
- Error handling (`set -euo pipefail` or try/except)
- JSON input parsing from stdin
- Valid JSON output to stdout
- Quoted variables (bash)
- Appropriate exit codes

**Should avoid:**
- Hardcoded absolute paths
- Unquoted variables
- Long-running operations without timeout
- Destructive operations without confirmation
- Secrets in script content

### Common Script Issues

**Should Flag:**
- Missing shebang line
- Missing `set -euo pipefail` in bash scripts
- Unquoted variables in bash
- Hardcoded paths
- Invalid JSON output
- Missing error handling
- Exit code 1 used for blocking (should be 2)

**Should NOT Flag:**
- Simple scripts without extensive validation
- Using Python instead of bash (design choice)
- Different JSON parsing methods
