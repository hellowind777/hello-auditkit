# Audit Checklist

> **Execution Required**: This checklist contains ALL audit dimensions. Execute each relevant dimension based on content type. Output check results with evidence.

## Quick Navigation

- [Dimension 0: Structure](#dimension-0-structure)
- [Dimension 0.1: Cross-Component](#dimension-01-cross-component)
- [Dimension 0.2: Design Coherence](#dimension-02-design-coherence)
- [Dimension 0.3: Progressive Loading](#dimension-03-progressive-loading)
- [Dimension 0.4: Naming & Numbering](#dimension-04-naming--numbering)
- [Dimension 0.5: Reference Integrity](#dimension-05-reference-integrity)
- [Dimension 0.6: Diagram & Flowchart](#dimension-06-diagram--flowchart)
- [Dimension 0.7: Language Expression](#dimension-07-language-expression)
- [Dimension 0.8: Security & Compliance](#dimension-08-security--compliance)
- [Dimensions 1-2: Fatal & Severe](#dimensions-1-2-fatal--severe)
- [Dimensions 3-6: Quality](#dimensions-3-6-quality)
- [Dimensions 7-8: Optimization](#dimensions-7-8-optimization)
- [Examples](#examples)

---

## Dimension 0: Structure

### 0.1 Manifest Validation

| Check | Expected | Severity |
|-------|----------|----------|
| `.claude-plugin/` exists | Yes (plugins) | Fatal |
| `plugin.json` in `.claude-plugin/` | Yes | Fatal |
| `name` field present | Yes | Fatal |
| `name` kebab-case, ≤50 chars | Yes | Warning |
| `version` follows semver | Yes | Warning |
| `description` ≤200 chars | Yes | Warning |

### 0.2 Directory Structure

| Check | Expected | Severity |
|-------|----------|----------|
| Components at root (not in .claude-plugin/) | Yes | Fatal |
| `skills/*/SKILL.md` exact filename | Yes | Fatal |
| `hooks/hooks.json` wrapper format | Yes | Severe |
| `.mcp.json` valid JSON | Yes | Severe |

### 0.3 Naming & Paths

| Check | Expected | Severity |
|-------|----------|----------|
| kebab-case (except SKILL.md) | Yes | Warning |
| No spaces or special chars | Yes | Severe |
| Use relative paths or env variables | Yes | Severe |

---

## Dimension 0.1: Cross-Component

### Reference & Script Integrity

| Check | Expected | Severity |
|-------|----------|----------|
| All referenced components exist | Yes | Severe |
| No circular dependencies | Yes | Fatal |
| Script functions match docs | Yes | Severe |
| Script imports exist | Yes | Fatal |

### Terminology & Numbering

| Check | Expected | Severity |
|-------|----------|----------|
| Same concept = same term | Yes | Warning |
| Consistent numbering format | Yes | Warning |
| Sequential numbering | Yes | Warning |
| Valid anchor links | Yes | Severe |

---

## Dimension 0.2: Design Coherence

### Full Directory Scanning

| Check | Expected | Severity |
|-------|----------|----------|
| All files enumerated | Yes | Info |
| All rules cataloged | Yes | Info |
| Cross-file contradictions detected | Yes | Severe |
| Rules propagated to relevant files | Yes | Warning |

### Framework Design

| Check | Expected | Severity |
|-------|----------|----------|
| No god files (SKILL.md >625 lines) | Yes | Warning |
| No scattered rules (>3 files) | Yes | Warning |
| No circular dependencies | Yes | Severe |
| Separation of concerns | Yes | Warning |

---

## Dimension 0.3: Progressive Loading

### Content Level Distribution

| Level | Limit | If Exceeded |
|-------|-------|-------------|
| L1 (metadata) | ≤100 words | Warning (>500: Severe) |
| L2 (body) | ≤500 lines | Warning (>625: Severe) |
| L3 (references) | **No official limit** | Evaluate by content nature |
| L4 (scripts) | No limit | N/A |

### Content Placement

| Check | Expected | Severity |
|-------|----------|----------|
| Core workflow in L2 | Yes | Severe |
| Edge cases in L3 | Yes | Warning |
| "When to read" guidance | Yes | Warning |

---

## Dimension 0.4: Naming & Numbering

> **MUST EXECUTE**: Extract actual numbers from content and verify. Do not skip.

### Naming Validation

| Check | Expected | Severity |
|-------|----------|----------|
| Consistent naming style | Same format throughout | Warning |
| kebab-case for identifiers | Except SKILL.md | Warning |
| No spaces/special chars | Letters, numbers, hyphens | Severe |
| Name reflects content | Descriptive names | Warning |
| No duplicate names | Unique identifiers | Severe |

### Numbering Validation

| Check | Expected | Severity |
|-------|----------|----------|
| Sequential (no gaps) | 1,2,3 not 1,2,4 | Warning |
| Consistent format | R1/R2 OR 1.1/1.2 | Warning |
| Referenced # exist | All R1, Step 2 defined | Severe |
| No duplicate numbers | Each number once | Warning |
| Hierarchical correct | 1.1, 1.2 under 1 | Warning |

### Order Validation

| Check | Expected | Severity |
|-------|----------|----------|
| Section order logical | Prerequisites first | Warning |
| Heading hierarchy | H1→H2→H3 no skip | Warning |
| TOC matches content | All TOC entries have headings | Warning |
| Priority order | High priority first | Info |
| Steps chronological | Execution order | Warning |

---

## Dimension 0.5: Reference Integrity

### Reference Accuracy

| Check | Expected | Severity |
|-------|----------|----------|
| Named refs exist | @file, skill-name | Severe |
| Numbered refs exist | R1, Step 2 defined | Severe |
| Anchor links valid | #section resolves | Warning |
| Cross-file refs valid | Target files exist | Severe |
| No undefined refs | All refs resolvable | Warning |

### Reference Consistency

| Check | Expected | Severity |
|-------|----------|----------|
| Same ref = same format | Consistent style | Warning |
| No circular refs | A→B→C→A pattern | Fatal |
| No conflicting refs | Same name = same target | Severe |
| Bidirectional valid | If A→B, B→A exists (if needed) | Info |

---

## Dimension 0.6: Diagram & Flowchart

### Diagram-Text Consistency

| Check | Expected | Severity |
|-------|----------|----------|
| Node names match text | Diagram = description | Severe |
| Flow paths match rules | Diagram = documented flow | Severe |
| All paths documented | Every path has description | Warning |
| No undocumented nodes | Every node explained | Warning |
| Conditions match | Decision conditions consistent | Severe |

### Flowchart Logic

| Check | Expected | Severity |
|-------|----------|----------|
| All paths have endpoints | No hanging branches | Fatal |
| No infinite loops | Exit conditions exist | Fatal |
| Decision completeness | All branches handled | Severe |
| Start/end nodes present | Clear entry/exit | Warning |
| Consistent notation | Same symbols | Info |

### Mermaid/Diagram Syntax

| Check | Expected | Severity |
|-------|----------|----------|
| Valid syntax | Renders without error | Severe |
| Node IDs match refs | Referenced nodes exist | Severe |
| Edge labels clear | Conditions readable | Info |

---

## Dimension 0.7: Language Expression

### Clarity & Precision

| Check | Expected | Severity |
|-------|----------|----------|
| Clear wording | No ambiguous phrases | Warning |
| Fluent expression | Grammatically correct | Warning |
| No typos | Spelling correct | Info |
| No redundancy | No unnecessary repeat | Warning |
| Consistent verb tense | Same tense throughout | Info |

### Ambiguity Patterns

| Check | Requirement | Severity |
|-------|-------------|----------|
| Vague quantifiers/timing | Must be specific or have context | Warning |
| Undefined criteria | Needs definition | Warning |
| Incomplete enumerations | Should have examples | Info |

### Terminology Consistency

| Check | Expected | Severity |
|-------|----------|----------|
| Same concept = same term | One term per concept | Warning |
| Domain terms defined | Technical terms explained | Info |
| Consistent verb forms | Same verbs for actions | Warning |
| Consistent formatting | Same style for elements | Warning |

### Wording Patterns (LLM Best Practices)

| Check | Expected | Severity |
|-------|----------|----------|
| Hedging language | "Based on provided context..." for uncertain claims | Warning |
| Avoid absolutes | No unqualified "always", "guaranteed", "never" | Warning |
| Scope constraint wording | "EXACTLY and ONLY", explicit "Do NOT" lists | Warning |
| Ambiguity handling wording | Clarifying questions OR interpretations with labels | Warning |
| No fabrication wording | "Never fabricate..." for factual content | Severe |
| Verbosity constraint wording | "≤N sentences/bullets", not vague "be concise" | Warning |

---

## Dimension 0.8: Security & Compliance

### Security Checks

| Check | Expected | Severity |
|-------|----------|----------|
| No hardcoded secrets | Use env variables | Severe |
| No exposed credentials | Protected | Severe |
| Path traversal prevention | Sanitize paths | Severe |
| Input validation | Validate user input | Warning |
| Command injection prevention | Sanitize inputs | Severe |

### Compliance Checks

| Check | Expected | Severity |
|-------|----------|----------|
| Data handling rules | Privacy documented | Warning |
| Error disclosure | No sensitive info | Warning |
| Audit trail | Actions logged | Info |
| Access control | Permissions documented | Warning |

---

## Dimensions 1-2: Fatal & Severe

### Fatal Issues (Dimension 1)

| Check | Expected | Severity |
|-------|----------|----------|
| No conflicting rules | Yes | Fatal |
| No impossible conditions | Yes | Fatal |
| No circular references | Yes | Fatal |
| All flow paths have endpoints | Yes | Fatal |

### Severe Issues (Dimension 2)

| Check | Expected | Severity |
|-------|----------|----------|
| Descriptions include triggers | Yes | Severe |
| Example code is valid | Yes | Severe |
| Scripts are executable | Yes | Severe |
| JSON/YAML valid | Yes | Severe |
| Valid tool/model/event names | Yes | Severe |

---

## Dimensions 3-6: Quality

### Dimension 3: Semantic Ambiguity

| Check | Expected | Severity |
|-------|----------|----------|
| Consistent terminology | Yes | Warning |
| Domain terms defined | Yes | Warning |
| Specific trigger conditions | Yes | Warning |
| Quantifiers have thresholds | Yes | Warning |

### Dimension 4: Expression Standards

| Check | Expected | Severity |
|-------|----------|----------|
| No duplicate content | Yes | Warning |
| No unnecessary explanations | Yes | Warning |
| Consistent markdown | Yes | Warning |
| Proper heading hierarchy | Yes | Warning |

### Dimension 5: Structure & Organization

| Check | Expected | Severity |
|-------|----------|----------|
| Logical grouping | Yes | Warning |
| Single source of truth | Yes | Warning |
| Dependencies explicit | Yes | Warning |
| TOC for long files | >100 lines | Info |
| Section boundaries clear | Yes | Info |
| No orphan sections | Yes | Warning |

### Dimension 5.1: Rule Logic

| Check | Expected | Severity |
|-------|----------|----------|
| No rule conflicts | Rules don't contradict | Severe |
| No rule duplication | Rules not repeated | Warning |
| No semantic duplicates | Different wording, same meaning → merge | Warning |
| Rules properly categorized | In correct sections | Warning |
| Rule coverage complete | All scenarios covered | Warning |
| Rule priority clear | When multiple apply | Warning |
| Optimization opportunities | Redundant rules → DELETE, conflicting → MERGE | Info |

### Dimension 5.2: Process Logic

| Check | Expected | Severity |
|-------|----------|----------|
| All scenarios covered | Main + edge cases | Warning |
| Main flow clear | Primary path obvious | Warning |
| Sub-flows documented | Secondary paths clear | Warning |
| No dead loops | Exit conditions exist | Fatal |
| No duplicate invocations | Each step once | Warning |
| No conflicting invocations | Steps don't conflict | Severe |

### Dimension 6: Robustness

| Check | Expected | Severity |
|-------|----------|----------|
| Common errors handled | Yes | Warning |
| Edge cases handled | Yes | Warning |
| Error recovery documented | Yes | Info |
| Fallback paths defined | Yes | Info |

---

## Dimensions 7-8: Optimization

### Dimension 7: Suggestions

| Check | Criteria |
|-------|----------|
| Structure optimization | ≥30% improvement, <10% cost |
| Readability improvement | ≥30% time reduction |
| Maintainability | Reduces future effort |

### LLM Prompting Best Practices

> **Detailed guidance**: See `type-prompt.md` → LLM Prompting Best Practices

| Check | Expected | Severity |
|-------|----------|----------|
| Verbosity constraints | Explicit length limits | Severe |
| Scope boundaries | "Do not" constraints present | Severe |
| No fabrication instruction | "Never fabricate..." | Severe |
| Output schema (structured) | JSON structure defined | Warning |
| Grounding language | "Based on context" | Warning |
| Self-check (high-risk) | Verification step | Warning |
| Tool preference | Tools over internal knowledge | Warning |
| Agentic updates | Brief, major phases, concrete outcomes | Warning |
| No task expansion | Don't expand beyond request | Warning |
| Long-context outline | >10k: outline, restatement, refs | Warning |
| Structured null handling | Missing → null, re-scan | Warning |

### Dimension 8: Architecture (Optional)

| Check | Expected |
|-------|----------|
| Clear responsibility boundaries | Yes |
| Appropriate coupling | Yes |
| Extensibility | Yes |
| Progressive loading optimization | Yes |

---

## Size Thresholds

> See `methodology-core.md` → Necessity Threshold for tiered evaluation.
> Key rule: ≤10% over recommended = **NOT an issue**.

---

## Examples

### Should Flag

**Structure:**
- `plugin.json` in root (not `.claude-plugin/`) → Fatal
- `skill.md` instead of `SKILL.md` → Fatal
- Components inside `.claude-plugin/` → Fatal

**Paths:**
- Hook uses `/Users/name/plugins/script.sh` → Severe (hardcoded absolute path)
- MCP config uses absolute path instead of relative → Severe

**Content:**
- Description missing triggers → Severe
- Referenced agent doesn't exist → Severe
- Script imports non-existent module → Fatal

**Consistency:**
- Same concept: 'task' vs 'job' → Warning
- Rule R3 referenced but undefined → Severe

### Should NOT Flag

**License/Copyright:**
- Fixed license header → Intentional
- Brand identifier → Design requirement

**Size (Tiered):**
- 504/500 lines (0.8% over) → **NOT an issue**
- 520/500 lines (4% over) → **NOT an issue**
- 550/500 lines (10% over) → Info at most
- 590/500 lines (18% over) → Info only

**Design Choices:**
- `cmds/` instead of `commands/` → Valid
- Different organization → Design choice

**AI Capability:**
- No JSON explanation → AI knows
- Assumes markdown knowledge → AI knows

**Optional:**
- Missing version → Optional
- No README.md → Optional
