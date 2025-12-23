# Special Output Formats

## Table of Contents

- [Design Alignment Review](#design-alignment-review-optional-add-on)
- [Terminology Consistency Report](#terminology-consistency-report)
- [Architecture Review Output](#architecture-review-output)

---

## Design Alignment Review (Optional Add-on)

**What it is**: NOT a separate mode. This is an optional add-on that can be combined with ANY audit mode when user provides original design requirements along with content to audit.

**Output condition**: When user provides both:
- Content to audit (any supported type)
- Original design requirements (brief description, detailed paragraph, or formal document)

**Output position**: After standard audit results, as an additional "Design Alignment" section

```markdown
---
## Design Alignment Review

**Content Audited**: [Plugin/Skill/Component path/name]
**Design Requirements Provided**: [Summary of user's stated goals]

---

### Design-Implementation Gap Analysis

| Design Goal | Implementation Status | Gap Assessment |
|-------------|----------------------|----------------|
| [Goal 1] | ✅ Fully implemented / ⚠️ Partial / ❌ Missing | [Details] |
| [Goal 2] | ✅/⚠️/❌ | [Details] |

---

### Intent Alignment by Component

#### [Component Name]

| Aspect | Design Intent | Actual Implementation | Aligned |
|--------|---------------|----------------------|---------|
| Purpose | [What it should do] | [What it does] | ✅/❌ |
| Triggers | [When it should activate] | [When it activates] | ✅/❌ |
| Scope | [Expected coverage] | [Actual coverage] | ✅/❌ |

---

### Trigger Condition Assessment

| Intended Scenario | Triggers Correctly | Notes |
|-------------------|-------------------|-------|
| [Scenario 1] | ✅/❌ | [Why/why not] |

---

### User Journey Validation

| User Goal | Achievable | Workflow Issues |
|-----------|------------|-----------------|
| [Goal 1] | ✅/❌ | [Issues if any] |

---

### Design Alignment Summary

**Overall Alignment**: [High/Medium/Low]

**Key Gaps**:
1. [Most critical gap]
2. [Second gap]

**Recommendations**:
1. [Priority fix]
2. [Secondary fix]
---
```

---

## Terminology Consistency Report

**Output condition**: When terminology inconsistencies found

```markdown
---
## Terminology Consistency Report

| Concept | Terms Used | Locations | Consistent |
|---------|------------|-----------|------------|
| [Concept] | term1 (X), term2 (Y) | file1, file2 | ✅/❌ |

**Recommendation**: [Standardize on term X because...]
---
```

---

## Architecture Review Output (Optional)

**Output condition**: When user requests architecture review

```markdown
---
## Architecture Review

### Current Architecture Overview
[Brief description of current plugin architecture]

### Architecture Issues Identified

| Issue | Impact | Severity |
|-------|--------|----------|
| [Issue 1] | [Impact description] | High/Medium/Low |

### Architecture Improvement Suggestions

| Improvement | Current State | Suggested Change | Expected Benefit |
|-------------|---------------|------------------|------------------|
| [Item] | [Current] | [Suggested] | [Benefit] |

### Recommended Architecture

[If major changes suggested, provide complete architecture proposal]

**Note**: Architecture suggestions are recommendations. Evaluate based on actual project needs before implementing.
---
```
