# Memory File Audit Rules

## Table of Contents

- [Important: Content-Based Audit](#important-content-based-audit)
- [Prompts Audit](#prompts-audit)
- [AGENTS.md Audit](#agentsmd-audit)
- [CLAUDE.md Audit](#claudemd-audit)
- [GEMINI.md Audit](#geminimd-audit)

---

## Important: Content-Based Audit

Audit is based on the **content** user provides, NOT limited to specific system paths. User may:
- Provide files copied to any location for review
- Paste content directly
- Point to any directory structure

Focus on auditing **content quality** itself. Path/location checks are **informational only** (marked as "Info (advisory)") - they help understand intended usage but should not fail the audit if content is in a non-standard location.

---

## Prompts Audit

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Verbosity constraints | Explicit length limits specified | Warning |
| Scope boundaries | Clear "do not" constraints | Warning |
| Ambiguity handling | Instructions for unclear cases | Info |
| Output format | Specified structure/format | Warning |
| Grounding | "Based on context" hedging for uncertain claims | Info |

### Content Quality

**Good prompt patterns:**
- Explicit constraints: "Respond in ≤3 sentences"
- Scope limits: "Only address the specific question asked"
- Ambiguity handling: "If unclear, ask 1-2 clarifying questions"
- Output format: "Return as JSON with fields: x, y, z"

**Bad prompt patterns:**
- Vague instructions: "Do it well"
- No length constraints
- No scope boundaries
- Absolute claims without grounding

### Common Prompt Issues

**Should Flag:**
- No verbosity constraints for open-ended tasks
- No scope boundaries allowing feature creep
- Missing output format for structured tasks
- Absolute claims without hedging
- Contradictory instructions

**Should NOT Flag:**
- Simple prompts that don't need constraints
- Style preferences
- Reasonable interpretation choices

---

## AGENTS.md Audit

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct hierarchy level | Info |
| Merge awareness | No conflicts with parent AGENTS.md | Severe |
| Instruction clarity | Clear, actionable instructions | Warning |
| Scope appropriateness | Instructions match file location | Warning |
| File length | ≤2000 lines recommended, ≤3000 lines limit | Warning/Severe |

### Merge Hierarchy

AGENTS.md files merge top-down:
1. `~/.codex/AGENTS.md` - personal global
2. `AGENTS.md` at repo root - project-wide
3. `AGENTS.md` in cwd - folder-specific

### Content Quality

**Good AGENTS.md patterns:**
```markdown
- Always use TypeScript for new files
- Run `npm test` before committing
- Follow existing code style in the project
```

**Bad AGENTS.md patterns:**
```markdown
- Be helpful (too vague)
- Do everything correctly (not actionable)
```

### Common AGENTS.md Issues

**Should Flag:**
- Contradictory instructions across hierarchy levels
- Vague, non-actionable instructions
- Instructions that don't match file scope
- Missing critical project-specific guidance

**Should NOT Flag:**
- Simple bullet-point format
- Reasonable instruction variations
- Optional guidance not present

---

## CLAUDE.md Audit

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct for memory type | Info (advisory) |
| Import syntax | Valid `@path/to/file` | Fatal |
| Path-specific rules | Valid YAML frontmatter | Severe |
| Format | Bullet points and markdown headings | Info |
| File length | ≤2000 lines recommended, ≤3000 lines limit | Warning/Severe |

### Memory Type Locations

| Type | Location |
|------|----------|
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Project rules | `./.claude/rules/*.md` |
| User memory | `~/.claude/CLAUDE.md` |
| Project local | `./CLAUDE.local.md` |

### Import Syntax

Valid: `@./shared-rules.md`, `@../common/rules.md`
Invalid: `@rules.md` (missing path prefix)

### Path-Specific Rules

```markdown
---
paths: src/api/**/*.ts
---
# API Rules
- All endpoints must include input validation
```

### Common CLAUDE.md Issues

**Should Flag:**
- Invalid import syntax
- File in wrong location for memory type
- Invalid YAML frontmatter for path-specific rules
- Vague instructions ("format code properly")

**Should NOT Flag:**
- Missing optional sections
- Style variations
- Reasonable instruction choices

---

## GEMINI.md Audit

> Source: Gemini CLI official documentation

### What It Is

GEMINI.md files provide instructional context to the Gemini model for project-specific instructions, personas, or coding style guides.

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File location | Correct hierarchy level | Info (advisory) |
| Import syntax | Valid `@file.md` imports | Fatal |
| Markdown format | Standard markdown | Info |
| Instruction clarity | Clear, actionable | Warning |
| File length | ≤2000 lines recommended, ≤3000 lines limit | Warning/Severe |

### File Location Hierarchy

Files are loaded and concatenated in this order:
1. **Global**: `~/.gemini/GEMINI.md` - default for all projects
2. **Project root/ancestors**: Up to `.git` folder
3. **Subdirectories**: Below current directory (respects `.gitignore`, `.geminiignore`)

### Import Syntax

Use `@file.md` to import other files:
- Supports relative and absolute paths
- Example: `@./shared-rules.md`, `@../common/context.md`

### Commands Reference

- `/memory show` - displays full concatenated context
- `/memory refresh` - reloads all context files
- `/memory add <text>` - appends to global GEMINI.md

### Common GEMINI.md Issues

**Should Flag:**
- Invalid import syntax
- Contradictory instructions across hierarchy levels
- Vague, non-actionable instructions

**Should NOT Flag:**
- Missing optional sections
- Style variations
- Reasonable instruction choices
