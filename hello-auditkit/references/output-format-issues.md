# Audit Output Format - Issues & Summary

## Table of Contents

- [4. Issue Classification](#4-issue-classification)
- [5. Verification Statistics](#5-verification-statistics)
- [6. Audit Summary](#6-audit-summary)
- [7. User Confirmation](#7-user-confirmation)
- [8. Modified Content](#8-modified-content)
- [Quick Reference](#quick-reference-status-icons)

---

## 4. Issue Classification

### Format for Each Issue Category

```markdown
---
## [Category] Issues

### Issue #N: [Short Title] - [File/Component]

**Problem Description**: Clear description of the issue

**Specific Impact**: What execution failure or error this causes

**Location**: File path and section/line

**Evidence**:
```
[Relevant code or content snippet]
```

**Fix Suggestion**: How to resolve

**Detailed Fix**:
Before:
```
[Original content]
```

After:
```
[Fixed content]
```
---
```

### Issue Categories (in order)

1. **Plugin Structure Issues** (Dimension 0)
2. **Cross-Component Issues** (Dimension 0.1)
3. **Fatal Issues** (Dimension 1)
4. **Severe Issues** (Dimension 2)
5. **Semantic Ambiguity Issues** (Dimension 3)
6. **Expression Issues** (Dimension 4)
7. **Conciseness Issues** (Dimension 4.1)
8. **Freedom Level Issues** (Dimension 4.2)
9. **Structure Issues** (Dimension 5)
10. **Robustness Issues** (Dimension 6)
11. **Optimization Suggestions** (Dimension 7)

### No Issues Found

```markdown
---
✅ **No [Category] issues found.**
---
```

### All Clear

```markdown
---
✅ **Audit Complete - No Issues Found**

The plugin passes all audit checks:
- Plugin structure is valid
- All components follow specifications
- No fatal, severe, or significant issues detected
- Best practices are followed

The plugin is ready for use.
---
```

---

## 5. Verification Statistics

**Output position**: After all issue classifications, before summary

```markdown
---
## Verification Statistics

**Scan Results**:
- Suspected issues scanned: X
- Issues verified: Y
- Issues discarded: Z

**By Category**:
| Category | Scanned | Verified | Discarded |
|----------|---------|----------|-----------|
| Structure | X | Y | Z |
| Cross-Component | X | Y | Z |
| Fatal | X | Y | Z |
| Severe | X | Y | Z |
| Other | X | Y | Z |

**Verification Rate**: Y/X (XX%)

**Discarded Issues Summary** (if any):
- [Issue description] - Discarded because: [reason - e.g., "design choice", "AI can infer", "not in scope"]
---
```

---

## 6. Audit Summary

**Output condition**: Only when issues are found

```markdown
---
## Audit Summary

**Overall Assessment**: [Quality evaluation - Good/Acceptable/Needs Work/Critical Issues]

**Core Strengths**:
- [What the plugin does well]
- [Good practices observed]

**Main Risks**:
- [Priority concerns]
- [Areas needing attention]

**Best Practices Compliance**:
| Practice | Status | Notes |
|----------|--------|-------|
| Plugin structure | ✅/❌ | [Notes] |
| Naming conventions | ✅/⚠️ | [Notes] |
| Path portability | ✅/❌ | [Notes] |
| Description quality | ✅/⚠️ | [Notes] |
| Progressive loading | ✅/⚠️ | [Notes] |

**Recommended Fix Priority**:
1. [Highest priority fix]
2. [Second priority]
3. [Third priority]
---
```

---

## 7. User Confirmation

**Output condition**: Only when issues are found

```markdown
---
## Next Steps

**Issues found that require attention:**
- Fatal: X issues
- Severe: X issues
- Warnings: X issues
- Suggestions: X items

**Would you like me to:**
1. Generate fixed versions of affected files?
2. Explain specific issues in more detail?
3. Prioritize fixes differently?

Please confirm how you'd like to proceed.
---
```

**Important**: Do NOT automatically generate fixes. Wait for user confirmation before modifying any files.

---

## 8. Modified Content

**Output condition**: After user confirms they want fixes

```markdown
---
## Fixed Content

### [File Path]

**Changes Made**:
1. [Change 1 description]
2. [Change 2 description]

**Complete Fixed File**:
```[language]
[Full fixed file content]
```
---
```

---

## Quick Reference: Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Pass / Valid / No issues |
| ❌ | Fail / Invalid / Issue found |
| ⚠️ | Warning / Suboptimal but acceptable |
| - | Not applicable / Not present |

## Quick Reference: Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| Fatal | Plugin won't work | Must fix |
| Severe | Major functionality affected | Should fix |
| Warning | Suboptimal but works | Consider fixing |
| Info | Suggestion only | Optional |
