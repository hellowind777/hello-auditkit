# Audit Checklist - Dimensions

## Table of Contents

- [Dimension 0: Plugin Structure](#dimension-0-plugin-structure-highest-priority)
- [Dimension 0.1: Cross-Component Consistency](#dimension-01-cross-component-consistency)
- [Dimension 1: Fatal Issues](#dimension-1-fatal-issues)
- [Dimension 2: Severe Issues](#dimension-2-severe-issues)
- [Dimension 3: Semantic Ambiguity](#dimension-3-semantic-ambiguity)
- [Dimension 4: Expression Standards](#dimension-4-expression-standards)
- [Dimension 4.1: Conciseness](#dimension-41-conciseness)
- [Dimension 4.2: Freedom Level](#dimension-42-freedom-level)
- [Dimension 5: Structure Issues](#dimension-5-structure-issues)
- [Dimension 6: Robustness](#dimension-6-robustness)
- [Dimension 7: Optimization Suggestions](#dimension-7-optimization-suggestions)
- [Dimension 7.1: LLM Prompting Best Practices](#dimension-71-llm-prompting-best-practices)
- [Dimension 8: Architecture Review](#dimension-8-architecture-review-optional)

---

## Dimension 0: Plugin Structure (Highest Priority)

### 0.1 Manifest Validation

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| `.claude-plugin/` directory exists | Yes | Fatal | Plugin won't load without it |
| `plugin.json` in `.claude-plugin/` | Yes | Fatal | Must be in correct location |
| `name` field present | Yes | Fatal | Required field |
| `name` is non-empty | Yes | Fatal | Cannot be empty string |
| `name` uses kebab-case | Yes | Warning | Best practice |
| `name` ≤50 characters | Yes | Warning | Recommended limit |
| `version` follows semver | X.Y.Z format | Warning | If present |
| `description` present | Yes | Warning | Recommended |
| `description` ≤200 characters | Yes | Warning | If present |

### 0.2 Directory Structure

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Components at root level | Yes | Fatal | Not inside `.claude-plugin/` |
| `commands/` contains `.md` files | Yes | Warning | If directory exists |
| `agents/` contains `.md` files | Yes | Warning | If directory exists |
| `skills/*/SKILL.md` pattern | Yes | Fatal | Exact filename required |
| `hooks/hooks.json` format | Wrapper format | Severe | Plugin-specific format |
| `.mcp.json` valid JSON | Yes | Severe | If file exists |

### 0.3 Naming Conventions

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| All directories kebab-case | Yes | Warning | Best practice |
| All files kebab-case (except SKILL.md) | Yes | Warning | Best practice |
| No spaces in names | Yes | Severe | Will cause issues |
| No special characters | Yes | Severe | Except hyphens |

### 0.4 Path References

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Hooks use `${CLAUDE_PLUGIN_ROOT}` | Yes | Severe | For portability |
| MCP configs use `${CLAUDE_PLUGIN_ROOT}` | Yes | Severe | For portability |
| No hardcoded absolute paths | Yes | Severe | Will break on other systems |
| No `~/` home directory paths | Yes | Severe | Not portable |

---

## Dimension 0.1: Cross-Component Consistency

### Reference Integrity

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| All agent references exist | Yes | Severe | Referenced agents must exist |
| All skill references exist | Yes | Severe | Referenced skills must exist |
| All script references exist | Yes | Severe | Referenced scripts must exist |
| All file references exist | Yes | Severe | Referenced files must exist |
| No circular dependencies | Yes | Fatal | A→B→C→A patterns |

### Script Completeness (For plugins with scripts/)

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Declared scripts exist | Yes | Severe | Scripts in docs must exist |
| Script functions match docs | Yes | Severe | Actual code matches description |
| Script dependencies exist | Yes | Fatal | Imported modules must exist |
| Runtime vs dev scripts separated | Yes | Warning | Dev tools not in runtime deps |
| Undeclared scripts documented | Yes | Warning | Existing scripts should be listed |

**Script Verification Process:**
1. Extract script declarations from docs (hooks.json, SKILL.md, etc.)
2. Determine search paths (scripts/, hooks/scripts/, skill-specific scripts/)
3. Compare declared vs actual scripts
4. For missing scripts: check if functionality merged into other scripts
5. Read actual script source to verify function descriptions
6. Check import dependencies between scripts

### Terminology Consistency

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Same concept, same term | Yes | Warning | Across all files |
| Terminology table if variations | Yes | Warning | If multiple terms used |
| Component names match references | Yes | Severe | Exact match required |

### Rule Numbering Consistency

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Consistent numbering format | Yes | Warning | R1/R2 or 1.1/1.2, not mixed |
| Sequential numbering | Yes | Warning | No gaps (1,2,4 missing 3) |
| Numbering matches references | Yes | Severe | Referenced R3 must exist |
| Nested numbering logical | Yes | Warning | 1.1 under 1, not under 2 |

### Hierarchy Structure

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Heading levels sequential | Yes | Warning | H1→H2→H3, no H1→H3 skip |
| Nesting depth ≤4 levels | Yes | Warning | Deeper is hard to navigate |
| Consistent indentation | Yes | Warning | Same level = same indent |
| List hierarchy logical | Yes | Warning | Sub-items relate to parent |

### Internal References

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| All #anchor links valid | Yes | Severe | Target heading exists |
| All file references exist | Yes | Severe | Referenced files present |
| Relative paths correct | Yes | Severe | ../file.md resolves |
| Template variables defined | Yes | Severe | ${VAR} has definition |
| Template variables used | Yes | Warning | Defined but unused |

### Output Format Consistency

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Consistent output format | Yes | Warning | If plugin defines formats |
| Format defined in one place | Yes | Warning | Avoid duplication |
| Components reference central format | Yes | Warning | If applicable |

---

## Dimension 1: Fatal Issues

### Logic Contradictions

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| No conflicting rules | Yes | Fatal | Rule A vs Rule B |
| No impossible conditions | Yes | Fatal | Can never be satisfied |
| Clear priority when rules overlap | Yes | Severe | Must be resolvable |

### Circular References

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| No circular agent calls | Yes | Fatal | A→B→A |
| No circular skill triggers | Yes | Fatal | Infinite loops |
| No circular file references | Yes | Fatal | Reference chains |

### Critical Omissions

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| All flow paths have endpoints | Yes | Fatal | No dead ends |
| Required dependencies documented | Yes | Severe | External tools, APIs |
| Error handling for critical operations | Yes | Severe | File ops, network |

---

## Dimension 2: Severe Issues

### Description Quality

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Command descriptions present | Yes | Severe | Required for /help |
| Agent descriptions include triggers | Yes | Severe | When to use |
| Skill descriptions include triggers | Yes | Severe | Must be in description |
| Descriptions are clear | Yes | Severe | Not vague |

### Code Quality

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Example code is valid | Yes | Severe | No syntax errors |
| Scripts are executable | Yes | Severe | Proper permissions |
| JSON files are valid | Yes | Severe | Parseable |
| YAML frontmatter is valid | Yes | Severe | Proper syntax |

### Reference Accuracy

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Tool names are valid | Yes | Severe | In allowed-tools |
| Model names are valid | Yes | Severe | haiku/sonnet/opus |
| Event names are valid | Yes | Severe | In hooks |
| Matcher patterns are valid | Yes | Severe | Regex syntax |

---

## Dimension 3: Semantic Ambiguity

### Terminology

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Consistent terminology | Yes | Warning | Same concept = same term |
| Terms defined if domain-specific | Yes | Warning | Glossary if needed |
| No ambiguous pronouns | Yes | Warning | Clear references |

### Conditions

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Trigger conditions are specific | Yes | Warning | Not vague |
| Quantifiers have thresholds | Yes | Warning | "many" → specific number |
| Scope boundaries are clear | Yes | Warning | What's included/excluded |

---

## Dimension 4: Expression Standards

### Redundancy

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| No duplicate content | Yes | Warning | Same info in multiple places |
| No unnecessary explanations | Yes | Warning | Claude already knows |
| Concise over verbose | Yes | Warning | Examples > lengthy text |

### Formatting

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Consistent markdown formatting | Yes | Warning | Headers, lists, code |
| Proper heading hierarchy | Yes | Warning | H1→H2→H3, no skips |
| Code blocks have language tags | Yes | Warning | For syntax highlighting |

### Readability

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Clear structure | Yes | Warning | Logical organization |
| Appropriate section lengths | Yes | Warning | Not too long |
| Examples near explanations | Yes | Warning | Easy to correlate |

---

## Dimension 4.1: Conciseness

### Content Efficiency

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| No Claude-known explanations | Yes | Warning | Don't explain JSON, etc. |
| Examples instead of lengthy text | Yes | Warning | Show, don't tell |
| No repeated information | Yes | Warning | Single source of truth |
| No unnecessary files | Yes | Warning | README.md ok, others not |

### Progressive Loading

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| SKILL.md body ≤500 lines | Ideal | Info | No risk |
| SKILL.md body 500-625 lines | Acceptable | Info | ≤25% over |
| SKILL.md body 625-750 lines | Review | Warning | Consider optimization |
| SKILL.md body >750 lines | Optimize | Severe | Must address |
| Large content in references/ | Yes | Warning | If body too long |

---

## Dimension 4.2: Freedom Level

### Freedom Level Guidelines

| Freedom Level | Applicable Scenarios | Implementation | Example |
|---------------|---------------------|----------------|---------|
| **High** | Multiple methods valid, context-dependent decisions, heuristic guidance | Text instructions | Code style suggestions |
| **Medium** | Preferred patterns exist, some variation allowed, config affects behavior | Pseudocode or parameterized scripts | API call templates |
| **Low** | Fragile operations, consistency critical, specific sequence required | Concrete scripts, few parameters | PDF form filling |

### Task-Appropriate Constraints

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Fragile ops have specific scripts | Yes | Warning | Low freedom for error-prone tasks |
| Flexible tasks have guidelines | Yes | Warning | High freedom for creative tasks |
| Freedom level documented | Yes | Warning | When to deviate |
| No over-constraint on simple tasks | Yes | Warning | Don't use 100-line scripts for style suggestions |
| No under-constraint on fragile tasks | Yes | Warning | Don't use text instructions for PDF filling |

### Common Freedom Level Issues

**Should Flag:**
- PDF form filling task only has text instructions (should have specific script)
- Code style suggestions have 100-line detailed script constraints (over-constrained)
- No guidance on when executor can deviate from instructions

**Should NOT Flag:**
- Using text instructions for genuinely flexible tasks
- Using scripts for genuinely fragile operations
- Reasonable balance between guidance and flexibility

---

## Dimension 5: Structure Issues

### Organization

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Logical grouping | Yes | Warning | Related items together |
| Clear hierarchy | Yes | Warning | Parent-child relationships |
| Appropriate modularity | Yes | Warning | Not too granular/monolithic |

### Maintainability

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Single source of truth | Yes | Warning | No duplicate definitions |
| Changes localized | Yes | Warning | Modify one place |
| Dependencies explicit | Yes | Warning | Clear what depends on what |

---

## Dimension 6: Robustness

### Error Handling

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Common errors handled | Yes | Warning | File not found, etc. |
| Graceful degradation | Yes | Warning | Fallback behavior |
| Clear error messages | Yes | Warning | Actionable guidance |

### Edge Cases

| Check Item | Expected | Severity | Notes |
|------------|----------|----------|-------|
| Empty input handled | Yes | Warning | If applicable |
| Invalid input handled | Yes | Warning | If applicable |
| Boundary conditions | Yes | Warning | Min/max values |

---

## Dimension 7: Optimization Suggestions

### Improvement Opportunities

| Check Item | Criteria | Notes |
|------------|----------|-------|
| Structure optimization | ≥30% improvement, <10% cost | Reorganization |
| Readability improvement | ≥30% time reduction | Formatting, examples |
| Maintainability improvement | Reduces future effort | Modularity |
| Performance optimization | Faster execution | Caching, efficiency |

---

## Dimension 7.1: LLM Prompting Best Practices

**Applies to**: All prompt content, skill instructions, rules, templates, and agent definitions within plugins.

**Purpose**: Evaluate whether the plugin's instructional content follows established LLM prompting best practices for clarity, precision, and reliability.

### Clear Instructions

| Check Item | Expected | Severity |
|------------|----------|----------|
| Specific task description | Clear what to do | Severe |
| Role/persona defined | When behavior matters | Warning |
| Delimiters for sections | Use ```, ---, XML tags | Warning |
| Step-by-step breakdown | For complex tasks | Warning |
| Examples provided | Few-shot when helpful | Info |

### Verbosity Control

| Check Item | Expected | Severity |
|------------|----------|----------|
| Length constraints specified | Yes for outputs | Warning |
| Structured format preferred | Bullets over paragraphs | Warning |
| Concise answers for simple queries | ≤2 sentences for yes/no | Info |
| No unnecessary preamble | Skip "I'll help you with..." | Warning |

### Scope Discipline

| Check Item | Expected | Severity |
|------------|----------|----------|
| Explicit constraints | "EXACTLY and ONLY what requested" | Warning |
| No feature creep | No extra features/embellishments | Warning |
| Simplest interpretation | For ambiguous instructions | Info |
| Clear boundaries | What's in/out of scope | Warning |

### Reference Text & Context

| Check Item | Expected | Severity |
|------------|----------|----------|
| Reference text provided | When accuracy critical | Warning |
| Quote from references | Anchor answers to source | Warning |
| Context window awareness | Don't exceed limits | Severe |

### Task Decomposition

| Check Item | Expected | Severity |
|------------|----------|----------|
| Complex tasks split | Into subtasks | Warning |
| Intent classification | For multi-path flows | Info |
| Summarize long content | Before processing | Info |

### Long-Context Handling (>10k tokens)

| Check Item | Expected | Severity |
|------------|----------|----------|
| Internal outline first | For long outputs | Info |
| Re-state constraints | Before answering | Info |
| Anchor claims to sections | Not generic statements | Warning |
| Quote fine details | Dates, thresholds, specifics | Warning |

### Ambiguity & Hallucination Mitigation

| Check Item | Expected | Severity |
|------------|----------|----------|
| Clarifying questions | 1-3 for underspecified queries | Info |
| Multiple interpretations | Present 2-3 with assumptions | Info |
| No fabrication | Don't invent figures/references | Severe |
| Explicit uncertainty | "I'm not sure" when appropriate | Warning |
| Admit limitations | When outside knowledge | Warning |

### Tool Usage Guidance

| Check Item | Expected | Severity |
|------------|----------|----------|
| Prefer tools over knowledge | For fresh/user-specific data | Warning |
| Parallelize reads | Independent operations | Info |
| Restate changes | After write operations | Warning |

### Rule & Template Quality

| Check Item | Expected | Severity |
|------------|----------|----------|
| Rules are actionable | Clear what to do, not just what not to do | Warning |
| Templates have placeholders | Clear variable markers | Warning |
| Examples accompany rules | Show, don't just tell | Info |
| Priority/order specified | When rules might conflict | Warning |
| Edge cases addressed | Common exceptions documented | Info |

### Reasoning & Chain-of-Thought

| Check Item | Expected | Severity |
|------------|----------|----------|
| Think step-by-step | For complex reasoning | Info |
| Show work before answer | When accuracy matters | Info |
| Self-verification | Check own output | Info |

---

## Dimension 8: Architecture Review (Optional)

### Architecture Quality

| Check Item | Expected | Notes |
|------------|----------|-------|
| Clear responsibility boundaries | Yes | Each component has clear role |
| Appropriate coupling | Yes | Not too tight/loose |
| Extensibility | Yes | Easy to add features |
| Reusability | Yes | Shared components where appropriate |
| Clear abstraction layers | Yes | Logical hierarchy |

### Improvement Areas

| Area | Assessment | Notes |
|------|------------|-------|
| Progressive loading optimization | Level 1/2/3 distribution | Content placement |
| Modular refactoring | Extractable components | Shared functionality |
| Flow simplification | Phase granularity | Too many/few steps |
| Routing optimization | Decision complexity | Clear decision tree |
