# Cross-Audit Rules

## Table of Contents

- [Design Requirements Review](#design-requirements-review)
- [Cross-Component Consistency](#cross-component-consistency)
- [Coverage Scan](#coverage-scan)
- [Composite System Audit](#composite-system-audit)

---

## Design Requirements Review

### Overview

This is NOT a separate mode - it's an optional add-on that can be combined with ANY audit mode.

When user provides original design requirements or PRD document along with content to audit:
1. Perform standard audit based on detected content type
2. Additionally evaluate design alignment

**User provides:**
- Content to audit (any supported type)
- Design requirements (brief description, detailed paragraph, or formal PRD)

### Design-Implementation Gap Analysis

| Check Area | Assessment | Severity |
|------------|------------|----------|
| Core functionality coverage | All intended features implemented? | Severe |
| Feature completeness | Partial vs full implementation | Severe |
| Scope creep | Unintended features added? | Warning |
| Missing capabilities | Gaps vs original intent | Severe |
| Over-engineering | More complex than needed? | Warning |

### Intent Alignment Validation

**For each stated design goal, verify:**
- Is there a corresponding component?
- Does the component fully address the goal?
- Are there gaps between intent and implementation?
- Are there deviations from original purpose?

### Trigger Condition Review

**Check if triggers match design intent:**
- Do skill/agent descriptions trigger for intended scenarios?
- Are there scenarios that should trigger but won't?
- Are there unintended trigger scenarios?

### Common Design Alignment Issues

**Should Flag:**
- Core design goal has no implementation
- Implementation contradicts stated purpose
- Critical user workflow is broken
- Significant feature missing vs intent
- Trigger conditions don't match intended use cases

**Should NOT Flag:**
- Implementation details differ from vague requirements
- Additional helpful features beyond minimum
- Style/structure choices within design bounds
- Reasonable interpretation of ambiguous requirements

---

## Cross-Component Consistency

### Reference Validation

**Check all cross-references:**
- Agent references in commands exist
- Skill references in agents exist
- Script references in hooks exist
- File references in any component exist

### Naming Consistency

**Verify consistent naming:**
- Same concept uses same term across files
- Component names match their references
- No conflicting terminology

### Output Format Consistency

**If plugin defines output formats:**
- All components follow same format
- Format documented in one place
- Components reference central format definition

### Common Cross-Component Issues

**Should Flag:**
- Referenced component doesn't exist
- Same concept with different names (without explanation)
- Conflicting output formats
- Circular dependencies
- Missing dependencies

**Should NOT Flag:**
- Different detail levels in different components
- Reasonable terminology variations with context

---

## Coverage Scan

### Overview

Coverage scan verifies that all defined elements have corresponding implementations.

### Phase Implementation Verification

For composite systems with defined phases/stages:

| Check | Requirement | Severity |
|-------|-------------|----------|
| All phases have implementation | Each phase in skeleton has SKILL.md | Fatal |
| Key steps documented | Critical steps in phase have detailed rules | Severe |
| No orphan implementations | All SKILL.md files are referenced | Warning |

### Routing Path Verification

For systems with routing/decision logic:

| Check | Requirement | Severity |
|-------|-------------|----------|
| All paths have rules | Each routing path has implementation | Fatal |
| No dead-end paths | All paths lead to valid endpoints | Fatal |
| Path conditions clear | Routing conditions are unambiguous | Severe |

### Rule Layering Verification

| Check | Requirement | Severity |
|-------|-------------|----------|
| Global rules in global file | Rules for all phases in AGENTS.md/CLAUDE.md | Warning |
| Local rules in local files | Phase-specific rules in respective SKILL.md | Warning |
| No misplaced rules | Global rules not scattered in local files | Warning |
| Cross-file redundancy | Same rule not fully repeated in multiple files | Warning |

### Reference Completeness

| Check | Requirement | Severity |
|-------|-------------|----------|
| All references exist | Referenced skills/scripts/files exist | Severe |
| Reference timing clear | When to read each reference is specified | Warning |
| No missing references | Brief descriptions have detailed references | Severe |

### Common Coverage Issues

**Should Flag:**
- Phase defined in skeleton but no SKILL.md implementation
- Routing path with no execution rules
- Global rule scattered across multiple local files
- Brief description without reference to detailed rules
- Referenced file doesn't exist

**Should NOT Flag:**
- Optional phases not implemented (if marked optional)
- Simplified routing for simple systems
- Intentional rule repetition for readability

---

## Composite System Audit

### Overview

Composite systems combine multiple components:
- `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` - Top-level instructions
- `skills/` directory - Multiple skill definitions
- Scripts (`.sh`, `.py`, etc.) - Supporting automation
- `.claude-plugin/` - Plugin structure (optional)

### Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Memory file exists | AGENTS.md/CLAUDE.md/GEMINI.md at root | Severe |
| skills/ directory | Contains valid SKILL.md files | Severe |
| Script references | All referenced scripts exist | Fatal |
| Directory structure | Logical organization | Warning |

### Cross-Component Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Memory file ↔ skills | No conflicting instructions | Severe |
| Skill ↔ skill | No overlapping triggers without differentiation | Warning |
| Script references | Valid paths in all components | Fatal |
| Naming conventions | Consistent across all files | Warning |

### Memory File + Skills Integration

**Check for:**
- Memory file instructions align with skill purposes
- No contradictory guidance between memory file and skills
- Skills referenced in memory file actually exist
- Skill triggers don't conflict with memory file scope

### Memory File + Plugin Integration

**Check for:**
- Memory file doesn't duplicate plugin instructions
- No conflicts between memory file rules and plugin components
- Clear separation of concerns (global vs plugin-specific)

### Script Quality Audit

| Check | Requirement | Severity |
|-------|-------------|----------|
| Shebang line | Present and correct | Warning |
| Error handling | `set -e` or try/except | Warning |
| Exit codes | Appropriate codes used | Info |
| Input validation | Validates inputs | Warning |
| Path references | Portable paths | Severe |

### Shell Script Checklist

```bash
#!/bin/bash
set -euo pipefail  # Required for safety

# Error handling
trap 'echo "Error on line $LINENO"' ERR

# Input validation
if [ -z "${1:-}" ]; then
    echo "Usage: $0 <arg>" >&2
    exit 1
fi
```

### Python Script Checklist

```python
#!/usr/bin/env python3
"""Script description."""

import sys

def main():
    try:
        # Validate inputs
        if len(sys.argv) < 2:
            print("Usage: script.py <arg>", file=sys.stderr)
            sys.exit(1)
        # Main logic
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Common Composite System Issues

**Should Flag:**
- Memory file contradicts skill instructions
- Referenced scripts don't exist
- Scripts without error handling
- Overlapping skill triggers without clear differentiation
- Broken cross-file references
- Inconsistent naming across components

**Should NOT Flag:**
- Different detail levels in different components
- Reasonable organizational choices
- Style variations within components
- Optional scripts not present
