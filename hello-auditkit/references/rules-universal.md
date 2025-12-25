# Universal Audit Rules

## Table of Contents

- [AI Executor Awareness](#ai-executor-awareness)
- [Content-Based Audit Principle](#content-based-audit-principle)
- [Universal Prompt Quality Rules](#universal-prompt-quality-rules)
- [Universal Size Thresholds](#universal-size-thresholds)
- [Universal Format Rules](#universal-format-rules)
- [Internationalization Rules](#internationalization-rules)
- [Universal Should Flag](#universal-should-flag)
- [Universal Should NOT Flag](#universal-should-not-flag)

---

## AI Executor Awareness

> **Rationale**: See `methodology-core.md` → AI Capability Model

### Core Principle

AI executors have contextual understanding and can infer from common sense and context.

### Audit Checks

| Check | Guideline | Severity |
|-------|-----------|----------|
| Avoid over-specification | Don't specify what AI can infer | Warning |
| Trust AI judgment | Guidelines over rigid rules for flexible tasks | Info |
| No redundant explanations | Don't explain concepts AI already knows | Warning |

**Threshold**: If <30% would misunderstand → AI can handle it, don't flag.

---

## Content-Based Audit Principle

**Audit is based on CONTENT user provides, NOT limited to specific system paths.**

User may:
- Provide files copied to any location for review
- Paste content directly
- Point to any directory structure

**Focus on**: Content quality itself
**Path/location checks**: Informational only (marked as "Info (advisory)")

---

## Universal Prompt Quality Rules

> **Execution Required**: For ALL content containing AI instructions (prompts, skills, agents, commands), verify each check below.

**Applies to**: All content containing instructions for AI execution
- Prompts, Memory files, Skill bodies, Command bodies, Agent bodies, Hook prompts

### LLM Prompting Best Practices

| Check | Requirement | Severity | Applies To |
|-------|-------------|----------|------------|
| Verbosity constraints | Explicit output length limits | Warning | All prompts |
| Scope boundaries | Clear "do not" constraints | Warning | All instructions |
| Ambiguity handling | Instructions for unclear cases | Info | Complex tasks |
| No AI-known content | Don't explain standard concepts | Warning | All |
| Grounding | "Based on context" for uncertain claims | Info | Data extraction |

### Freedom Level Matching

| Task Type | Expected Constraint Level | Issue if Mismatch |
|-----------|---------------------------|-------------------|
| Fragile/deterministic ops | Specific scripts | Severe if too loose |
| Data extraction | Strict schema | Severe if unstructured |
| Creative/flexible tasks | Guidelines only | Warning if over-constrained |
| Code generation | Patterns + flexibility | Warning if too rigid |

### Conciseness Principle

| Check | Requirement | Severity |
|-------|-------------|----------|
| Single source of truth | Info in ONE place only | Warning |
| No duplication | Not in body AND references | Warning |
| Prefer examples | Over lengthy explanations | Info |
| Remove AI-known | Don't explain common concepts | Warning |

### Trigger Condition Placement

| Content Type | Trigger Location | Body Contains |
|--------------|------------------|---------------|
| Skill | description field | Implementation |
| Agent | description field | Instructions |
| Command | description field | Task instructions |
| Hook | matcher config | Action logic |

**Issue**: Trigger conditions in body instead of description → Severe

---

## Numbering & Order Rules

> **Execution Required**: Extract actual numbers from content and verify.

### Numbering Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Sequential numbering | No gaps (1,2,3 not 1,2,4) | Warning |
| Consistent format | Same style (R1/R2 OR 1.1/1.2) | Warning |
| Referenced numbers exist | All referenced R1, Step 2 etc. exist | Severe |
| No duplicate numbers | Each number used once | Warning |
| Hierarchical consistency | 1.1, 1.2 under section 1 | Warning |

### Order Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Section order logical | Prerequisites before dependents | Warning |
| Heading hierarchy | H1→H2→H3 (no skipping) | Warning |
| TOC matches content | TOC order = section order | Warning |
| Priority order | High priority items first | Info |
| Chronological flow | Steps in execution order | Warning |

---

## Reference Integrity Rules

> **Execution Required**: Extract ALL references from content (file refs, anchor links, numbered refs) and verify each exists.

### Reference Accuracy

| Check | Requirement | Severity |
|-------|-------------|----------|
| Named references exist | All `@file`, `skill-name` exist | Severe |
| Numbered references exist | All R1, Step 2, etc. defined | Severe |
| Anchor links valid | All #section-name anchors resolve | Warning |
| Cross-file refs valid | References to other files exist | Severe |
| No orphan references | No undefined references | Warning |

### Reference Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Same ref = same format | Consistent reference style | Warning |
| Bidirectional integrity | If A refs B, B should ref A (if needed) | Info |
| No circular references | A→B→C→A pattern | Fatal |
| No conflicting references | Same name != different targets | Severe |

---

## Diagram & Flowchart Rules

> **Execution Required**: If diagrams exist, verify each node has text description and all paths have endpoints.

### Diagram-Text Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Node names match text | Diagram nodes = text descriptions | Severe |
| Flow paths match rules | Diagram paths = documented flow | Severe |
| All paths documented | Every diagram path has description | Warning |
| No undocumented nodes | Every node explained | Warning |
| Conditions match | Decision conditions consistent | Severe |

### Flowchart Logic Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| All paths have endpoints | No hanging branches | Fatal |
| No infinite loops | All loops have exit conditions | Fatal |
| Decision completeness | All decision branches handled | Severe |
| Start/end nodes present | Clear entry and exit points | Warning |
| Consistent notation | Same symbols throughout | Info |

### Mermaid/Diagram Syntax

| Check | Requirement | Severity |
|-------|-------------|----------|
| Valid syntax | Renders without error | Severe |
| Node IDs match references | Referenced nodes exist | Severe |
| Edge labels clear | Conditions readable | Info |

---

## Language Expression Rules

> **Execution Required**: Scan for ambiguity patterns listed below. Flag if found without condition/context.

### Clarity & Precision

| Check | Requirement | Severity |
|-------|-------------|----------|
| Clear wording | No ambiguous phrases | Warning |
| Fluent expression | Grammatically correct | Warning |
| No typos | Scan for spelling errors in identifiers, headings, key terms | Info |
| No redundancy | No unnecessary repetition | Warning |
| Consistent verb tense | Same tense throughout | Info |

### Ambiguity Detection

| Check | Requirement | Severity |
|-------|-------------|----------|
| Vague quantifiers/timing | Must be specific or have context | Warning |
| Undefined criteria | "appropriate/suitable" needs definition | Warning |
| Incomplete enumerations | "etc." should have examples or be exhaustive | Info |

### Terminology Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Same concept = same term | One term per concept | Warning |
| Defined domain terms | Technical terms explained | Info |
| Consistent verb forms | Same verbs for same actions | Warning |
| Consistent formatting | Same style for same elements | Warning |

---

## Security & Compliance Rules

> **Execution Required**: Search for hardcoded paths, secrets, API keys. Check scripts for injection vulnerabilities.

### Security Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| No hardcoded secrets | Use env variables | Severe |
| No exposed credentials | API keys, passwords protected | Severe |
| Path traversal prevention | Sanitize file paths | Severe |
| Input validation rules | Validate user input | Warning |
| Command injection prevention | Sanitize shell inputs | Severe |

### Compliance Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Data handling rules | Privacy requirements documented | Warning |
| Error disclosure | No sensitive info in errors | Warning |
| Audit trail | Actions logged appropriately | Info |
| Access control | Permissions documented | Warning |

---

## Structure & Organization Rules

> **Execution Required**: Verify TOC-content match by comparing actual entries.

### Section Structure

| Check | Requirement | Severity |
|-------|-------------|----------|
| TOC present (>100 lines) | Table of contents for navigation | Info |
| TOC-content match | Every TOC entry has corresponding heading | Warning |
| Logical grouping | Related content together | Warning |
| Clear boundaries | Sections clearly separated | Info |
| No orphan sections | All sections integrated | Warning |

### Rule Organization

| Check | Requirement | Severity |
|-------|-------------|----------|
| Single source of truth | Rule defined in one place | Warning |
| No scattered rules | Same rule not in >3 files | Warning |
| No semantic duplicates | No rules with same meaning but different wording | Warning |
| Proper categorization | Rules in correct sections | Warning |
| Level-appropriate | Global vs local rules correct | Warning |

### Template Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| Required sections present | All mandatory sections exist | Severe |
| Section order correct | Sections in expected order | Warning |
| Consistent formatting | Same format across similar files | Warning |

---

## Universal Size Thresholds

> See `methodology-core.md` → Necessity Threshold for rationale.

### Tiered Size Evaluation

| Range | Status | Severity |
|-------|--------|----------|
| ≤500 lines | Ideal | - |
| 500-550 (≤10% over) | **NOT an issue** | - |
| 550-625 (10-25% over) | Info only | Info |
| 625-750 (>25% over) | Should fix | Warning |
| >750 lines | Must fix | Severe |

### Component-Specific Limits

| Component | Limit | Notes |
|-----------|-------|-------|
| L1 Metadata | ~100 words | Permanent context cost |
| L2 Body | <500 lines | Self-sufficient for common cases |
| L3 References | ≤500 lines/file | On-demand loading |
| L4 Scripts | No limit | Runtime only |

---

## Universal Format Rules

### Frontmatter Validation

| Field | Rule | Severity |
|-------|------|----------|
| Required fields | Must be present and non-empty | Fatal/Severe |
| name | kebab-case, appropriate length | Warning |
| description | Include trigger conditions, concise | Severe |
| Valid YAML | Parseable, correct syntax | Fatal |

### Markdown Structure

| Check | Rule | Severity |
|-------|------|----------|
| Heading hierarchy | H1→H2→H3 (no skipping) | Warning |
| Table format | Valid markdown tables | Warning |
| Code blocks | Proper language tags | Info |
| Links | Valid internal/external links | Warning |

### Naming Conventions

| Element | Convention | Severity |
|---------|------------|----------|
| Directories | kebab-case | Warning |
| Files | kebab-case (except SKILL.md) | Warning |
| No spaces | Use hyphens instead | Severe |
| No special chars | Letters, numbers, hyphens only | Severe |
| File encoding | UTF-8 without BOM | Warning |

---

## Internationalization Rules

### When i18n is Declared

**Applies when**: Content has any language/locale configuration

| Check | Guideline | Severity |
|-------|-----------|----------|
| No hardcoded user-facing text | Use variables/templates | Warning |
| No fixed language output examples | Use `{example_output}` placeholders | Warning |
| Language-agnostic rules | Rules shouldn't assume specific language | Info |
| BCP 47 language tags | Standard format like `zh-CN`, `en-US` | Warning |

### Hardcoded Content Exceptions

**Do NOT flag:**
- License/copyright notices
- Technical terms (API, JSON, etc.)
- Code examples showing syntax (not content)
- Variable/function names
- Log messages for debugging

---

## Universal Should Flag

### Fatal Issues (Blocks Execution)

- Contradictory rules (A vs NOT A)
- Impossible conditions
- Circular references (A→B→C→A)
- Missing required fields
- Invalid syntax (JSON, YAML, etc.)
- Referenced files/components don't exist

### Severe Issues (Major Impact)

- Hardcoded absolute paths (should use relative paths or environment variables)
- Missing trigger conditions in descriptions
- ≥60% executor error rate
- Core workflow in wrong location
- Security vulnerabilities (injection, secrets)
- Invalid tool/model/event names

### Warnings (Suboptimal)

- Size >625 lines (25%+ over recommended)
- Missing "when to read" for references
- Vague instructions ("do it well")
- Inconsistent terminology without explanation
- Missing error handling
- Non-kebab-case naming

### Info (Suggestions)

- Size 550-625 lines (10-25% over)
- Could benefit from examples
- Minor style variations
- Optional fields missing
- Optimization opportunities

---

## Universal Should NOT Flag

### Size Tolerance

- ≤10% over recommended → **NOT an issue**
- 504/500 lines → **NOT an issue** (only 0.8% over)
- 520/500 lines → **NOT an issue** (only 4% over)

### Design Choices

- Different directory naming (commands/ vs cmds/)
- Different file organization
- Style variations within specification
- Platform-specific patterns (Claude vs Codex)
- Using different valid approaches

### Intentional Content

- License/copyright notices
- Brand identifiers
- Fixed header/footer in output
- Technical specifications
- Code examples demonstrating syntax

### AI Capability

- Content AI can infer from context
- Standard terminology without definition
- Common patterns without explanation
- Obvious constraints

### Optional Elements

- Missing optional fields
- Missing README.md
- Missing version field
- Additional helper directories

---

## Severity Decision Matrix

### Quick Reference

| Condition | Severity |
|-----------|----------|
| Cannot execute at all | Fatal |
| ≥60% serious errors | Severe |
| ≥3 conflicting interpretations | Severe |
| ≥40% misunderstand | Warning |
| ≥20% failure in common cases | Warning |
| ≥30% improvement possible, <10% cost | Info |
| <10% over recommended | NOT an issue |
| AI can infer | NOT an issue |
| Design choice | NOT an issue |

### Verification Questions

Before flagging ANY issue:

1. **Concrete impact?** Can you describe specific failure?
2. **In scope?** Within design boundaries?
3. **Flaw or choice?** Can find reasonable rationale?
4. **Meets threshold?** Above quantified threshold?

If ANY answer is NO → Discard the issue
