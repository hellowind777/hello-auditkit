# Composite System Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Requires**: Type-specific rules from `type-*.md`
> **Execution Required**: Execute each check table below. Verify cross-component references, terminology consistency, rule layering, and script integrity.

## Table of Contents

- [Overview](#overview)
- [Composite Types](#composite-types)
- [Cross-Component Consistency](#cross-component-consistency)
- [Reference Integrity](#reference-integrity)
- [Rule Layering](#rule-layering)
- [Coverage Scan](#coverage-scan)
- [Script Quality](#script-quality)
- [Design Requirements Review](#design-requirements-review)
- [Common Issues](#common-issues)

---

## Overview

**Composite systems** combine multiple components that must work together cohesively.

### Audit Approach

```
Composite System Audit Flow:

1. Identify Components
   ├── Memory file (AGENTS.md/CLAUDE.md/GEMINI.md)
   ├── Skills (find all SKILL.md)
   ├── Plugin structure (.claude-plugin/)
   └── Other components (scripts, hooks, etc.)

2. Individual Audits
   └── Apply type-specific rules to each component

3. Cross-Cutting Audits (THIS FILE)
   ├── Reference integrity
   ├── Terminology consistency
   ├── Rule layering
   └── Coverage verification

4. Integration Verification
   └── Components work together without conflicts
```

---

## Composite Types

| Type | Components | Entry Point |
|------|------------|-------------|
| **Claude Composite** | CLAUDE.md + skills/ | CLAUDE.md |
| **Codex Composite** | AGENTS.md + skills/ | AGENTS.md |
| **Gemini Composite** | GEMINI.md + skills/ | GEMINI.md |
| **Plugin Composite** | .claude-plugin/ + all components | plugin.json |
| **Multi-Memory** | Multiple memory files + skills | Most specific |

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Memory file exists | At least one memory file | Severe |
| skills/ directory | Contains valid SKILL.md files | Severe |
| Script references | All referenced scripts exist | Fatal |
| Directory structure | Logical organization | Warning |

### Main Rule File Structure (AGENTS.md/CLAUDE.md)

| Check | Requirement | Severity |
|-------|-------------|----------|
| Bootstrap comments | lang, encoding, version, architecture | Info |
| Core sections present | Global rules, routing, phase skeleton | Severe |
| Section order | Logical flow (global → routing → phases) | Warning |
| Skills reference table | Complete and accurate | Severe |

**Core Sections for Main Rule File:**

| Section | Purpose | Required |
|---------|---------|----------|
| Global Rules | Apply to all phases | Yes |
| Routing Mechanism | Path decision logic | Yes (if multi-path) |
| Phase Skeleton | High-level phase flow | Yes |
| Skills Reference Table | List all skill references | Recommended |
| Auxiliary Scripts | Runtime dependencies | If scripts exist |

---

## Cross-Component Consistency

### Reference Validation

**Check all cross-references:**

| Reference Type | Check | Severity |
|----------------|-------|----------|
| Memory → Skill | Referenced skills exist | Severe |
| Skill → Skill | Inter-skill references valid | Warning |
| Agent → Skill | Referenced skills exist | Severe |
| Hook → Script | Referenced scripts exist | Fatal |
| Any → File | File references exist | Severe |

### Terminology Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Same concept = same term | Across all files | Warning |
| Component names match refs | Names consistent | Warning |
| No conflicting terminology | Without explanation | Warning |

**Example:**
```
Memory file: "task processing"
Skill A: "job handling"      ← Warning: inconsistent
Skill B: "task processing"   ← OK: consistent
```

### Naming Conventions

| Check | Requirement | Severity |
|-------|-------------|----------|
| Consistent numbering | R1/R2/R3 or 1.1/1.2/1.3 | Warning |
| No numbering gaps | Sequential | Warning |
| Format consistency | Same format across files | Warning |

### Output Format Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Format defined centrally | One source of truth | Warning |
| Components follow format | Consistent application | Warning |
| Format documented | Clear specification | Info |

---

## Reference Integrity

### Existence Checks

| Referenced Item | Must Exist | Severity |
|-----------------|------------|----------|
| Skills in memory file | Yes | Severe |
| Scripts in hooks | Yes | Fatal |
| Files in imports | Yes | Fatal |
| Agents in commands | Yes | Severe |

### Circular Dependency Detection

```
A → B → C → A  ← FATAL: Circular dependency
```

| Check | Requirement | Severity |
|-------|-------------|----------|
| No circular refs | A→B→C→A pattern | Fatal |
| Dependency graph acyclic | Can be topologically sorted | Fatal |

### Anchor/Link Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| #anchor links valid | Target exists | Severe |
| File references valid | Target file exists | Severe |
| Path format correct | Portable paths | Warning |

---

## Rule Layering

### Hierarchy Principle

```
Global Rules (Memory File)
    ↓ (inherited by)
Local Rules (Skills/Components)
    ↓ (can override with)
Component-Specific Rules
```

### Layering Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Global rules in memory file | Not scattered in skills | Warning |
| Local rules in components | Component-specific only | Warning |
| No misplaced rules | Rules at correct level | Warning |
| Override documented | If local overrides global | Info |

### Inheritance Verification

| Check | Requirement | Severity |
|-------|-------------|----------|
| Global inherited | Skills follow memory file rules | Warning |
| Conflicts resolved | No contradictory rules | Severe |
| Override explicit | Local override is intentional | Info |

---

## Coverage Scan

### Phase Implementation

For systems with defined phases:

| Check | Requirement | Severity |
|-------|-------------|----------|
| All phases implemented | Each phase has SKILL.md | Fatal |
| Key steps documented | Critical steps have rules | Severe |
| No orphan implementations | All skills referenced | Warning |

### Routing Path Verification

| Check | Requirement | Severity |
|-------|-------------|----------|
| All paths have rules | Each routing path covered | Fatal |
| No dead-end paths | All paths lead to endpoints | Fatal |
| Path conditions clear | Unambiguous routing | Severe |

### Capability Coverage

| Check | Requirement | Severity |
|-------|-------------|----------|
| Declared → Implemented | All declared capabilities exist | Severe |
| No orphan skills | All skills are reachable | Info |
| Triggers don't conflict | Skills have distinct triggers | Warning |

---

## Script Quality

> **Detailed steps**: See `type-skill.md` → Scripts Audit → Script Integrity Verification

**Applies to**: All scripts in composite system

### Script Integrity Checklist

| Check | Requirement | Severity |
|-------|-------------|----------|
| Declared scripts exist | All listed scripts present | Severe |
| Import targets exist | All imported modules present | Fatal |
| No circular imports | Acyclic dependency graph | Severe |
| Shebang present | `#!/bin/bash` or `#!/usr/bin/env python3` | Warning |
| Error handling | `set -euo pipefail` (bash) or try/except (python) | Warning |
| No hardcoded secrets | Use env variables | Severe |
| Path references | Use relative paths or env variables | Severe |
| External packages listed | In requirements.txt or docs | Warning |

### Script Type Classification

| Type | Purpose | Document? |
|------|---------|-----------|
| **Runtime** | Called during skill execution | Yes (required) |
| **Dev tools** | Development/debugging only | No |
| **Internal helpers** | Imported by other scripts | Optional |

### Function Merge Check

If declared script doesn't exist:
1. Read other scripts' source code
2. Check if function merged into another file
3. If merged → Document update needed, not missing issue
4. If truly missing → Severe issue

---

## Design Requirements Review

### When to Apply

**Optional add-on** when user provides design requirements with audit target.

### Gap Analysis

| Check | Assessment | Severity |
|-------|------------|----------|
| Core functionality | All features implemented? | Severe |
| Feature completeness | Partial vs full | Severe |
| Scope creep | Unintended features added? | Warning |
| Missing capabilities | Gaps vs intent | Severe |
| Over-engineering | More complex than needed? | Warning |

### Alignment Verification

For each design goal:
- Is there a corresponding component?
- Does it fully address the goal?
- Are there gaps between intent and implementation?
- Are there deviations from purpose?

### Trigger Condition Review

| Check | Requirement | Severity |
|-------|-------------|----------|
| Triggers match intent | Cover intended scenarios | Warning |
| No missing triggers | All scenarios covered | Warning |
| No unintended triggers | No false positives | Warning |

---

## Common Issues

### Should Flag

| Issue | Severity |
|-------|----------|
| Memory file contradicts skill | Severe |
| Referenced scripts don't exist | Fatal |
| Overlapping triggers without differentiation | Warning |
| Broken cross-file references | Severe |
| Inconsistent naming | Warning |
| Circular dependencies | Fatal |
| Global rule scattered in skills | Warning |
| Phase defined but not implemented | Fatal |
| Script without error handling | Warning |
| Import dependencies missing | Fatal |

### Should NOT Flag

| Pattern | Reason |
|---------|--------|
| Different detail levels | Normal variation |
| Reasonable organizational choices | Design choice |
| Style variations within components | Acceptable |
| Optional scripts not present | Optional |
| Different structure than examples | Valid if working |

---

## Audit Output Format

### Cross-Component Section

```markdown
## Cross-Component Analysis

### Reference Integrity
| Source | Target | Status |
|--------|--------|--------|
| CLAUDE.md:45 | skills/audit | ✅ Exists |
| skill-a → skill-b | Reference | ✅ Valid |

### Terminology Consistency
| Concept | Terms Used | Status |
|---------|------------|--------|
| Processing | task, job | ⚠️ Inconsistent |

### Rule Layering
| Rule | Location | Level | Status |
|------|----------|-------|--------|
| Output format | CLAUDE.md | Global | ✅ Correct |
| Validation | skill-a | Local | ✅ Correct |

### Coverage
| Capability | Declared | Implemented | Status |
|------------|----------|-------------|--------|
| Audit | Yes | Yes | ✅ Complete |
```
