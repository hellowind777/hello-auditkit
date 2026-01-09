# Memory File Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Execution Required**: Execute each check table below. Verify import syntax, instruction quality, and content specificity.

## Table of Contents

- [Overview](#overview)
- [AGENTS.md Audit](#agentsmd-audit)
- [CLAUDE.md Audit](#claudemd-audit)
- [GEMINI.md Audit](#geminimd-audit)
- [Common Issues](#common-issues)

---

## Overview

**Applies to**: AI assistant memory/instruction files

| File Type | Platform | Purpose |
|-----------|----------|---------|
| AGENTS.md | Codex CLI | Agent instructions |
| CLAUDE.md | Claude Code | Memory files |
| GEMINI.md | Gemini CLI | Context files |

**Universal size limit**: ≤2000 lines recommended, ≤3000 limit

---

## AGENTS.md Audit

> Source: Codex CLI documentation

### Merge Hierarchy

AGENTS.md files merge top-down:
1. `~/.codex/AGENTS.md` - personal global
2. `AGENTS.md` at repo root - project-wide
3. `AGENTS.md` in cwd - folder-specific

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct hierarchy level | Info |
| Merge awareness | No conflicts with parent AGENTS.md | Severe |
| Instruction clarity | Clear, actionable instructions | Warning |
| Scope appropriateness | Instructions match file location | Warning |
| File length | ≤2000 lines recommended | Warning |

### Content Guidelines

**Good patterns:**
```markdown
- Always use TypeScript for new files
- Run `npm test` before committing
- Follow existing code style in the project
```

**Bad patterns:**
```markdown
- Be helpful (too vague)
- Do everything correctly (not actionable)
```

### Should Flag

- Contradictory instructions across hierarchy levels
- Vague, non-actionable instructions
- Instructions that don't match file scope
- Missing critical project-specific guidance

### Should NOT Flag

- Simple bullet-point format
- Reasonable instruction variations
- Optional guidance not present

---

## CLAUDE.md Audit

> Source: Claude Code documentation

### Memory Types

| Type | Location |
|------|----------|
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Project rules | `./.claude/rules/*.md` |
| User memory | `~/.claude/CLAUDE.md` |
| Project local | `./CLAUDE.local.md` |

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct for memory type | Info (advisory) |
| Import syntax | Valid `@path/to/file` | Fatal |
| Path-specific rules | Valid YAML frontmatter | Severe |
| Format | Bullet points and markdown headings | Info |
| File length | ≤2000 lines recommended | Warning |

### Import Syntax

**Valid:**
```markdown
@./shared-rules.md
@../common/rules.md
```

**Invalid:**
```markdown
@rules.md  (missing path prefix)
```

### Path-Specific Rules

```markdown
---
paths: src/api/**/*.ts
---
# API Rules
- All endpoints must include input validation
```

### Should Flag

- Invalid import syntax
- File in wrong location for memory type
- Invalid YAML frontmatter for path-specific rules
- Vague instructions ("format code properly")

### Should NOT Flag

- Missing optional sections
- Style variations
- Reasonable instruction choices

---

## GEMINI.md Audit

> Source: Gemini CLI documentation

### File Hierarchy

Files loaded and concatenated in order:
1. **Global**: `~/.gemini/GEMINI.md`
2. **Project root/ancestors**: Up to `.git` folder
3. **Subdirectories**: Below current directory

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct hierarchy level | Info (advisory) |
| Import syntax | Valid `@file.md` imports | Fatal |
| Markdown format | Standard markdown | Info |
| Instruction clarity | Clear, actionable | Warning |
| File length | ≤2000 lines recommended | Warning |

### Import Syntax

```markdown
@./shared-rules.md
@../common/context.md
```

### Commands Reference

- `/memory show` - displays full concatenated context
- `/memory refresh` - reloads all context files
- `/memory add <text>` - appends to global GEMINI.md

### Should Flag

- Invalid import syntax
- Contradictory instructions across hierarchy levels
- Vague, non-actionable instructions

### Should NOT Flag

- Missing optional sections
- Style variations
- Reasonable instruction choices

---

## Common Issues

### All Memory Files

| Issue | Severity |
|-------|----------|
| Invalid import syntax | Fatal |
| Contradictory instructions | Severe |
| Instructions don't match scope | Warning |
| Vague instructions | Warning |
| File >2000 lines | Warning |
| File >3000 lines | Severe |

### Content Quality Checks

| Check | Good | Bad |
|-------|------|-----|
| Specificity | "Use 2-space indentation" | "Format code properly" |
| Actionability | "Run `npm test` before commit" | "Test your code" |
| Clarity | "TypeScript for new files" | "Use good practices" |

### Instruction Quality (LLM Best Practices)

> **Full LLM checks**: See `rules-universal.md` → LLM Prompting Best Practices
> **Detailed practices**: See `type-prompt.md` → LLM Prompting Best Practices

| Check | Requirement | Severity |
|-------|-------------|----------|
| Verbosity constraints | Explicit length limits for outputs | Warning |
| Scope boundaries | Clear "do not" constraints | Warning |
| Ambiguity handling | Instructions for unclear cases | Info |
| Conciseness | No AI-known explanations | Warning |
| Freedom level match | Constraints match task fragility | Warning |
| Specific instructions | Actionable, not vague | Warning |
| No contradictions | No conflicting rules | Severe |
| Tool preference | Prefer tools over internal knowledge (if tool-using) | Warning |
| Agentic updates | Brief updates at major phases (if agentic) | Warning |
| Long-context outline | For >10k tokens: outline, restatement | Warning |

### Best Practices

1. **Be specific**: Clear, actionable instructions
2. **Use bullet points**: Easy to scan
3. **Include commands**: Frequently used build/test/lint
4. **Document conventions**: Code style, naming
5. **Match scope**: Global rules in root, specific in subdirs
6. **Single source of truth**: No duplicated rules
7. **Appropriate freedom**: Guidelines for flexible tasks, strict rules for fragile ops
