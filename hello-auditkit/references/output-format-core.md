# Audit Output Format - Core

## Table of Contents

- [Language and Output Mode](#language-and-output-mode)
- [Output Structure Overview](#output-structure-overview)
- [1. Audit Type Identification](#1-audit-type-identification)
- [2. Plugin Structure Check](#2-plugin-structure-check)
- [3. Component Audit Results](#3-component-audit-results)

---

## Language and Output Mode

### Output Language Rule

**CRITICAL**: Check the `OUTPUT_LANGUAGE` setting in the main SKILL.md file. ALL audit output MUST be in the specified language:
- `en` → English
- `zh` → 中文 (Chinese)
- `ja` → 日本語 (Japanese)
- `ko` → 한국어 (Korean)
- `es` → Español (Spanish)
- `fr` → Français (French)
- `de` → Deutsch (German)

This applies to: section headers, descriptions, issue explanations, suggestions, and all other text output.

### File Output Rules

**When to output to file(s)**:
- If the audit report exceeds ~300 lines or ~15KB, create a file instead of inline output
- For Full Plugin Mode with many components, always create file(s)

**File naming convention**:
- Single file: `audit-report-{plugin-name}-{YYYYMMDD}.md`
- Multiple files (if single file would exceed ~500 lines):
  - `audit-report-{plugin-name}-{YYYYMMDD}-part1-structure.md`
  - `audit-report-{plugin-name}-{YYYYMMDD}-part2-components.md`
  - `audit-report-{plugin-name}-{YYYYMMDD}-part3-issues.md`
  - `audit-report-{plugin-name}-{YYYYMMDD}-part4-summary.md`

**File location**: Same directory as the audited plugin, or current working directory if auditing pasted content.

**Inline summary**: When creating file(s), output a brief inline summary:
```
## 审计完成 / Audit Complete

审计报告已保存至 / Report saved to:
- [file path(s)]

快速摘要 / Quick Summary:
- 发现问题 / Issues found: X
- 严重程度 / Severity: [Fatal: X, Severe: Y, Warning: Z]
- 建议优先修复 / Priority fix: [brief description]
```

---

## Output Structure Overview

```
1. Audit Type Identification (Required, First)
2. Plugin Structure Check (Full Plugin Mode)
3. Component Audit Results (By type)
4. Issue Classification (By severity)
5. Verification Statistics (Required)
6. Audit Summary (If issues found)
7. User Confirmation (If issues found)
8. Modified Content (After user approval)
```

---

## 1. Audit Type Identification

**Output position**: First section, before all other output

```markdown
---
## Audit Type Identification

**Audit Mode**: [Single Component / Full Plugin / PRD]

**Target**: [Path or file name]

**Components Detected**: (Full Plugin Mode only)
- plugin.json: ✅ Found
- commands/: X files
- agents/: X files
- skills/: X skills
- hooks/: ✅/❌
- .mcp.json: ✅/❌

**Audit Scope**: [Description of what will be audited]
---
```

---

## 2. Plugin Structure Check (Full Plugin Mode)

### 2.1 Manifest Check

```markdown
---
## Plugin Manifest Check

| Check Item | Current Value | Status | Notes |
|------------|---------------|--------|-------|
| `.claude-plugin/` exists | Yes/No | ✅/❌ | [Notes] |
| plugin.json location | [Path] | ✅/❌ | Must be in .claude-plugin/ |
| name field | [Value] | ✅/❌ | Required, non-empty |
| name format | [kebab-case/other] | ✅/⚠️ | Should be kebab-case |
| name length | X chars | ✅/⚠️ | ≤50 recommended |
| version field | [Value] | ✅/⚠️/- | Optional, semver format |
| description field | [Value] | ✅/⚠️/- | Optional, ≤200 chars |

**Conclusion**: ✅ Manifest valid / ❌ Issues found
---
```

### 2.2 Directory Structure Check

```markdown
---
## Directory Structure Check

| Check Item | Status | Notes |
|------------|--------|-------|
| Components at root level | ✅/❌ | Not inside .claude-plugin/ |
| commands/ structure | ✅/⚠️/- | [X .md files found] |
| agents/ structure | ✅/⚠️/- | [X .md files found] |
| skills/ structure | ✅/❌/- | [X SKILL.md files found] |
| hooks/ structure | ✅/❌/- | [hooks.json format] |
| .mcp.json | ✅/❌/- | [Valid JSON] |

**Path Reference Check**:
| Location | Uses ${CLAUDE_PLUGIN_ROOT} | Status |
|----------|---------------------------|--------|
| hooks.json | Yes/No | ✅/❌ |
| .mcp.json | Yes/No | ✅/❌ |
| [Other files] | Yes/No | ✅/❌ |

**Conclusion**: ✅ Structure valid / ❌ Issues found
---
```

### 2.3 Inferred Design Intent

```markdown
## Inferred Design Intent
**Plugin Purpose**: [One sentence summary]
**Target Users**: [Who this is for]
**Core Capabilities**: 1. [Primary] 2. [Secondary]
**Expected Use Cases**: [When user wants to...]
**Design Boundaries**: [What this is NOT for]
**Confidence Level**: [High/Medium/Low] - [Reason]
```

---

## 3. Component Audit Results

### 3.1 Commands Audit

```markdown
---
## Commands Audit

### command-name.md

| Check Item | Current Value | Status | Notes |
|------------|---------------|--------|-------|
| description | [Value] (X chars) | ✅/❌ | Required |
| argument-hint | [Value] | ✅/- | Optional |
| allowed-tools | [Value] | ✅/❌/- | Valid tool names |
| model | [Value] | ✅/❌/- | haiku/sonnet/opus |
| Body format | Instructions for Claude | ✅/❌ | Not user docs |
| Bash syntax | [Valid/Invalid] | ✅/❌ | If uses !`...` |

**Issues Found**: [List or "None"]
---
```

### 3.2 Agents Audit

```markdown
---
## Agents Audit

### agent-name.md

| Check Item | Current Value | Status | Notes |
|------------|---------------|--------|-------|
| name | [Value] (X chars) | ✅/❌ | Required, ≤50 chars |
| description | [Value] (X chars) | ✅/❌ | Required, ≤500 chars |
| Trigger conditions in description | Yes/No | ✅/❌ | Must include |
| tools | [Value] | ✅/❌/- | Valid tool names |
| model | [Value] | ✅/⚠️/- | haiku/sonnet/opus |
| Body quality | [Assessment] | ✅/⚠️ | Clear instructions |

**Issues Found**: [List or "None"]
---
```

### 3.3 Skills Audit

```markdown
---
## Skills Audit

### skill-name/SKILL.md

| Check Item | Current Value | Status | Notes |
|------------|---------------|--------|-------|
| File name | SKILL.md | ✅/❌ | Case-sensitive |
| name | [Value] (X chars) | ✅/❌ | ≤64 chars |
| description | [Value] (X chars) | ✅/❌ | ≤1024 chars (≤500 recommended) |
| Trigger conditions in description | Yes/No | ✅/❌ | Must include |
| version | [Value] | ✅/⚠️/- | Semver format |
| Body length | X lines | ✅/⚠️/❌ | ≤500 ideal, >750 needs work |
| Reference depth | X levels | ✅/❌ | Should be 1 |
| Unnecessary files | [List] | ✅/❌ | No README.md etc. |

**Issues Found**: [List or "None"]
---
```

### 3.4 Hooks Audit

```markdown
---
## Hooks Audit

### hooks/hooks.json

| Check Item | Current Value | Status | Notes |
|------------|---------------|--------|-------|
| Wrapper format | Yes/No | ✅/❌ | {"hooks": {...}} required |
| Valid JSON | Yes/No | ✅/❌ | Parseable |
| Event names valid | [List] | ✅/❌ | Known events only |
| Hook types valid | [List] | ✅/❌ | command/prompt |
| Path references | ${CLAUDE_PLUGIN_ROOT} | ✅/❌ | Portable paths |
| Scripts exist | [X/Y exist] | ✅/❌ | Referenced scripts |
| Timeouts set | Yes/No | ✅/⚠️ | Recommended |

**Script Validation**:
| Script | Exists | Shebang | Error Handling | Status |
|--------|--------|---------|----------------|--------|
| [script.sh] | ✅/❌ | ✅/❌ | ✅/⚠️ | ✅/❌ |

**Issues Found**: [List or "None"]
---
```

### 3.5 MCP Servers Audit

```markdown
---
## MCP Servers Audit

### .mcp.json

| Server Name | Type | Config Valid | Path Portable | Status |
|-------------|------|--------------|---------------|--------|
| [name] | http/command | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found**: [List or "None"]
---
```
