# Prompt Best Practices Reference

## Table of Contents

- [GPT-5.2 Prompting Guidelines](#gpt-52-prompting-guidelines)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Audit Checklist for Prompts](#audit-checklist-for-prompts)
- [AGENTS.md Best Practices](#agentsmd-best-practices)
- [CLAUDE.md Best Practices](#claudemd-best-practices)
- [Skill Best Practices](#skill-best-practices-unified-claude--codex)
- [Script Best Practices](#script-best-practices)

---

## GPT-5.2 Prompting Guidelines

> Source: OpenAI GPT-5.2 Prompting Guide

### Core Principles

1. **Explicit over implicit**: Articulate preferences clearly rather than relying on defaults
2. **Constraint-driven**: Use explicit scope, verbosity, and format constraints
3. **Verification-oriented**: Favor correctness and grounding; add self-check steps for high-risk outputs
4. **Minimal interpretation**: "If any instruction is ambiguous, choose the simplest valid interpretation"

### Verbosity Control

| Context | Constraint |
|---------|------------|
| Simple yes/no questions | ≤2 sentences |
| Default responses | 3-6 sentences or ≤5 bullets |
| Complex tasks | 1 overview paragraph + ≤5 tagged bullets (What changed, Where, Risks, Next steps, Open questions) |

### Scope Discipline

Prevent feature creep with explicit boundaries:
- "Implement EXACTLY and ONLY what the user requests"
- "No extra features, no added components, no UX embellishments"
- Forbid inventing colors, animations, or UI elements unless requested

### Long-Context Handling (>10k tokens)

1. Produce internal outline of relevant sections first
2. Re-state user constraints before answering
3. Anchor claims to specific sections with quotes/paraphrases

### Ambiguity & Hallucination Prevention

- Ask 1-3 clarifying questions OR present 2-3 interpretations with labeled assumptions
- Use hedging language: "Based on the provided context..." instead of absolutes
- Never fabricate exact figures or references when uncertain
- Set missing fields to null rather than guessing
- Re-scan source before returning for missed fields

### Tool Usage Best Practices

- "Prefer tools over internal knowledge" for fresh/user-specific data
- Parallelize independent reads to reduce latency
- After write operations, restate: what changed, where, and validation performed

### Agentic Updates

- Send brief updates (1-2 sentences) only at major phases or plan changes
- Avoid narrating routine tool calls
- Each update must include concrete outcomes

### Structured Extraction

- Always provide schema/JSON shape
- Distinguish required vs optional fields
- Set missing fields to null rather than guessing

---

## Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|-----------------|
| Leaving verbosity unspecified | Add explicit length constraints |
| Allowing scope expansion | Add "no extra features" constraints |
| Generic tool descriptions | 1-2 sentences: what it does + when to use |
| Narrating every tool call | Update only at milestones with outcomes |
| Guessing missing data | Return null, state uncertainty explicitly |
| Absolute claims without grounding | Qualify with "based on provided context" |

---

## Audit Checklist for Prompts

### Fatal Issues
- [ ] Contradictory instructions
- [ ] Impossible constraints
- [ ] Missing critical context

### Severe Issues
- [ ] No verbosity constraints
- [ ] No scope boundaries
- [ ] Ambiguous output format
- [ ] No error handling instructions

### Warnings
- [ ] Vague instructions ("do it well")
- [ ] Missing examples for complex tasks
- [ ] No hedging guidance for uncertain cases
- [ ] Overly long without structure

### Info/Suggestions
- [ ] Could benefit from examples
- [ ] Could add self-check steps
- [ ] Could specify output structure more precisely

---

## AGENTS.md Best Practices

### Merge Hierarchy

AGENTS.md files merge top-down:
1. `~/.codex/AGENTS.md` - personal global guidance
2. `AGENTS.md` at repo root - shared project notes
3. `AGENTS.md` in current working directory - sub-folder specifics

### Content Guidelines

- Use bullet points for clear instructions
- Keep instructions actionable and specific
- Avoid contradictions across hierarchy levels
- Match instruction scope to file location

### Example Structure

```markdown
# Project Guidelines

- Always use TypeScript for new files
- Run tests before committing
- Follow existing code style

# API Guidelines

- Use REST conventions
- Include error handling
- Document all endpoints
```

---

## CLAUDE.md Best Practices

### Memory Types

| Type | Location | Purpose |
|------|----------|---------|
| Enterprise policy | System paths | Organization-wide |
| Project memory | `./CLAUDE.md` | Team-shared |
| Project rules | `./.claude/rules/*.md` | Modular rules |
| User memory | `~/.claude/CLAUDE.md` | Personal |
| Project local | `./CLAUDE.local.md` | Personal, gitignored |

### Import Syntax

Use `@path/to/file` to import other files:
- Supports relative and absolute paths
- Max depth of 5 hops
- Example: `@./shared-rules.md`

### Path-Specific Rules

Use YAML frontmatter with `paths` field:
```markdown
---
paths: src/api/**/*.ts
---
# API Rules
- All endpoints must include input validation
```

### Content Guidelines

- Be specific: "Use 2-space indentation" beats "Format code properly"
- Use bullet points and markdown headings
- Include frequently used commands (build, test, lint)
- Document code style preferences and naming conventions

---

## Skill Best Practices (Unified Claude + Codex)

### SKILL.md Structure

```yaml
---
name: skill-name
description: What this skill does AND when to use it
allowed-tools: Read, Grep, Glob  # Optional
---

# Skill Name

## Instructions
Clear, step-by-step guidance.

## Examples
Concrete usage examples.
```

### Field Requirements

| Field | Requirement |
|-------|-------------|
| name | ≤64 chars, lowercase letters, numbers, hyphens only |
| description | ≤1024 chars (≤500 recommended), must include trigger conditions |
| allowed-tools | Optional, comma-separated valid tool names |

### Description Best Practices

Include trigger terms:
- Good: "Analyze Excel spreadsheets, create pivot tables. Use when working with Excel files, spreadsheets, or .xlsx format."
- Bad: "Helps with spreadsheets"

### Body Guidelines

- Keep focused on one capability
- ≤500 lines, <5k words ideal; >750 lines needs work
- Reference supporting files for progressive loading
- Document version history

---

## Script Best Practices

### Shell Scripts

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Error handling
trap 'echo "Error on line $LINENO"' ERR

# Main logic here
```

### Python Scripts

```python
#!/usr/bin/env python3
"""Script description."""

import sys

def main():
    try:
        # Main logic
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Checklist

- [ ] Proper shebang line
- [ ] Error handling (set -e or try/except)
- [ ] Clear exit codes
- [ ] Input validation
- [ ] Helpful error messages
