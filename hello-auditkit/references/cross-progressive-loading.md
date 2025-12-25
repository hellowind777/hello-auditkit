# Progressive Loading Audit Rules

> **Applies to**: Skills, Plugins, Composite Systems
> **Execution Required**: Audit content placement at each level (L1-L4). Check for anti-patterns. Verify "when to read" guidance.

## Table of Contents

- [Overview](#overview)
- [Loading Level Model](#loading-level-model)
- [Content Placement Audit](#content-placement-audit)
- [Progressive Disclosure](#progressive-disclosure)
- [Reference File Audit](#reference-file-audit)
- [Anti-Patterns](#anti-patterns)
- [Output Format](#output-format)

---

## Overview

### Two Related Concepts

| Concept | Definition | Goal |
|---------|------------|------|
| **Progressive Loading** | Content loaded in stages | Minimize context usage |
| **Progressive Disclosure** | Info revealed gradually | Reduce cognitive load |

---

## Loading Level Model

### Standard Levels

| Level | Content | Load Timing | Cost | Limit |
|-------|---------|-------------|------|-------|
| **L1** | Metadata | Always | Permanent | ~100 words |
| **L2** | Main body | When triggered | Session | <500 lines |
| **L3** | References | On demand | Temporary | ≤500 lines/file |
| **L4** | Scripts | Runtime only | Zero | No limit |

### L1: Metadata (Always Loaded)

**Content that MUST be in L1:**
- Unique identifier (name)
- Trigger conditions (description)
- Essential routing keywords

**Content that MUST NOT be in L1:**
- Implementation details
- Full instructions
- Examples >1 sentence

### L2: Main Body (Trigger-Loaded)

**Content that belongs:**
- Core instructions and workflows
- Common case handling
- Primary output format
- Brief inline examples

**Content to move to L3:**
- Detailed tables (>20 rows)
- Extended examples (>10 lines)
- Domain-specific docs
- Edge case details
- Historical context

### L3: References (On-Demand)

**Content that belongs:**
- Detailed specifications
- Comprehensive examples
- Domain knowledge
- API documentation
- Lookup tables

**Content that should NOT be here:**
- Core workflow (needed every time)
- Critical constraints
- Primary output format

### L4: Scripts (Runtime-Only)

- Never loaded into AI context
- Executed at runtime
- **No size limits**

---

## Content Placement Audit

### Step 1: Inventory by Level

```markdown
## Content Level Inventory

| Level | Location | Content | Lines |
|-------|----------|---------|-------|
| L1 | frontmatter | name, desc | X |
| L2 | SKILL.md body | [sections] | Y |
| L3 | references/*.md | [files] | Z |
| L4 | scripts/*.py | [scripts] | W |
```

### Step 2: Identify Misplacement

#### L1 Bloat Detection

| Issue | Detection | Severity |
|-------|-----------|----------|
| Description >500 chars | Character count | Warning |
| Implementation in description | Contains workflow | Warning |
| Examples in description | Code blocks | Warning |
| Redundant keywords | Repeated concepts | Info |

#### L2 Overload Detection

| Issue | Detection | Severity |
|-------|-----------|----------|
| Body >500 lines | Line count | Warning (>625: Severe) |
| Large inline tables | >20 rows | Warning |
| Extended examples | >10 lines each | Info |
| Edge-case-only content | Conditional use | Warning |
| Duplicated from L3 | Same content | Warning |

#### L3 Misuse Detection

| Issue | Detection | Severity |
|-------|-----------|----------|
| Core workflow in L3 | Should be L2 | Severe |
| No "when to read" | Missing guidance | Warning |
| Reference never needed | No use case | Info |
| Reference always needed | Should be L2 | Warning |

### Step 3: Calculate Efficiency

```markdown
## Loading Efficiency

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| L1 size | X words | ≤100 | ✅/⚠️/❌ |
| L2 size | Y lines | ≤500 | ✅/⚠️/❌ |
| L3 size | Z lines | ≤500/file | ✅/⚠️ |
| "Always needed" in L3 | N files | 0 | ⚠️ if >0 |
```

---

## Progressive Disclosure

### Disclosure Layers

| Layer | What User Sees | When |
|-------|----------------|------|
| **Surface** | Basic usage | First interaction |
| **Standard** | Full features | Regular use |
| **Advanced** | Edge cases, config | Expert use |

### Surface Layer Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Simple usage works | Sensible defaults | Severe |
| Basic example provided | Early in content | Warning |
| No mandatory complex setup | Can start immediately | Warning |

### Standard Layer Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Options documented | All configurable behaviors | Warning |
| Options have defaults | No mandatory decisions | Info |
| Common workflows covered | 80% use cases in body | Warning |

### Advanced Layer Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Advanced separated | In references or marked | Info |
| Expert options documented | For customization | Info |
| Edge cases in references | Not cluttering main | Info |

---

## Reference File Audit

### "When to Read" Requirements

Every reference MUST have loading guidance in SKILL.md:

**Good:**
```markdown
## Reference Files

Read `references/api-spec.md` when:
- User asks about API endpoints
- Generating API code
- Debugging API errors
```

**Bad:**
```markdown
See references/ for more information.
```

### Reference Checklist

| Check | Requirement | Severity |
|-------|-------------|----------|
| Has "when to read" | In SKILL.md | Warning |
| Conditions specific | Not just "when needed" | Info |
| Conditions detectable | AI can recognize | Warning |
| Not always needed | Should be in L2 | Warning |
| Not never needed | Remove or justify | Info |

### Loading Patterns

| Pattern | Description | Status |
|---------|-------------|--------|
| **Conditional** | Load for specific scenarios | ✅ Correct |
| **Always** | Load every time | ❌ Move to L2 |
| **Never** | Never actually used | ❌ Remove |
| **Cascading** | A says load B | ⚠️ Avoid depth |

---

## Anti-Patterns

### 1. Metadata Bloat

```yaml
# BAD
description: |
  This skill helps with X. When triggered:
  1. First analyze input
  2. Process according to rules
  Example: input "foo" produces "bar"

# GOOD
description: Use when user asks to "do X" or mentions "keyword Y".
```

**Detection**: Description >300 chars with workflow/code

### 2. Monolithic Body

```markdown
# BAD - 800+ line SKILL.md
## Core (50 lines)
## API Reference (200 lines)  ← Should be L3
## Error Codes (150 lines)    ← Should be L3
## Examples (100 lines)       ← Should be L3
```

**Detection**: Body >500 lines with separable sections

### 3. Essential Content in L3

```markdown
# BAD
## Overview
This skill processes data. See `references/workflow.md` for how.
```

**Detection**: Main body lacks workflow; references always needed

### 4. Orphan References

```
references/
├── spec-v1.md      # No mention in SKILL.md
├── old-format.md   # No mention
└── maybe-useful.md # No mention
```

**Detection**: Reference not mentioned with "when to read"

### 5. Reference Cascade

```markdown
# references/main.md
For details, see `sub-spec.md`.

# references/sub-spec.md
For implementation, see `impl-notes.md`.
```

**Detection**: References with internal cross-references; depth >1

### 6. Inverted Disclosure

```markdown
# BAD order
## Advanced Configuration   ← Expert first
## Performance Tuning
## Basic Usage             ← Basics buried!
```

**Detection**: "basic/simple" sections after "advanced/expert"

---

## Output Format

### Progressive Loading Section

```markdown
## Progressive Loading Analysis

### Content Level Distribution
| Level | Location | Size | Target | Status |
|-------|----------|------|--------|--------|
| L1 | frontmatter | X words | ≤100 | ✅/⚠️ |
| L2 | SKILL.md | Y lines | ≤500 | ✅/⚠️ |
| L3 | references/ | Z lines | ≤500/file | ✅/⚠️ |
| L4 | scripts/ | W lines | No limit | ✅ |

### Loading Efficiency
**Overall**: [Good/Acceptable/Needs Optimization]

| Metric | Status |
|--------|--------|
| L1 Minimality | ✅/⚠️ |
| L2 Self-Sufficiency | ✅/⚠️ |
| L3 Conditionality | ✅/⚠️ |
| Disclosure Order | ✅/⚠️ |

### Content Placement Issues
| Content | Current | Recommended | Reason | Severity |
|---------|---------|-------------|--------|----------|
| [X] | L2 | L3 | Edge case only | Warning |
| [Y] | L3 | L2 | Needed every time | Severe |

### Reference Loading Guidance
| File | Has "When to Read" | Specific | Status |
|------|-------------------|----------|--------|
| api-spec.md | ✅ | ✅ | Good |
| error-codes.md | ❌ | - | Missing |

### Anti-Patterns Detected
| Pattern | Detected | Location | Severity |
|---------|----------|----------|----------|
| Metadata bloat | ✅/❌ | | Warning |
| Monolithic body | ✅/❌ | | Warning |
| Essential in L3 | ✅/❌ | | Severe |
| Orphan references | ✅/❌ | | Warning |

### Recommendations
1. [Priority 1]: [Most impactful]
2. [Priority 2]: [Second fix]
```

---

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| Core workflow in L3 | Severe |
| L1 >1000 chars | Severe |
| L2 >750 lines | Severe |
| L2 >625 lines | Warning |
| L2 >500 lines | Info |
| No "when to read" | Warning |
| Reference always needed | Warning |
| Reference never needed | Info |
| Inverted disclosure | Warning |
| Metadata 300-500 chars | Info |
| Metadata >500 chars | Warning |
