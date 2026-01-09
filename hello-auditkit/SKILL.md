---
name: hello-auditkit
description: This skill should be used when the user wants to audit, review, validate, analyze, or check the quality of AI coding assistant configurations. Use this skill for examining prompts, memory files (AGENTS.md, CLAUDE.md, GEMINI.md), skills, plugins, hooks, commands, agents, templates, or rules. This includes any request related to quality assessment, best practices compliance, design review, structure validation, issue detection, or comprehensive evaluation of AI assistant components and configurations.
version: 2.0.0
---

<!-- ============ OUTPUT LANGUAGE CONFIGURATION ============ -->
<!-- Supported: en-US, zh-CN, zh-TW, ja-JP, ko-KR, es-ES, fr-FR, de-DE -->

**OUTPUT_LANGUAGE: zh-CN**

<!-- ======================================================= -->

> **IMPORTANT**: All audit output MUST be in the language specified above.

# Hello-AuditKit: AI Coding Assistant Audit System

## Overview

Comprehensive audit system for AI coding assistant configurations:

| Content Type | Identification | Rule File |
|--------------|----------------|-----------|
| **Prompts** | Any text/markdown prompt | `type-prompt.md` |
| **AGENTS.md** | Codex agent instructions | `type-memory.md` |
| **CLAUDE.md** | Claude Code memory files | `type-memory.md` |
| **GEMINI.md** | Gemini CLI context files | `type-memory.md` |
| **Skills** | Directory with `SKILL.md` | `type-skill.md` |
| **Plugins** | Directory with `.claude-plugin/` | `type-plugin.md` |
| **Composite** | Memory file + skills/ | `cross-composite.md` |

## Core Principles

> **Source**: Based on Latest GPT Prompting Guide (openai-cookbook/examples/gpt-5)

### Principle 1: 4-Point Verification

Before marking ANY issue, verify:
1. **Concrete Scenario** - Can describe specific failure?
2. **Design Scope** - Within intended boundaries?
2b. **Functional Capability** - Can it actually do what it claims? (Requires domain knowledge first)
3. **Flaw vs Choice** - Unintentional error or valid choice?
4. **Threshold Met** - Above quantified threshold?

If ANY fails → Discard the issue

### Principle 2: Occam's Razor

**"If unnecessary, don't add."**

Fix Priority: DELETE > MERGE > RESTRUCTURE > MODIFY > ADD

### Principle 3: AI Capability

- AI CAN infer: synonyms, context, standard terms
- AI CANNOT: 3+ step inference, domain-specific variations
- If <30% would misunderstand → exempt from issue

### Principle 4: Size Tolerance (SKILL.md body only)

| Range | Status |
|-------|--------|
| ≤500 lines | Ideal |
| 500-550 (≤10% over) | **NOT an issue** |
| 550-625 (10-25% over) | Info only |
| >625 lines | Warning |

> **Note**: Reference files have no official line limit. Evaluate based on content nature.

### Principle 5: Prompt Compliance

**For prompts/instructions, verify critical checks** (see `type-prompt.md` → Prompt Compliance Checks):
- Verbosity constraints (Severe)
- Scope boundaries with "do not" list (Severe)
- No fabrication instruction (Severe)
- Output schema for structured tasks (Warning)

## Audit Execution

> **CRITICAL**: Each step below is MANDATORY. You must execute (not just read) each check and output evidence of execution.

### Step 0: Fetch Latest Prompting Guide (For Prompt-Containing Content)

**When auditing content containing AI instructions** (Prompts, Memory files, Skills, Plugins):

1. Fetch latest GPT prompting guides from: `https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5`
2. Cross-validate with built-in checks in `type-prompt.md`
3. Apply any new/updated practices found in the latest guide

**Evidence Output**: Note guide version fetched and any new checks applied.

**If WebFetch unavailable**: Use built-in checks, note "offline mode" in report.

### Step 1: Detection & Classification

Scan path → identify type → load appropriate rules:

```
Prompt       → type-prompt.md
Memory file  → type-memory.md
Skill        → type-skill.md
Plugin       → type-plugin.md
Composite    → Apply all + cross-*.md
```

### Step 2: Execute Universal Checks (ALL TYPES)

**Every audit MUST execute these checks from `rules-universal.md`:**

| Category | Action Required | Evidence Output |
|----------|-----------------|-----------------|
| Naming & Numbering | Extract ALL: (1) naming conventions (kebab-case, no special chars), (2) numbered sequences → verify sequential, no duplicates, no gaps, (3) order validation → section order logical, heading hierarchy H1→H2→H3 | "Checked N sequences, M naming issues, K order issues" |
| Reference Integrity | Extract ALL references (file refs, anchor links, numbered refs like R1/Step 2) → verify each target exists, no circular refs | "Checked N refs, M broken, K circular" |
| Structure & Organization | (1) TOC-content match, (2) section categorization correct, (3) template compliance (required sections present, order correct), (4) no orphan sections | "TOC: N entries vs M headings, K mismatches; Template: L issues" |
| Diagram & Flowchart | If exists: (1) node-text consistency, (2) all paths have endpoints, (3) no infinite loops, (4) decision branches complete | "Checked N diagrams, M consistency issues, K logic issues" |
| Language Expression | (1) Ambiguity patterns (may/might/could without condition), (2) terminology consistency (same concept = same term), (3) spelling errors in identifiers/headings, (4) redundant content, (5) LLM wording patterns (hedging language, avoid absolutes, scope constraint wording, verbosity constraint wording) | "Found N ambiguity, M terminology, K spelling, L redundancy, P wording issues" |
| Security & Compliance | Check for hardcoded secrets, paths, credentials; input validation rules | "Checked, N security issues" |
| Size Thresholds | SKILL.md body: apply tiered thresholds (≤500 ideal). Reference files: evaluate by content nature | "SKILL.md: N lines (status)" |
| Rule Logic | If rules exist: (1) no conflicts, (2) no duplicates/semantic equivalents, (3) coverage complete, (4) optimization opportunities (DELETE > MERGE > MODIFY) | "Checked N rules: M conflicts, K duplicates, L gaps" |
| Process Logic | If process/flow defined: (1) all scenarios covered, (2) main flow clear, (3) no dead loops, (4) no conflicting invocations | "Process: N scenarios, M flow issues" |
| Output & i18n | If output format defined: (1) format specification complete, (2) language control correct (if i18n configured), (3) no hardcoded language-specific content | "Output: N format issues, M i18n issues" |
| Prompt Compliance | (1) Verbosity constraints present, (2) Scope boundaries with "do not" list, (3) No fabrication instruction, (4) Output schema for structured tasks, (5) Grounding for uncertain claims, (6) Tool preference over internal knowledge, (7) Agentic updates brief with concrete outcomes, (8) Long-context outline for >10k tokens | "Prompt: N verbosity, M scope, K grounding, L tool, P agentic issues" |

**Numbering Check Execution** (commonly missed):
1. Find all numbered lists (1. 2. 3. or Step 0, Step 1, etc.)
2. Verify: sequential? no duplicates? no gaps?
3. Find all TOC entries → verify each has matching heading
4. Cross-section: if steps span sections (Step 0 here, Step 3 there), verify continuity

### Step 3: Execute Type-Specific Checks

**Based on content type, execute ALL checks in the relevant file:**

#### For Prompts (`type-prompt.md`):
| Check Category | Action |
|----------------|--------|
| Structure Validation | Verbosity constraints? Scope boundaries? Output format? |
| Content Quality | Specific instructions? Not vague? |
| LLM Best Practices | Freedom level match? Grounding? Ambiguity handling? |
| Prompt Compliance | Verbosity limits? "Do not" list? No fabrication? Schema? Self-check? |
| Audit Checklist | Execute all Fatal/Severe/Warning checks at end of file |

#### For Memory Files (`type-memory.md`):
| Check Category | Action |
|----------------|--------|
| Structure Validation | File location? Merge hierarchy? |
| Import Syntax | Valid `@path` imports? |
| Content Quality | Specific? Actionable? Not vague? |
| Instruction Quality | Verbosity constraints? Scope boundaries? |

#### For Skills (`type-skill.md`):
| Check Category | Action |
|----------------|--------|
| Directory Validation | SKILL.md exists? Correct filename? |
| Frontmatter | name, description, triggers present? |
| Body Size | SKILL.md: ≤500 ideal, >625 warning. References: no limit, evaluate by content |
| Script Integrity | Declared scripts exist? Imports valid? Shebang? Error handling? |
| References | Has "when to read" guidance? |

#### For Plugins (`type-plugin.md`):
| Check Category | Action |
|----------------|--------|
| Structure | plugin.json in .claude-plugin/? Components at root? |
| Path Variables | Uses relative paths or env variables? No hardcoded absolute paths? |
| Commands | Valid frontmatter? allowed-tools valid? |
| Agents | name, description, tools valid? |
| Hooks | Wrapper format? Valid matchers? Scripts exist? |
| MCP/LSP | Valid JSON? Paths correct? No hardcoded secrets? |

### Step 4: Execute Cross-Cutting Checks (Multi-file Systems)

**For Skills, Plugins, Composites, execute ALL checks from:**

#### From `cross-design-coherence.md`:
| Check | Action |
|-------|--------|
| Full Directory Scan | Enumerate ALL files, classify each, build rule inventory |
| Design Philosophy | Extract principles from all files, check consistency |
| Rule Propagation | Global rules applied in local files? |
| Conflict Detection | Same-file contradictions? Cross-file contradictions? |
| Structural Redundancy | Repeated sections? Duplicate tables? Parallel content? → centralize |
| Red Flags | SKILL.md >625 lines? Scattered rules (>3 files)? Circular deps? |

#### From `cross-progressive-loading.md`:
| Check | Action |
|-------|--------|
| Content Level Audit | L1 ≤100 words? L2 ≤500 lines? L3: evaluate by content nature |
| Content Placement | Core workflow in L2? Edge cases in L3? |
| Reference Guidance | Each reference has "when to read"? |
| Anti-Patterns | Metadata bloat? Monolithic body? Essential in L3? |

#### From `cross-composite.md`:
| Check | Action |
|-------|--------|
| Reference Integrity | All cross-file refs valid? |
| Terminology Consistency | Same concept = same term across files? |
| Numbering Consistency | Sequential across all files? No duplicates? |
| Script Integrity | All declared scripts exist? Imports valid? |

### Step 5: Issue Verification (4-Point Check)

For each suspected issue, verify ALL points:
1. **Concrete scenario** - Can describe specific failure?
2. **Design scope** - Within intended boundaries?
2b. **Functional capability** - Does implementation match claimed capability?
3. **Flaw vs choice** - Unintentional error or valid design?
4. **Threshold met** - Above quantified threshold?

If ANY fails → Discard the issue (move to Filtered)

### Step 6: Generate Report

Follow `references/ref-output-format.md` for structure.

**Section 2 Cross-Cutting Analysis MUST include:**
- Naming & Numbering: actual check results with specific findings
- TOC-Content Match: comparison results
- Reference Integrity: broken refs listed
- (For multi-file) Design Coherence, Progressive Loading results

**Section 3 Issue Inventory MUST include:**
- Verification Statistics: "Scanned X → Verified Y → Filtered Z"
- Both Confirmed and Filtered issues with filter reasons

## Reference Files

### Layer 0: Core Methodology (永恒不变)

Read `references/methodology-core.md` when:
- Need to verify if something is truly an issue
- Deciding fix priority
- Understanding AI capability boundaries

### Layer 1: Universal Rules (通用规则)

Read `references/rules-universal.md` when:
- Starting any audit
- Need Should Flag / Should NOT Flag patterns
- Checking size thresholds

### Layer 2: Type-Specific Rules (类型规则)

| File | Read When |
|------|-----------|
| `references/type-prompt.md` | Auditing standalone prompts |
| `references/type-memory.md` | Auditing AGENTS.md, CLAUDE.md, GEMINI.md |
| `references/type-skill.md` | Auditing skills (SKILL.md, scripts) |
| `references/type-plugin.md` | Auditing plugins, hooks, MCP, LSP |

### Layer 3: Cross-Cutting Rules (跨切规则)

| File | Read When |
|------|-----------|
| `references/cross-composite.md` | Auditing multi-component systems |
| `references/cross-design-coherence.md` | Checking design consistency |
| `references/cross-progressive-loading.md` | Evaluating content placement |

### Layer 4: Reference Materials (参考资料)

| File | Read When |
|------|-----------|
| `references/ref-output-format.md` | Generating audit report |
| `references/ref-checklist.md` | Need dimension checklist |
| `references/ref-quick-reference.md` | Quick lookup of patterns |

## Special Reminders

### Key References by Topic

| Topic | Reference File |
|-------|---------------|
| Report structure & format | `ref-output-format.md` |
| Issue filtering rules | `rules-universal.md` → Should NOT Flag |
| False positive prevention | `rules-universal.md` → Verification Questions |
| Size thresholds | `rules-universal.md` → Universal Size Thresholds |
| Checklist by dimension | `ref-checklist.md` |
| LLM prompting best practices | `type-prompt.md` → LLM Prompting Best Practices |

### Quick Filtering Rules

| Condition | Action |
|-----------|--------|
| ≤10% over recommended | NOT an issue |
| AI can infer | NOT an issue |
| Design choice | NOT an issue |

## External Documentation

| Platform | Source |
|----------|--------|
| Claude Code | github.com/anthropics/claude-code |
| Codex CLI | github.com/openai/codex/tree/main/codex-cli |
| Gemini CLI | github.com/google-gemini/gemini-cli |
| Anthropic Docs | docs.anthropic.com |
| OpenAI Docs | github.com/openai/openai-cookbook |
| GPT Prompting Resources | github.com/openai/openai-cookbook/tree/main/examples/gpt-5 |

> **Version Policy**: Always use the **latest version** of GPT prompting guides as authoritative source. When multiple versions exist in the gpt-5 directory, prefer the highest version number (e.g., gpt-5.2 over gpt-5.1 over gpt-5). The directory contains prompting guides, troubleshooting guides, and optimization cookbooks.
