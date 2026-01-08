# Quick Reference

> **Purpose**: Condensed lookup of key information. For full details, see referenced source files.

## Content Type Identification

| Identifier | Type | Audit Rule File |
|------------|------|-----------------|
| Single prompt/text | Prompt | `type-prompt.md` |
| `AGENTS.md` file | Memory (Codex) | `type-memory.md` |
| `CLAUDE.md` file | Memory (Claude) | `type-memory.md` |
| `GEMINI.md` file | Memory (Gemini) | `type-memory.md` |
| Directory with `SKILL.md` | Skill | `type-skill.md` |
| Directory with `.claude-plugin/` | Plugin | `type-plugin.md` |
| Memory file + skills/ | Composite | `cross-composite.md` |

---

## Severity Quick Guide

| Severity | Threshold | Action |
|----------|-----------|--------|
| **Fatal** | Cannot execute | Must fix |
| **Severe** | ≥60% errors | Should fix |
| **Warning** | ≥40% misunderstand | Consider |
| **Info** | Suggestion | Optional |
| **NOT issue** | ≤10% over limit | Ignore |

---

## Size Limits

| Content | Limit | Tolerance |
|---------|-------|-----------|
| L1 Metadata | ~100 words | - |
| L2 Body | 500 lines | +10% OK |
| L3 Reference | **No official limit** | Evaluate by content |
| L4 Scripts | **No limit** | - |
| Memory files | 2000 lines | 3000 max |

### Tiered Thresholds (SKILL.md body only)

```
≤500     → Ideal
500-550  → OK (NOT an issue)
550-625  → Info only
>625     → Warning
```

---

## 4-Point Verification

```
Issue Detected
    ↓
1. Concrete Scenario? → NO → Discard
    ↓ YES
2. In Design Scope? → NO → Discard
    ↓ YES
3. Flaw or Choice? → Choice → Discard
    ↓ Flaw
4. Meets Threshold? → NO → Discard
    ↓ YES
Mark as Issue
```

---

## Fix Priority

```
1. DELETE     ← Preferred
2. MERGE
3. RESTRUCTURE
4. MODIFY
5. ADD        ← Last Resort
```

---

## Loading Levels

| Level | Content | Timing | Limit |
|-------|---------|--------|-------|
| L1 | Metadata | Always | ~100 words |
| L2 | Body | Triggered | <500 lines |
| L3 | References | On demand | No official limit |
| L4 | Scripts | Runtime | No limit |

---

## Common Patterns

### Valid Tool Names

```yaml
# Single
allowed-tools: Read

# Multiple (string)
allowed-tools: Read, Write, Edit

# Multiple (array)
allowed-tools: [Read, Write, Bash(git:*)]

# MCP
allowed-tools: ["mcp__server__tool"]
```

### Path Variables

| Variable | Use |
|----------|-----|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin paths |
| `${CLAUDE_PROJECT_DIR}` | Project root |

### Hook Wrapper (Plugin)

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

---

## AI Capability Model

### AI CAN Infer

- Common synonyms
- Standard terminology
- Conventional patterns
- JSON, markdown syntax
- Error handling patterns

### AI CANNOT Infer

- 3+ step inference chains
- Domain-specific terms
- Project conventions
- Counter-intuitive requirements

---

## Should NOT Flag

| Category | Examples |
|----------|----------|
| **Size** | ≤10% over limit |
| **License** | Copyright notices |
| **Design** | Valid alternatives |
| **AI knows** | Standard concepts |
| **Optional** | Missing optional fields |

---

## Key File Requirements

### SKILL.md

```yaml
---
name: required, ≤64 chars
description: required, include triggers
---
```

### plugin.json

```json
{
  "name": "required-kebab-case"
}
```

### hooks.json (Plugin)

```json
{
  "hooks": { ... }
}
```

---

## BCP 47 Language Tags

| Correct | Incorrect |
|---------|-----------|
| `en-US` | `en`, `english` |
| `zh-CN` | `zh`, `chinese` |
| `zh-TW` | `zh-tw` |
| `ja-JP` | `ja`, `japanese` |

---

## Reference Documentation

### Official Sources

| Platform | Repository |
|----------|------------|
| Claude Code | github.com/anthropics/claude-code |
| Codex CLI | github.com/openai/codex/tree/main/codex-cli |
| Gemini CLI | github.com/google-gemini/gemini-cli |

### Documentation

| Resource | URL |
|----------|-----|
| Claude Code Docs | docs.anthropic.com/en/docs/claude-code |
| OpenAI Cookbook | github.com/openai/openai-cookbook |
| Google AI | ai.google.dev/docs |
