# Plugin Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Execution Required**: Execute each check table below. Verify structure, paths, components (commands, agents, hooks, MCP, LSP).

## Table of Contents

- [Overview](#overview)
- [Plugin Structure](#plugin-structure)
- [Plugin Manifest](#plugin-manifest)
- [Commands Audit](#commands-audit)
- [Agents Audit](#agents-audit)
- [Hooks Audit](#hooks-audit)
- [MCP Servers Audit](#mcp-servers-audit)
- [LSP Servers Audit](#lsp-servers-audit)
- [Common Issues](#common-issues)

---

## Overview

**Plugin identification**: Directory with `.claude-plugin/plugin.json`

```
plugin-name/
├── .claude-plugin/plugin.json  (required)
├── commands/                    (slash commands)
├── agents/                      (subagent definitions)
├── skills/                      (agent skills)
├── hooks/hooks.json             (event handlers)
├── .mcp.json                    (MCP servers)
└── .lsp.json                    (LSP servers)
```

**CRITICAL**: Components MUST be at root level, NOT inside `.claude-plugin/`

---

## Plugin Structure

### Critical Rules

| Rule | Requirement | Severity |
|------|-------------|----------|
| Manifest location | `plugin.json` in `.claude-plugin/` | Fatal |
| Component dirs | At plugin root, NOT in `.claude-plugin/` | Fatal |
| Skill file naming | Exactly `SKILL.md` (case-sensitive) | Fatal |
| Command/Agent format | `.md` files with YAML frontmatter | Severe |
| Hooks format | Wrapper `{"hooks": {...}}` | Severe |
| Path references | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |
| Naming | kebab-case for all names | Warning |

### Path Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory | Hooks, MCP, LSP, scripts |
| `${CLAUDE_PROJECT_DIR}` | Project root | Hooks, scripts |
| `${CLAUDE_ENV_FILE}` | Env file path | SessionStart hooks |

### Never Use

- Hardcoded absolute paths (`/Users/name/...`)
- Relative paths from working directory
- Home shortcuts (`~/plugins/...`)

---

## Plugin Manifest

### plugin.json

**Required:**
```json
{
  "name": "plugin-name"
}
```

**Recommended:**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation"
}
```

### Validation Rules

| Field | Rule | Severity |
|-------|------|----------|
| name | Required, non-empty, kebab-case | Fatal |
| name | ≤50 characters | Warning |
| version | Semver format (X.Y.Z) | Warning |
| description | ≤200 characters | Warning |
| Custom paths | Relative, start with `./` | Severe |

---

## Commands Audit

**Location**: `commands/*.md`

### Frontmatter

```yaml
---
description: Brief description for /help
argument-hint: <required> [optional]
allowed-tools: [Read, Glob, Grep]
model: sonnet
---
```

| Field | Rule | Severity |
|-------|------|----------|
| description | Recommended, ≤100 chars | Info |
| allowed-tools | Valid tool names | Severe |
| model | `sonnet`, `opus`, `haiku` | Severe |

### allowed-tools Formats

```yaml
# Single tool
allowed-tools: Read

# Multiple (string)
allowed-tools: Read, Write, Edit

# Multiple (array)
allowed-tools:
  - Read
  - Bash(git:*)

# MCP tools
allowed-tools: ["mcp__server__tool"]
```

### Content Rule

**Commands are instructions FOR Claude, not messages TO users.**

✅ **Correct:**
```markdown
Review this code for vulnerabilities:
- SQL injection, XSS attacks
Provide line numbers and severity.
```

❌ **Incorrect:**
```markdown
This command will review your code.
You'll receive a report.
```

### Command Prompt Quality

> **Full LLM checks**: See `rules-universal.md` → LLM Prompting Best Practices

| Check | Requirement | Severity |
|-------|-------------|----------|
| Clear task | Specific, actionable instruction | Severe |
| Verbosity constraint | Output length specified | Warning |
| Scope boundaries | What NOT to do | Warning |
| Freedom level match | Constraints fit task fragility | Warning |
| No AI-known content | Don't explain standard concepts | Info |
| Tool preference | Prefer tools over internal knowledge | Warning |
| Agentic updates | Brief updates at major phases (if agentic) | Warning |

---

## Agents Audit

**Location**: `agents/*.md`

### Frontmatter

```yaml
---
name: agent-name
description: Agent role and when to use
tools: [Glob, Grep, Read]
model: sonnet
---
```

| Field | Required | Rule | Severity |
|-------|----------|------|----------|
| name | Yes | kebab-case, ≤50 chars | Severe |
| description | Yes | Include when to use, ≤500 chars | Severe |
| tools | No | Valid tool names | Warning |
| model | No | `inherit`, `sonnet`, `opus`, `haiku` | Warning |

### Description Pattern

```yaml
description: Use this agent when [conditions]. Examples:

<example>
Context: [Situation]
user: "[Request]"
assistant: "[Response]"
<commentary>
[Why this agent triggered]
</commentary>
</example>
```

### Agent Body Quality (LLM Best Practices)

> **Full LLM checks**: See `rules-universal.md` → LLM Prompting Best Practices

| Check | Requirement | Severity |
|-------|-------------|----------|
| Clear role | Specific agent purpose | Severe |
| Trigger conditions | In description, not body | Severe |
| Verbosity constraints | Output expectations | Warning |
| Scope discipline | What agent should NOT do | Warning |
| Tool usage guidance | When to use which tools | Info |
| Freedom level match | Constraint level fits task | Warning |
| Conciseness | No redundant explanations | Warning |
| Tool preference | Prefer tools over internal knowledge | Warning |
| Agentic updates | Brief updates at major phases, concrete outcomes | Warning |
| No task expansion | Don't expand beyond user request | Warning |
| Long-context outline | For >10k tokens: outline, restatement | Warning |

---

## Hooks Audit

### hooks.json Format (Plugin Context)

**MUST use wrapper format:**
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
  "PreToolUse": [...]  // Wrong for plugins
}
```

### Hook Events

| Event | Description | Matcher |
|-------|-------------|---------|
| PreToolUse | Before tool, can approve/deny/modify | Yes |
| PostToolUse | After tool succeeds | Yes |
| Stop | Main agent considers stopping | Yes |
| SubagentStop | Subagent considers stopping | Yes |
| SessionStart | Session begins | Yes |
| Notification | On notification | Yes |

### Hook Configuration

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
          }
        ]
      }
    ]
  }
}
```

### Hook Types

| Type | Description | Use Case |
|------|-------------|----------|
| `command` | Execute shell | Scripts, validation |
| `prompt` | LLM evaluation | Complex decisions |
| `agent` | Agentic verifier | Multi-step verification |

### Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `Write` | Only Write |
| `Edit\|Write` | Edit or Write |
| `Notebook.*` | All Notebook tools |
| `*` or `""` | All tools |
| `mcp__server__.*` | All from MCP server |

### Hook Scripts

**Bash:**
```bash
#!/bin/bash
set -euo pipefail
input=$(cat)  # Read JSON from stdin
tool_name=$(echo "$input" | jq -r '.tool_name')
echo '{"continue": true}'  # Output JSON
```

**Python:**
```python
#!/usr/bin/env python3
import sys, json
input_data = json.load(sys.stdin)
print(json.dumps({"continue": True}))
```

| Check | Rule | Severity |
|-------|------|----------|
| Shebang | Present | Warning |
| Input | Read JSON from stdin | Severe |
| Output | Valid JSON to stdout | Severe |
| Exit codes | 0=success, 2=blocking | Warning |
| Paths | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |

---

## MCP Servers Audit

**Location**: `.mcp.json`

### Formats

**stdio (local):**
```json
{
  "server-name": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
    "env": {"API_KEY": "${MY_API_KEY}"}
  }
}
```

**HTTP:**
```json
{
  "api-server": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {"Authorization": "Bearer ${API_TOKEN}"}
  }
}
```

### Validation

| Check | Rule | Severity |
|-------|------|----------|
| Valid JSON | Parseable | Fatal |
| Server name | Unique, descriptive | Warning |
| command | Required for stdio | Severe |
| url | Required for http | Severe |
| Paths | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |
| Secrets | Use env variables, not hardcoded | Severe |

---

## LSP Servers Audit

**Location**: `.lsp.json`

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    }
  }
}
```

| Check | Rule | Severity |
|-------|------|----------|
| command | Required | Severe |
| extensionToLanguage | Required, valid mapping | Severe |
| transport | `stdio` or `socket` | Warning |
| Valid JSON | Parseable | Fatal |

---

## Common Issues

### Should Flag

| Issue | Severity |
|-------|----------|
| Missing `.claude-plugin/plugin.json` | Fatal |
| plugin.json not in `.claude-plugin/` | Fatal |
| Components inside `.claude-plugin/` | Fatal |
| Skill not named `SKILL.md` | Fatal |
| hooks.json missing wrapper | Severe |
| Hardcoded paths | Severe |
| Referenced component doesn't exist | Severe |
| Invalid JSON in config | Fatal |
| Hardcoded secrets | Severe |
| Invalid tool/event names | Severe |

### Should NOT Flag

| Pattern | Reason |
|---------|--------|
| Missing optional components | Not all plugins need all types |
| Custom directory names | Valid if configured |
| Style variations | Design choice |
| Missing README.md | Optional |
| Different organization | Design choice |
