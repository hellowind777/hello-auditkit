---
name: hello-auditkit
description: This skill should be used when the user asks to "audit a plugin", "audit prompts", "review AGENTS.md", "review CLAUDE.md", "audit skills", "review plugin structure", "validate components", "check quality", "analyze hooks/agents/skills/commands", "check against design requirements", "audit templates", "review rules", or needs comprehensive assessment of AI coding assistant configurations, prompt quality, and best practices compliance.
version: 1.0.1
---

<!-- ============ OUTPUT LANGUAGE CONFIGURATION ============ -->
<!-- Change the value below to set audit report output language -->
<!-- Supported: en (English), zh (中文), ja (日本語), ko (한국어), es (Español), fr (Français), de (Deutsch) -->

**OUTPUT_LANGUAGE: zh**

<!-- ======================================================= -->

> **IMPORTANT**: All audit output MUST be in the language specified by OUTPUT_LANGUAGE above. This includes all section headers, descriptions, issue explanations, and suggestions.

# Hello-AuditKit: AI Coding Assistant Audit System

## Overview

Comprehensive audit system for AI coding assistant configurations, supporting multiple content types:

| Content Type | Description | Identification |
|--------------|-------------|----------------|
| **Prompts** | Standalone LLM prompts | Any text/markdown prompt |
| **AGENTS.md** | Codex agent instructions | `AGENTS.md` file |
| **CLAUDE.md** | Claude Code memory files | `CLAUDE.md` file |
| **GEMINI.md** | Gemini CLI context files | `GEMINI.md` file |
| **Skills** | Claude/Codex skills | Directory containing `SKILL.md` |
| **Plugins** | Claude Code plugins | Directory with `.claude-plugin/plugin.json` |
| **Composite Systems** | Memory file + Skills | `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` + `skills/` |

### Skills Definition

> Source: Codex skill-creator official documentation

**A skill is any directory containing a `SKILL.md` file.** Skills consist of:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown body: instructions (required)
└── Bundled Resources (optional)
    ├── scripts/      - Executable code (Python/Bash/etc.)
    ├── references/   - Documentation loaded into context as needed
    └── assets/       - Files used in output (templates, icons, etc.)
```

**Key points:**
- `scripts/`: For deterministic, reusable code (e.g., `rotate_pdf.py`)
- `references/`: For documentation Codex reads when needed (schemas, API docs, domain knowledge)
- `assets/`: For output resources not loaded into context (templates, images, fonts)
- References should be one level deep from SKILL.md (avoid nested references)
- Files >100 lines should have table of contents
- Do NOT include: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc.

When auditing a directory, recursively find all `SKILL.md` files and audit each skill including its scripts, references, and assets.

## Audit Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| **Prompt Mode** | Single prompt file/text | Audit standalone prompts |
| **AGENTS.md Mode** | `AGENTS.md` file alone | Audit Codex agent instructions |
| **CLAUDE.md Mode** | `CLAUDE.md` file alone | Audit Claude memory files |
| **GEMINI.md Mode** | `GEMINI.md` file alone | Audit Gemini context files |
| **Skills Mode** | Directory containing `SKILL.md` file(s) | Audit all skills found |
| **Plugin Mode** | Directory with `.claude-plugin/` | Full plugin audit |
| **Memory + Skills** | `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` + `skills/` | Memory file + skills audit |
| **Memory + Plugin** | `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` + `.claude-plugin/` | Memory file + plugin audit |

**Auto-detection rules:**
- Single `.md` file with prompt content → Prompt Mode
- File named `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` alone → Respective Memory Mode
- Directory containing any `SKILL.md` → Skills Mode (audit all found)
- Directory with `.claude-plugin/plugin.json` → Plugin Mode
- Directory with memory file + `skills/` subdirectory → Memory + Skills
- Directory with memory file + `.claude-plugin/` → Memory + Plugin

**Important: Content-Based Audit**

Audit is based on the content user provides (file, directory, or pasted text), NOT limited to specific system paths. User may:
- Provide files copied to any location for review
- Paste content directly
- Point to any directory structure

Focus on auditing the **content quality** itself. Path/location checks are informational only - they help understand intended usage but should not fail the audit if content is in a non-standard location.

### Design Requirements Review (Optional)

User can provide original design requirements or PRD document along with ANY audit mode. When provided:

1. **Standard audit** - Perform normal audit based on detected mode
2. **Design alignment check** - Additionally evaluate:
   - Does implementation match stated design goals?
   - Are all intended features implemented?
   - Are trigger conditions aligned with intended use cases?
   - Any scope creep (unintended features)?
   - Any missing capabilities vs design intent?

**How to use**: User provides both:
- Content to audit (path, directory, or pasted content)
- Design requirements (brief description, detailed paragraph, or formal PRD)

The audit report will include a "Design Alignment" section comparing implementation against stated requirements.

## Core Principles

### Principle 1: Explicit Over Implicit (GPT-5 Best Practice)

> Source: GPT-5.2 Prompting Guide

- Articulate preferences clearly rather than relying on defaults
- Use explicit scope, verbosity, and format constraints
- Favor correctness and grounding; add self-check steps for high-risk outputs
- "If any instruction is ambiguous, choose the simplest valid interpretation"

### Principle 2: Verbosity Control

**Default constraints:**
- Simple responses: ≤2 sentences
- Standard responses: 3-6 sentences or ≤5 bullets
- Complex tasks: 1 overview paragraph + ≤5 tagged bullets

**Scope discipline:**
- "Implement EXACTLY and ONLY what the user requests"
- "No extra features, no added components, no UX embellishments"

### Principle 3: Occam's Razor Applied Correctly

**Do not add entities without necessity.**

- **Don't over-simplify**: Ensure optimized language remains professional, accurate, and complete
- **Balanced attitude**: Find real issues without false positives
- **Respect design choices**: Distinguish "design flaws" from "design choices"
- **Conservative modifications**: Prefer modifying existing rules over adding new ones

### Principle 4: Progressive Loading Design

| Level | Content | Load Timing | Size Guidance |
|-------|---------|-------------|---------------|
| Level 1 | Metadata (name + description) | **Always in context** | ~100 words |
| Level 2 | Main content (body) | **When triggered** | <500 lines |
| Level 3 | Bundled resources | **On demand** | Unlimited |

### Principle 5: Hallucination Prevention

- Ask 1-3 clarifying questions OR present 2-3 interpretations with labeled assumptions
- Use hedging language: "Based on the provided context..." instead of absolutes
- Never fabricate exact figures or references when uncertain
- Set missing fields to null rather than guessing

### Principle 6: AI Capability Assumptions

**AI CAN understand**: Common synonyms, clear contextual references, standard terminology
**AI CANNOT reliably understand**: Cross-section implicit relationships, 3+ step inference chains, domain-specific term variations

**Balance Principle for Issue Identification:**
1. Identify issues first, then verify if AI capability exempts them
2. If removing a constraint causes ≥30% of AI executors to misunderstand → Flag as issue
3. If removing a constraint causes <30% to misunderstand → Can exempt
4. When uncertain, prefer keeping constraints and mark as "optimization suggestion"

### Principle 7: Platform-Specific Rules

When Claude and Codex specifications conflict, apply the **most appropriate** rule based on:
1. Target platform (if known)
2. Best practice alignment
3. Practical effectiveness

Do NOT flag as issues when both approaches are valid.

## Content-Specific Audit Rules

### Prompt Audit Rules

| Check | Requirement | Severity |
|-------|-------------|----------|
| Verbosity constraints | Explicit length limits | Warning |
| Scope boundaries | Clear "do not" constraints | Warning |
| Ambiguity handling | Instructions for unclear cases | Info |
| Output format | Specified structure | Warning |
| Grounding | "Based on context" hedging | Info |

### AGENTS.md Audit Rules

| Check | Requirement | Severity |
|-------|-------------|----------|
| Merge hierarchy | Respects top-down merge (global → repo → cwd) | Info |
| Instruction clarity | Clear, actionable instructions | Warning |
| Scope appropriateness | Instructions match file location scope | Warning |
| No conflicts | No contradictory instructions across levels | Severe |

### CLAUDE.md Audit Rules

| Check | Requirement | Severity |
|-------|-------------|----------|
| Memory type location | Correct location for memory type | Info (advisory) |
| Import syntax | Valid `@path/to/file` imports | Fatal |
| Path-specific rules | Valid YAML frontmatter with `paths` field | Severe |
| Bullet format | Uses bullet points and markdown headings | Info |
| Specificity | Specific instructions, not vague | Warning |

### GEMINI.md Audit Rules

> Source: Gemini CLI official documentation

| Check | Requirement | Severity |
|-------|-------------|----------|
| File hierarchy | Correct hierarchy (global/project/subdirectory) | Info (advisory) |
| Import syntax | Valid `@file.md` imports (relative or absolute) | Fatal |
| Markdown format | Standard markdown with headings, lists, code blocks | Info |
| Instruction clarity | Clear, actionable instructions | Warning |
| Specificity | Specific instructions, not vague | Warning |
| No conflicts | No contradictory instructions across hierarchy | Severe |

**GEMINI.md hierarchy:**
1. Global: `~/.gemini/GEMINI.md`
2. Project root/ancestors: Up to `.git` folder
3. Subdirectories: Below current directory (respects `.gitignore`)

### Skill Audit Rules (Claude + Codex Unified)

**Skill as a Whole** (audit entire skill directory):
| Check | Requirement | Severity |
|-------|-------------|----------|
| SKILL.md exists | Required in skill root | Fatal |
| Directory structure | scripts/, references/, assets/ if used | Info |
| No extraneous files | No README.md, CHANGELOG.md, etc. | Warning |
| All references accessible | Files in references/ exist and readable | Severe |
| All scripts valid | Scripts in scripts/ are executable, have proper shebang | Warning |
| Reference depth | References one level deep (no nested references) | Warning |
| Large files have TOC | Files >100 lines have table of contents | Info |

**SKILL.md Content**:
| Check | Requirement | Severity |
|-------|-------------|----------|
| File name | `SKILL.md` (case-sensitive) | Fatal |
| name field | ≤64 chars, lowercase letters, digits, hyphens | Severe |
| description field | Required, ≤1024 chars (≤500 recommended), includes when skill should trigger | Severe |
| Body length | ≤500 lines, <5k words ideal; >750 lines needs optimization | Warning |
| References documented | SKILL.md describes when to read each reference file | Warning |
| allowed-tools | Valid tool names if specified | Severe |

**Scripts Audit** (for each script in scripts/):
| Check | Requirement | Severity |
|-------|-------------|----------|
| Shebang line | Present and correct | Warning |
| Error handling | Proper error handling (set -e or try/except) | Warning |
| Referenced in SKILL.md | Script usage documented | Info |

**References Audit** (for each file in references/):
| Check | Requirement | Severity |
|-------|-------------|----------|
| Referenced in SKILL.md | Clear "when to read" instructions | Warning |
| No duplication | Info not duplicated in SKILL.md | Info |
| TOC for large files | Files >100 lines have table of contents | Info |

**Cross-Skill Checks** (when multiple skills in directory):
| Check | Requirement | Severity |
|-------|-------------|----------|
| No trigger conflicts | Skills have distinct trigger conditions | Warning |
| Shared resources | All skills can access shared scripts/files | Severe |
| Cross-references | Valid paths between skills | Severe |

### Plugin Audit Rules (Claude Code)

> Audit entire plugin directory as a whole, including all component types

**Plugin Structure** (directory level):
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json (required - manifest)
├── commands/        - Slash commands (.md files)
├── agents/          - Subagent definitions (.md files)
├── skills/          - Skills (directories with SKILL.md)
├── hooks/
│   └── hooks.json   - Hook configurations
├── .mcp.json        - MCP server definitions
├── .lsp.json        - LSP server configurations
├── scripts/         - Utility scripts
├── rules/           - Rule files (.md)
└── templates/       - Template files
```

**Plugin-Level Checks**:
| Check | Requirement | Severity |
|-------|-------------|----------|
| plugin.json exists | In `.claude-plugin/` directory | Fatal |
| plugin.json valid | Valid JSON, required fields present | Fatal |
| name format | kebab-case | Severe |
| Component dirs at root | Not inside `.claude-plugin/` | Fatal |
| Path references | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |

**Component-Level Checks** (audit each by its own rules):
| Component | Location | Audit Rules |
|-----------|----------|-------------|
| Commands | `commands/*.md` | Command audit rules |
| Agents | `agents/*.md` | Agent audit rules |
| Skills | `skills/*/SKILL.md` | Skill audit rules (full skill audit) |
| Hooks | `hooks/hooks.json` | Hook audit rules |
| MCP Servers | `.mcp.json` | MCP audit rules |
| LSP Servers | `.lsp.json` | LSP audit rules |
| Scripts | `scripts/*` | Script audit rules |
| Rules | `rules/*.md` | Prompt/rule audit rules |

**Cross-Component Checks**:
| Check | Requirement | Severity |
|-------|-------------|----------|
| All references valid | Commands→agents, agents→skills, etc. | Severe |
| hooks.json format | `{"hooks": {...}}` wrapper | Fatal |
| Script references | All referenced scripts exist | Fatal |
| Naming consistency | Consistent across all components | Warning |

### Composite System Audit Rules

| Check | Requirement | Severity |
|-------|-------------|----------|
| AGENTS.md + skills consistency | No conflicting instructions | Severe |
| Script references | All referenced scripts exist | Fatal |
| Script quality | Proper shebang, error handling | Warning |
| Cross-file references | Valid paths, no broken links | Severe |
| Naming consistency | Consistent naming across files | Warning |

## Audit Dimensions (Priority Order)

| Priority | Dimension | Description |
|----------|-----------|-------------|
| 0 | Structure | File/directory structure, naming conventions |
| 0.1 | Cross-Component Consistency | References, naming across files |
| 1 | Fatal Issues | Logic contradictions, missing critical components |
| 2 | Severe Issues | Unclear descriptions, broken references |
| 3 | Semantic Ambiguity | Inconsistent terminology |
| 4 | Expression Standards | Redundancy, formatting |
| 4.1 | Conciseness | Unnecessary explanations |
| 4.2 | Freedom Level Mismatch | Over/under-constrained |
| 5 | Structure Issues | Organization, hierarchy |
| 6 | Robustness | Error handling, edge cases |
| 7 | Optimization Suggestions | Optional improvements |
| 7.1 | LLM Prompting Best Practices | GPT-5 guidelines compliance |
| 8 | Architecture Review | Optional, on request |

## Audit Execution

### Step 1: Content Type Detection

1. Scan provided path/content
2. Identify content type (Prompt/AGENTS.md/CLAUDE.md/Skill/Plugin/Composite)
3. Confirm audit mode with user
4. For Composite Mode, list all detected components

### Step 2: Comprehensive Scan

**For Composite Mode (AGENTS.md + Skills + Scripts):**
1. Scan AGENTS.md structure and content
2. Scan each skill in skills/ directory
3. Scan all scripts (*.sh, *.py, etc.)
4. Check cross-component consistency
5. Infer design intent
6. Apply general dimensions (1-8)

**For other modes:** Apply content-specific rules + general dimensions

### Step 3: Issue Verification (4-Point Checklist)

For each suspected issue:
1. **Concrete Scenario Test**: Does this cause clear negative consequences?
2. **Design Scope Verification**: Is this within design scope?
3. **Design Intent Judgment**: Is this a flaw or a choice?
4. **Severity Assessment**: Does it meet threshold?

### Step 4: Generate Report

- Output in configured language
- Create file(s) if report exceeds ~300 lines
- Include fix suggestions with Before/After comparisons

## Output Format

Read `references/output-format-core.md` and `references/output-format-issues.md` for complete specifications.

**Language**: Output in the language specified by `OUTPUT_LANGUAGE` at the top of this file.

**File Output**: If report exceeds ~300 lines, create file(s). See `references/output-format-core.md` for naming rules.

## Reference Files

1. **`references/plugin-structure-spec.md`** - Plugin structure specifications
2. **`references/memory-file-rules.md`** - Prompts, AGENTS.md, CLAUDE.md, GEMINI.md audit rules
3. **`references/component-audit-rules.md`** - Commands, Agents, Skills audit rules
4. **`references/plugin-hooks-rules.md`** - Plugin System, Hooks, Hook Scripts audit rules
5. **`references/mcp-lsp-rules.md`** - MCP Servers, LSP Servers audit rules
6. **`references/cross-audit-rules.md`** - Design Requirements, Cross-Component, Composite System audit rules
7. **`references/audit-verification-principles.md`** - Issue verification checklist and AI capability assumptions
8. **`references/audit-checklist-dimensions.md`** - Dimension 0-8 audit checklist with severity levels
9. **`references/audit-checklist-examples.md`** - Examples of what should/should not be flagged
10. **`references/output-format-core.md`** - Output format: language, structure, component templates
11. **`references/output-format-issues.md`** - Output format: issues, summary, user confirmation
12. **`references/output-format-special.md`** - Special outputs (design alignment, terminology, architecture)
13. **`references/prompt-best-practices.md`** - GPT-5 and LLM prompting best practices

## Special Reminders

**Avoid False Positives**
- Don't flag valid design choices as issues
- Don't assume rules that don't exist
- Respect platform differences (Claude vs Codex)

**Avoid Over-interpretation**
- Don't treat simplification as omission
- Don't treat flexibility as ambiguity
- Don't treat style differences as inconsistency

**Platform Compatibility**
- When auditing skills, apply unified best practices
- Don't flag Claude-specific or Codex-specific patterns as errors
- Focus on practical effectiveness over strict compliance

## Reference Documentation

**Prompt Engineering:**
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [OpenAI Platform Docs](https://platform.openai.com/docs)
- [Anthropic Documentation](https://docs.anthropic.com)
- [Google AI Documentation](https://ai.google.dev/docs)

**Codex CLI:**
- [Codex CLI Repository](https://github.com/openai/codex)
- [Codex CLI Docs](https://github.com/openai/codex/tree/main/docs)

**Claude Code:**
- [Claude Code Repository](https://github.com/anthropics/claude-code) - Official source for plugins, hooks, MCP, agents
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

**Gemini CLI:**
- [Gemini CLI Repository](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI Docs](https://github.com/google-gemini/gemini-cli/tree/main/docs)
