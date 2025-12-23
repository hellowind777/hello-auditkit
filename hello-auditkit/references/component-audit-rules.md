# Component Audit Rules

## Table of Contents

- [Commands Audit](#commands-audit)
- [Agents Audit](#agents-audit)
- [Skills Audit](#skills-audit)

---

## Commands Audit

> Source: Claude Code official documentation (github.com/anthropics/claude-code)

### Frontmatter Validation

| Field | Rule | Severity |
|-------|------|----------|
| description | Optional but recommended, brief description | Info |
| argument-hint | Documents expected arguments (e.g., `[pr-number] [priority]`) | Info |
| allowed-tools | Valid tool names (string or array) | Severe |
| model | `sonnet`, `opus`, `haiku` | Severe |
| disable-model-invocation | Boolean, prevents LLM invocation | Info |

### allowed-tools Formats

> Source: Claude Code frontmatter-reference.md

```yaml
# Single tool
allowed-tools: Read

# Multiple tools (comma-separated string)
allowed-tools: Read, Write, Edit

# Multiple tools (array)
allowed-tools:
  - Read
  - Write
  - Bash(git:*)

# Bash with command filter
allowed-tools: Bash(git:*)    # Only git commands
allowed-tools: Bash(npm:*)    # Only npm commands
allowed-tools: Bash(docker:*) # Only docker commands

# MCP tools
allowed-tools: ["mcp__server__tool_name"]
```

### Body Validation

| Check | Rule | Severity |
|-------|------|----------|
| Content type | Instructions for Claude, not user documentation | Severe |

> Note: Claude Code SlashCommand tool has a total metadata budget of 15,000 characters (configurable via `SLASH_COMMAND_TOOL_CHAR_BUDGET`).

### Content Validation

**Commands are instructions FOR Claude, not messages TO users.**

✅ **Correct (instructions for Claude):**
```markdown
Review this code for security vulnerabilities including:
- SQL injection
- XSS attacks
Provide specific line numbers and severity ratings.

Current files: !`git diff --name-only`
File content: @src/main.js

Arguments: $ARGUMENTS or $1, $2
```

❌ **Incorrect (messages to user):**
```markdown
This command will review your code for security issues.
You'll receive a report with vulnerability details.
```

### Command Features

| Feature | Syntax | Description |
|---------|--------|-------------|
| All arguments | `$ARGUMENTS` | All user-provided arguments |
| Positional args | `$1`, `$2`, `$3` | Individual arguments |
| Bash execution | `!`git status`` | Executes before command runs |
| File reference | `@path/to/file` | Includes file contents |
| Namespacing | Subdirectories | Creates namespaced commands |

### Common Command Issues

**Should Flag:**
- Invalid tool names in allowed-tools
- Hardcoded paths instead of `${CLAUDE_PLUGIN_ROOT}`
- Command body written as user documentation instead of Claude instructions
- Missing `$ARGUMENTS` or `$1`, `$2` when arguments expected
- Bash execution syntax errors (missing `!` before backticks)
- Invalid Bash filter pattern (e.g., `Bash(invalid)`)

**Should NOT Flag:**
- Missing description (optional field)
- Style preferences in formatting
- Using `$ARGUMENTS` vs positional args (design choice)
- Using `disable-model-invocation: true` (design choice)

---

## Agents Audit

> Source: Claude Code official documentation (github.com/anthropics/claude-code)

### Frontmatter Validation

| Field | Type | Required | Severity |
|-------|------|----------|----------|
| name | string | Yes | Severe |
| description | string | Yes | Severe |
| model | string | No | Warning |
| color | string | No | Info |
| tools | array | No | Warning |

### Field Details

**name**
- Required, kebab-case identifier
- ≤50 characters recommended

**description**
- Required, must include when to use this agent
- Should include `<example>` blocks showing trigger scenarios
- ≤500 characters recommended

**model**
- Values: `inherit`, `sonnet`, `opus`, `haiku`
- Default: `inherit` (from conversation)

**color**
- Display color for agent
- Optional

**tools**
- Array of tool names agent can use
- Follows principle of least privilege

### tools Configuration Examples

> Source: Claude Code agent-development SKILL.md

```yaml
# Read-only analysis agent
tools: ["Read", "Grep", "Glob"]

# Code generation agent
tools: ["Read", "Write", "Grep"]

# Testing agent
tools: ["Read", "Bash", "Grep"]

# Full access (omit field or use wildcard)
tools: ["*"]
```

### Description with Examples Pattern

> Source: Claude Code agent-development SKILL.md

```yaml
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation description]
user: "[User request]"
assistant: "[How assistant should respond]"
<commentary>
[Why this agent should be triggered]
</commentary>
</example>
```

### Body Validation

| Check | Rule | Severity |
|-------|------|----------|
| Role definition | Clear role and methodology | Warning |
| Process steps | Step-by-step workflow | Info |
| Output guidance | Clear output expectations | Info |

**Agent body should include:**
- Clear role definition ("You are an agent that...")
- Core process or methodology
- Output format specification
- When applicable: specific instructions, constraints

### Common Agent Issues

**Should Flag:**
- Missing name or description
- Description doesn't explain when agent should be used
- Description lacks `<example>` blocks (recommended)
- Invalid tool names in tools array
- Agent body lacks clear instructions
- Circular agent references (Agent A calls Agent B calls Agent A)
- Overly generic descriptions that could match too many scenarios

**Should NOT Flag:**
- Missing optional fields (tools, model, color)
- Style variations in body structure
- Using `inherit` for model (valid choice)
- Missing `<example>` blocks if description is clear

---

## Skills Audit

> Source: Codex skill-creator official documentation

**A skill is any directory containing a `SKILL.md` file.** Skills consist of:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown body: instructions (required)
└── Bundled Resources (optional)
    ├── scripts/      - Executable code (Python/Bash/etc.)
    ├── references/   - Documentation loaded into context as needed
    └── assets/       - Files used in output (templates, icons, etc.)
```

### Skill Directory Validation

| Check | Rule | Severity |
|-------|------|----------|
| SKILL.md exists | Required in skill root | Fatal |
| Directory structure | scripts/, references/, assets/ if used | Info |
| No extraneous files | No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md | Warning |
| All references accessible | Files in references/ exist and readable | Severe |
| All scripts valid | Scripts have proper shebang, are executable | Warning |
| Reference depth | One level deep (no nested references) | Warning |
| Large files have TOC | Files >100 lines have table of contents | Info |
| Reference file size | Files >500 lines should consider splitting | Warning |

### Scripts Directory Audit

**Purpose**: Executable code for deterministic, reusable tasks

| Check | Rule | Severity |
|-------|------|----------|
| Shebang line | Present and correct (`#!/bin/bash`, `#!/usr/bin/env python3`) | Warning |
| Error handling | `set -euo pipefail` for bash, try/except for Python | Warning |
| Referenced in SKILL.md | Usage documented in SKILL.md | Info |
| Executable | File has execute permissions (or can be run with interpreter) | Warning |

### References Directory Audit

**Purpose**: Documentation loaded into context as needed (schemas, API docs, domain knowledge)

| Check | Rule | Severity |
|-------|------|----------|
| Referenced in SKILL.md | Clear "when to read" instructions | Warning |
| No duplication | Info not duplicated in SKILL.md body | Info |
| TOC for large files | Files >100 lines have table of contents | Info |
| One level deep | No nested references (references/ → more references/) | Warning |
| File size | Files >500 lines should consider splitting | Warning |

### Assets Directory Audit

**Purpose**: Files used in output, not loaded into context (templates, images, fonts)

| Check | Rule | Severity |
|-------|------|----------|
| Referenced in SKILL.md | Usage documented | Info |
| Appropriate content | Templates, images, fonts - not documentation | Info |

### Frontmatter Validation

| Field | Rule | Severity |
|-------|------|----------|
| name | Required, ≤64 characters | Severe |
| name | Lowercase letters, numbers, hyphens only | Warning |
| description | Required, ≤1024 characters (≤500 recommended) | Severe |
| description | Must include trigger conditions | Severe |
| allowed-tools | Valid tool names, comma-separated | Warning |

### Description Quality

**Good description pattern:**
```yaml
description: This skill should be used when the user asks to "specific phrase", "another phrase", mentions "keyword", or discusses topic-area.
```

**Must include:**
- Specific trigger phrases users might say
- Keywords that indicate relevance
- Topic areas the skill covers

**Should NOT include:**
- Implementation details
- Technical specifications
- Information that belongs in body

### Body Validation

**Length guidelines (from Codex skill-creator documentation):**
- ≤500 lines, <5k words: No risk
- 500-625 lines (≤25% over): Acceptable
- 625-750 lines (25-50% over): Low risk, consider optimization
- >750 lines (>50% over): Should optimize or split

**When body is too long, check in order:**
1. Contains explanations Claude already knows? → Delete
2. Lengthy text instead of concise examples? → Simplify
3. Repeated information? → Deduplicate
4. High-freedom tasks with excessive constraints? → Simplify
5. Still too long after optimization? → Split to references/

### Common Skill Issues

**Should Flag:**
- File not named `SKILL.md`
- Missing or empty name/description
- name >64 characters or description >1024 characters
- Description doesn't include trigger conditions
- Trigger conditions in body instead of description
- Body >750 lines without optimization
- References not mentioned in SKILL.md
- Deep reference nesting (>1 level)
- Unnecessary files (README.md, CHANGELOG.md in skill directory)
- Reference files >500 lines without splitting consideration

**Should NOT Flag:**
- Body 500-625 lines (acceptable range)
- Using references/ directory (good practice)
- Optional fields missing (allowed-tools)
- Style variations
