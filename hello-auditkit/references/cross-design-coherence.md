# Design Coherence Audit Rules

> **Applies to**: Multi-file systems (Skills, Plugins, Composite Systems)
> **Execution Required**: Execute FULL directory scan. Extract ALL rules from ALL files. Detect conflicts and red flags.

## Table of Contents

- [Overview](#overview)
- [Full Directory Scanning](#full-directory-scanning)
- [Design Philosophy Extraction](#design-philosophy-extraction)
- [Rule Inventory](#rule-inventory)
- [Cross-File Coherence](#cross-file-coherence)
- [Conflict Detection](#conflict-detection)
- [Framework Assessment](#framework-assessment)
- [Output Format](#output-format)

---

## Overview

**Design Coherence Audit** analyzes the entire directory structure to:

1. **Extract** all design intents, rules, and specifications
2. **Verify** consistency across all files
3. **Detect** conflicts and contradictions
4. **Assess** overall framework quality

---

## Full Directory Scanning

### Step 0: Complete Enumeration

**CRITICAL: Scan ALL files, not just entry points.**

Recursively enumerate, classify, read, and build complete rule inventory.

### File Classification

| Type | Role | What to Extract |
|------|------|-----------------|
| `SKILL.md` | Primary | Purpose, principles, rules |
| `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` | Memory | Global rules, conventions |
| `plugin.json` | Manifest | Declared capabilities |
| `references/*.md` | Supporting | Detailed rules, specs |
| `commands/*.md` | Commands | Per-command rules |
| `agents/*.md` | Agents | Per-agent rules |
| `*.py`, `*.sh` | Scripts | Implemented behaviors |
| `*.json`, `*.yaml` | Configs | Configuration constraints |

### Scan Output

```markdown
## Directory Scan

| File | Type | Rules | Constraints |
|------|------|-------|-------------|
| SKILL.md | Primary | 12 | 8 |
| references/spec.md | Reference | 25 | 15 |
| ... | ... | ... | ... |

**Total**: N files, M rules, K constraints
```

---

## Design Philosophy Extraction

### Per-File Extraction

| Element | Source Patterns | Priority |
|---------|-----------------|----------|
| Primary purpose | description, Overview | Highest |
| Core principles | "Principle:", numbered lists | High |
| Explicit constraints | MUST, MUST NOT, ALWAYS, NEVER | High |
| Implicit values | Repeated patterns, emphasis | Medium |
| Assumptions | "assumes", "expects" | Medium |

### Aggregation

```markdown
## Aggregated Design Philosophy

### From Primary Files
- Purpose: [Synthesized]
- Principles: [List]

### From References
- Additional principles: [List]
- Detailed constraints: [List]

### Synthesized Core Philosophy
1. [Principle 1] - appears in N files
2. [Principle 2] - appears in M files
```

### Consistency Check

| Check | Question | Severity |
|-------|----------|----------|
| Purpose alignment | All files serve stated purpose? | Severe |
| Principle coverage | Principles mentioned consistently? | Warning |
| Constraint consistency | Same constraints in relevant files? | Warning |
| Value alignment | Shared implicit values? | Info |

---

## Rule Inventory

### Complete Extraction

**Extract ALL rules from ALL files.**

### Rule Categories

| Category | Examples | Source Patterns |
|----------|----------|-----------------|
| **Behavioral** | "When X, do Y" | Conditionals |
| **Constraint** | "MUST/MUST NOT" | Modal verbs |
| **Format** | "Output must be JSON" | Format specs |
| **Process** | "First X, then Y" | Sequential |
| **Validation** | "Check that X" | Validation |
| **Exception** | "Unless X, then Y" | Exception clauses |

### Inventory Format

```markdown
## Rule Inventory

### Behavioral Rules (N total)
| ID | Rule | Source | Line |
|----|------|--------|------|
| R1 | "When user asks X..." | SKILL.md | 45 |

### Constraint Rules (N total)
| ID | Constraint | Type | Source |
|----|------------|------|--------|
| C1 | "MUST validate" | MUST | SKILL.md:67 |
```

---

## Cross-File Coherence

### Rule Propagation Check

```
For each rule R from file F:
  1. Identify files where R should apply
  2. Check if R mentioned/followed in those files
  3. Check for contradictions
  4. Report gaps and conflicts
```

### Propagation Matrix

```markdown
## Rule Propagation

| Rule | Origin | Should Apply | Applied In | Gap |
|------|--------|--------------|------------|-----|
| "Validate input" | SKILL.md | All cmds | cmd1, cmd2 | cmd3 ❌ |
| "JSON output" | SKILL.md | All | All | ✅ |
```

### Cross-Reference Verification

| Check | Description | Severity |
|-------|-------------|----------|
| Rule in docs, not in code | Mentioned but not implemented | Warning |
| Rule in code, not in docs | Implemented but undocumented | Info |
| Conflicting rules | File A says X, File B says NOT X | Severe |
| Rule scope mismatch | Global rule not applied locally | Warning |

### Constraint Inheritance

```markdown
## Constraint Inheritance

| Global Constraint | Local Files | Status |
|-------------------|-------------|--------|
| "MUST use kebab-case" | commands/*.md | ✅ All compliant |
| "NEVER hardcode paths" | scripts/*.py | ⚠️ script2.py violates |
```

### Structural Redundancy Detection

| Check | Description | Severity |
|-------|-------------|----------|
| Repeated sections | Same section structure in multiple files → centralize | Warning |
| Duplicate tables | Identical tables → move to shared reference | Warning |
| Parallel content | Same info in different formats → keep one | Warning |

---

## Conflict Detection

### Conflict Categories

#### Category A: Same-File Contradictions

```markdown
File: SKILL.md
  Line 45: "MUST include detailed error messages"
  Line 123: "MUST NOT expose error details"
Conflict: Direct contradiction
Severity: Severe
```

#### Category B: Cross-File Contradictions

```markdown
File A (SKILL.md:45): "Output MUST be JSON"
File B (cmd/run.md:23): "Output as plain text"
Conflict: Command contradicts skill rule
Severity: Severe
```

#### Category C: Principle-Rule Conflicts

```markdown
Principle (SKILL.md): "Keep it simple"
Rule (spec.md:89): "Include full audit trail in every response"
Conflict: Rule contradicts principle
Severity: Warning
```

#### Category D: Implicit-Explicit Conflicts

```markdown
Implicit (description): "Fast, lightweight"
Explicit (spec.md): "Run 30+ validation checks"
Conflict: Explicit contradicts implicit
Severity: Warning
```

### Detection Algorithm

For each rule pair: check domain overlap → verify logical/constraint/value consistency → flag conflicts with locations.

---

## Framework Assessment

### Structural Design

| Check | Question | If Failed |
|-------|----------|-----------|
| Separation of concerns | Responsibilities separated? | Suggest splitting |
| Single responsibility | Each file has one purpose? | Suggest refactoring |
| Appropriate abstraction | Right level? | Suggest changes |
| Modularity | Independent components? | Suggest decoupling |

### Red Flags

| Red Flag | Indicator | Severity | Suggestion |
|----------|-----------|----------|------------|
| God file | SKILL.md >625 lines, multiple concerns | Warning | Split by responsibility |
| Scattered rules | Same rule in >3 files | Warning | Centralize |
| Orphan components | Files not referenced | Info | Remove or integrate |
| Circular deps | A→B→C→A | Severe | Break cycle |
| Implicit contracts | Undocumented assumptions | Warning | Document explicitly |
| Missing error handling | No error rules | Warning | Add error section |

### Industry Patterns

| Pattern | When to Suggest |
|---------|-----------------|
| Layered architecture | Mixed concerns detected |
| Convention over config | Too much required config |
| Composition over inheritance | Monolithic components |
| Explicit over implicit | Hidden assumptions |
| Progressive disclosure | Information overload |

---

## Output Format

### Design Coherence Section

```markdown
## Design Coherence Analysis

### Directory Scan Summary
| Metric | Value |
|--------|-------|
| Files scanned | N |
| Rules extracted | M |
| Constraints found | K |

### Aggregated Philosophy
**Purpose**: [Synthesized]
**Principles** (by frequency):
1. [P1] - N files
2. [P2] - M files

### Cross-File Coherence

#### Rule Propagation
| Status | Count |
|--------|-------|
| ✅ Fully propagated | N |
| ⚠️ Partial gaps | M |
| ❌ Major gaps | K |

#### Conflicts Detected
| Type | Count | Severity |
|------|-------|----------|
| Direct contradictions | N | Severe |
| Cross-file conflicts | M | Severe |
| Principle-rule conflicts | K | Warning |

### Framework Assessment
**Quality**: [Good/Acceptable/Needs Improvement]

| Aspect | Status |
|--------|--------|
| Separation of concerns | ✅/⚠️/❌ |
| Single responsibility | ✅/⚠️/❌ |
| Modularity | ✅/⚠️/❌ |

### Red Flags
| Flag | Location | Severity |
|------|----------|----------|
| [Flag] | [File] | [Level] |

### Recommendations
1. **Priority 1**: [Most critical]
2. **Priority 2**: [Second]
```

---

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| Cross-file rule contradiction | Severe |
| Core principle violated | Severe |
| Rule not propagated | Warning |
| Framework red flag | Warning |
| Implicit-explicit conflict | Warning |
| Missing documentation | Info |
| Suboptimal pattern | Info |

---

## Should NOT Flag

- Different detail levels (summary vs detailed)
- Scoped rule overrides with justification
- Progressive disclosure patterns
- Platform-specific variations (documented)
- Intentional design choices (with rationale)
- Minor style variations
