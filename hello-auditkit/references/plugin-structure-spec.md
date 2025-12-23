# Plugin Structure Specification

## Table of Contents

- [Directory Structure Requirements](#directory-structure-requirements)
- [Plugin Manifest (plugin.json)](#plugin-manifest-pluginjson)
- [Component Directory Specifications](#component-directory-specifications)
- [Path Reference Rules](#path-reference-rules)
- [Naming Conventions](#naming-conventions)
- [Files That Should NOT Exist](#files-that-should-not-exist)
- [Auto-Discovery Mechanism](#auto-discovery-mechanism)
- [Common Structure Issues](#common-structure-issues)

---

## Directory Structure Requirements

### Important: Specification vs Reference Implementation

**The official plugin marketplace structure is a REFERENCE, not a mandatory standard.**

Only the following are REQUIRED by plugin specification:
- `.claude-plugin/plugin.json` must exist
- Components must be at plugin root level (not inside `.claude-plugin/`)
- Skills must use `SKILL.md` filename (case-sensitive)
- Hooks must use wrapper format in plugin context

**Everything else is OPTIONAL or a design choice:**
- Directory naming (commands/ vs cmds/ vs custom-commands/)
- File organization within directories
- Presence of README.md, scripts/, assets/, etc.
- Specific subdirectory structure

**Do NOT flag as issues:**
- Using different directory names than marketplace examples
- Having additional directories not in marketplace examples
- Organizing files differently than marketplace examples
- Missing optional directories (agents/, hooks/, etc.)

### Standard Plugin Layout (Reference Only)

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Slash commands (.md files)
│   └── command-name.md
├── agents/                   # Subagent definitions (.md files)
│   └── agent-name.md
├── skills/                   # Agent skills (subdirectories)
│   └── skill-name/
│       ├── SKILL.md         # Required for each skill
│       ├── references/      # Optional reference materials
│       ├── scripts/         # Optional helper scripts
│       └── examples/        # Optional examples
├── hooks/
│   ├── hooks.json           # Event handler configuration
│   └── scripts/             # Hook scripts
├── .mcp.json                # MCP server definitions
├── scripts/                 # Shared helper scripts
└── README.md                # Plugin documentation
```

### Critical Structure Rules

| Rule | Requirement | Severity |
|------|-------------|----------|
| Manifest location | `plugin.json` MUST be in `.claude-plugin/` directory | Fatal |
| Component directories | MUST be at plugin root level, NOT inside `.claude-plugin/` | Fatal |
| Skill file naming | MUST be exactly `SKILL.md` (case-sensitive) | Fatal |
| Command/Agent format | MUST be `.md` files with YAML frontmatter | Severe |
| Hooks format | MUST use wrapper format `{"hooks": {...}}` in plugin hooks.json | Severe |
| Path references | MUST use `${CLAUDE_PLUGIN_ROOT}` for portability | Severe |
| Naming convention | SHOULD use kebab-case for all names | Warning |

## Plugin Manifest (plugin.json)

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Name requirements:**
- Use kebab-case format (lowercase with hyphens)
- Must be unique across installed plugins
- No spaces or special characters
- Max length: 50 characters recommended

### Recommended Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  }
}
```

### Optional Fields

```json
{
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation"],
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "skills": "./custom-skills",
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

**Path Behavior Rules:**
- Custom paths SUPPLEMENT default directories (don't replace them)
- All paths must be relative to plugin root and start with `./`
- Multiple paths can be specified as arrays (e.g., `["./agents", "./more-agents"]`)

### Validation Rules

| Field | Rule | Error Type |
|-------|------|------------|
| name | Required, non-empty, kebab-case | Fatal |
| name | ≤50 characters | Warning |
| version | Semantic versioning format (X.Y.Z) | Warning |
| description | ≤200 characters recommended | Warning |
| Custom paths | Must be relative, start with `./` | Severe |

## Component Directory Specifications

### Commands Directory

**Location**: `commands/`
**File format**: `.md` files with YAML frontmatter
**Auto-discovery**: All `.md` files load automatically

**Required frontmatter:**
```yaml
---
description: Brief description for /help
---
```

**Optional frontmatter:**
```yaml
---
description: Command description
argument-hint: <required-arg> [optional-arg]
allowed-tools: [Read, Glob, Grep, Bash]
model: sonnet
disable-model-invocation: false
---
```

**Validation rules:**
- description: Required, ≤100 characters recommended
- argument-hint: Optional, documents expected arguments
- allowed-tools: Optional, restricts tool access
- model: Optional, one of: haiku, sonnet, opus

### Agents Directory

**Location**: `agents/`
**File format**: `.md` files with YAML frontmatter
**Auto-discovery**: All `.md` files load automatically

**Required frontmatter:**
```yaml
---
name: agent-name
description: Agent role and when to use
---
```

**Optional frontmatter:**
```yaml
---
name: agent-name
description: Agent description
tools: Glob, Grep, Read, WebFetch
model: sonnet
color: green
---
```

**Validation rules:**
- name: Required, kebab-case, ≤50 characters
- description: Required, ≤500 characters, must include trigger conditions
- tools: Optional, comma-separated tool list
- model: Optional, one of: haiku, sonnet, opus
- color: Optional, for UI display

### Skills Directory

**Location**: `skills/skill-name/`
**File format**: `SKILL.md` (exact name required)
**Auto-discovery**: All `SKILL.md` files in subdirectories load automatically

**Required frontmatter:**
```yaml
---
name: skill-name
description: Trigger conditions for this skill
---
```

**Optional frontmatter:**
```yaml
---
name: skill-name
description: Skill description with trigger conditions
version: 1.0.0
license: MIT
---
```

**Validation rules:**
- name: Required, ≤64 characters
- description: Required, ≤1024 characters (≤500 recommended), must include "when to use" information
- version: Optional, semantic versioning
- File must be named exactly `SKILL.md` (case-sensitive)
- Directory name should match skill name

**Skill subdirectory structure:**
```
skill-name/
├── SKILL.md          # Required
├── references/       # Optional: Reference materials (loaded on demand)
├── scripts/          # Optional: Helper scripts
├── examples/         # Optional: Example files
└── assets/           # Optional: Templates, resources
```

### Hooks Directory

**Location**: `hooks/`
**Configuration file**: `hooks.json`
**Scripts location**: `hooks/scripts/` or `hooks/`

**Plugin hooks.json format (wrapper required):**
```json
{
  "description": "Optional description",
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

**Hook event configuration:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Available hook events:**
- PreToolUse: Before tool execution
- PostToolUse: After tool execution
- Stop: When main agent stops
- SubagentStop: When subagent stops
- SessionStart: Session begins
- SessionEnd: Session ends
- UserPromptSubmit: User submits prompt
- PreCompact: Before context compaction
- Notification: User notification

**Hook types:**
- `command`: Execute bash command
- `prompt`: LLM-driven evaluation (for Stop, SubagentStop, UserPromptSubmit, PreToolUse)

**Validation rules:**
- Must use wrapper format with `"hooks": {...}`
- All paths must use `${CLAUDE_PLUGIN_ROOT}`
- Timeout values in seconds (default: 60 for command, 30 for prompt)
- Matcher patterns are case-sensitive

### MCP Servers

**Location**: `.mcp.json` at plugin root
**Format**: JSON configuration

**Example format:**
```json
{
  "server-name": {
    "type": "http",
    "url": "https://mcp.example.com/api"
  }
}
```

**Or with command:**
```json
{
  "server-name": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
    "env": {
      "API_KEY": "${API_KEY}"
    }
  }
}
```

**Validation rules:**
- Server names must be unique
- Use `${CLAUDE_PLUGIN_ROOT}` for paths
- Environment variables use `${VAR_NAME}` syntax

## Path Reference Rules

### Available Environment Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory | Hooks, MCP, LSP, scripts |
| `${CLAUDE_PROJECT_DIR}` | Project root directory | Hooks, scripts |
| `${CLAUDE_ENV_FILE}` | File path for persisting env vars | SessionStart hooks only |
| `${CLAUDE_CODE_REMOTE}` | `"true"` if running in web environment | Hooks |
| `$ARGUMENTS` | Hook input JSON (for prompt hooks) | Prompt hooks |

### ${CLAUDE_PLUGIN_ROOT}

**Must use for:**
- Hook command paths
- MCP server command arguments
- LSP server configurations
- Script execution references
- Resource file paths in hooks/MCP

**Never use:**
- Hardcoded absolute paths (`/Users/name/plugins/...`)
- Relative paths from working directory (`./scripts/...` in commands)
- Home directory shortcuts (`~/plugins/...`)

**Correct usage:**
```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

**In markdown files:**
```markdown
Reference: ${CLAUDE_PLUGIN_ROOT}/references/guide.md
Execute: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh`
```

## Naming Conventions

### Plugin Name
- kebab-case: `my-plugin-name`
- Descriptive: indicates purpose
- Unique: no conflicts with existing plugins

### Component Names
- Commands: `review-pr.md`, `run-tests.md`
- Agents: `code-reviewer.md`, `test-generator.md`
- Skills: `api-testing/`, `error-handling/`
- Scripts: `validate-input.sh`, `generate-report.py`

### Avoid
- Spaces in names
- Special characters (except hyphens)
- Generic names: `utils/`, `misc.md`, `temp.sh`
- Uppercase (except SKILL.md)

## Files That Should NOT Exist

Plugins should NOT contain:
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md` (unless specifically needed)
- Duplicate documentation
- Development-only files in production

**README.md is acceptable** for plugin documentation.

## Auto-Discovery Mechanism

The plugin system automatically discovers:
1. **Plugin manifest**: `.claude-plugin/plugin.json`
2. **Commands**: All `.md` files in `commands/`
3. **Agents**: All `.md` files in `agents/`
4. **Skills**: All `SKILL.md` files in `skills/*/`
5. **Hooks**: Configuration from `hooks/hooks.json`
6. **MCP servers**: Configuration from `.mcp.json`

**Discovery timing:**
- Plugin installation: Components register
- Plugin enable: Components become available
- No restart required for file changes (new session needed)

## Common Structure Issues

### Fatal Issues
- Missing `.claude-plugin/plugin.json`
- plugin.json not in `.claude-plugin/` directory
- Components inside `.claude-plugin/` instead of root
- Skill file not named `SKILL.md`

### Severe Issues
- Missing required frontmatter fields
- Hardcoded paths instead of `${CLAUDE_PLUGIN_ROOT}`
- hooks.json without wrapper format
- Invalid YAML frontmatter syntax

### Warnings
- Non-kebab-case naming
- Missing optional but recommended fields
- Overly long descriptions
- Missing README.md
