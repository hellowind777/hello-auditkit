# Audit Report Output Format

## Design Principles

1. **Single Conclusion**: Verdict appears ONLY in the final Conclusion section
2. **Full Transparency**: Show ALL issues (confirmed + filtered) with filter reasons
3. **Problem-Centric**: Each issue's analysis and fix together in one place
4. **Before/After Clarity**: All fixes use clear before/after comparison format
5. **No Repetition**: Each information appears once only (Occam's Razor)
6. **AI Executor Awareness**: Trust AI to understand context, don't over-specify
7. **Logical Flow**: Overview → Analysis → Issues → Solutions → Conclusion

---

## Report Structure

```
0. Header              - Basic info (NO verdict)
1. Assessment Overview - Rating, audit summary, coverage (score first)
2. Cross-Cutting       - Design coherence, progressive loading, references, etc.
3. Issue Inventory     - Statistics + 3.1 Confirmed + 3.2 Filtered
4. Fix & Optimization  - 4.1 Fix Proposals (🔴🟡) + 4.2 Optimization Proposals (🟢)
5. Conclusion          - Quality judgment, overall verdict, recommended actions (FINAL)
```

**Total: 6 sections (0-5)**

**Key Rules**:
- Section 1 shows rating, summary, and coverage (NO issue statistics here)
- Section 3 shows issue statistics + all issues (confirmed + filtered)
- Section 4 supports multiple proposals per issue (mark recommended with "Recommended")
- Section 5 ends with Recommended Actions table as the final report output

---

## Section Specifications

### 0. Header

**Required fields**: Target, Type, Date, Files, Lines

**Format**: Table with Item/Value columns

**Rules**:
- Maximum 5 rows
- NO verdict or assessment language

---

### 1. Assessment Overview

**Required subsections (in order)**:

#### Rating
Table with columns: Dimension | Score | Notes

**Rating Dimensions by Audit Type**:

| Type | Dim 1 | Dim 2 | Dim 3 | Dim 4 |
|------|-------|-------|-------|-------|
| Prompt | Clarity | Completeness | Accuracy | Usability |
| Memory | Organization | Completeness | Consistency | Effectiveness |
| Skill | Structure | Maintainability | Documentation | Robustness |
| Plugin | Architecture | Integration | Documentation | Extensibility |
| Composite | Coherence | Coverage | Consistency | Robustness |

#### Audit Type Results Summary
Table with columns: Audit Type | Files | Issues | Key Findings

**Audit types and checks by target**:

| Target | Audit Type | Key Checks |
|--------|------------|------------|
| Prompt | Structure | Verbosity, scope, format, ambiguity |
| Prompt | Content Quality | Clarity, completeness, accuracy |
| Prompt | LLM Best Practices | Grounding, constraints, tool usage |
| Prompt | Language Expression | Wording, fluency, terminology |
| Memory | Structure | File location, hierarchy |
| Memory | Import Syntax | Valid `@path` imports |
| Memory | Content Quality | Actionable instructions |
| Memory | Terminology | Consistent terms, defined concepts |
| Skill | Directory | SKILL.md exists, structure |
| Skill | SKILL.md | Frontmatter, body size, triggers |
| Skill | Scripts | Integrity, shebang, error handling |
| Skill | References | Size, "when to read", integrity |
| Skill | Naming & Numbering | Sequential, consistent format |
| Skill | Flowcharts | Diagram-text consistency, logic |
| Plugin | Manifest | plugin.json location, fields |
| Plugin | Commands | Frontmatter, allowed-tools, prompt quality |
| Plugin | Agents | Name, description, tools, body quality |
| Plugin | Hooks | Wrapper format, matchers, scripts |
| Plugin | MCP/LSP | Valid JSON, paths, secrets |
| Plugin | Security | No hardcoded secrets, path safety |
| Composite | Cross-Component | References, terminology, layering |
| Composite | Process Logic | Flow coverage, no dead loops |
| Composite | Rule Logic | No conflicts, no duplication |

#### Coverage Statistics
Table with columns: Category | Scanned | Verified | Filtered

**Rules**:
- NO verdict or conclusion
- NO issue statistics (moved to Section 3)
- Order: Rating → Summary → Coverage (score first)

---

### 2. Cross-Cutting Analysis

**Content varies by audit type. Include applicable subsections:**

| Audit Type | Applicable Subsections |
|------------|------------------------|
| Prompt | Content Assessment, LLM Best Practices, Language Expression, Size Check |
| Memory | Content Assessment, Instruction Quality, Import Syntax Check, Terminology Check, Size Check |
| Skill | Design Coherence, Progressive Loading, Naming & Numbering, Reference Integrity, Reference Loading Guidance, Flowchart Validation, Script Quality |
| Plugin | Structure Validation, Security Check, Design Coherence, Progressive Loading, Component Prompt Quality, Component Summary |
| Composite | All above + Audit Scope Summary, Cross-File Review, Process Logic, Rule Logic |

#### Prompt Subsections

**Content Assessment**: Table (Aspect | Status | Notes)
- Aspects: Goal Clarity, Instruction Flow, Edge Case Coverage, Ambiguity Handling

**LLM Best Practices**: Table (Practice | Status | Notes)
- Practices: Verbosity Constraints, Scope Boundaries, Output Format, Grounding, Freedom Level
- Per `type-prompt.md` LLM Prompting Best Practices section

**Language Expression**: Table (Check | Status | Notes)
- Checks: Clarity, Fluency, Ambiguity Patterns, Terminology Consistency
- Per `rules-universal.md` Language Expression Rules section

**Size Check**: Table (Metric | Actual | Limit | Status)

#### Memory Subsections

**Content Assessment**: Table (Aspect | Status | Notes)
- Aspects: Goal Clarity, Instruction Flow, Edge Case Coverage, Ambiguity Handling

**Instruction Quality**: Table (Check | Status | Notes)
- Checks: Verbosity Constraints, Scope Boundaries, Actionability, Freedom Level Match
- Per `type-prompt.md` LLM Prompting Best Practices (applies to memory file instructions)

**Import Syntax Check**: Table (Import | Valid | Status)
- Per `type-memory.md` Import Syntax section

**Terminology Check**: Table (Concept | Terms Used | Consistent | Status)
- Per `rules-universal.md` Terminology Consistency section

**Size Check**: Table (Metric | Actual | Limit | Status)

#### Skill Subsections

**Design Coherence**: Table (Principle | Status | Notes)
- Check principles from `cross-design-coherence.md`
- Include red flags if detected: god files, scattered rules, circular deps

**Progressive Loading**: Table (Level | Actual | Target | Status)
- Levels: L1-L4 per `cross-progressive-loading.md`
- Note anti-patterns if detected: metadata bloat, monolithic body, essential in L3

**Naming & Numbering**: Table (Check | Expected | Actual | Status)
- Checks: Sequential numbering, No duplicates, Format consistent, TOC-Content match
- Per `rules-universal.md` Numbering & Order Rules section

**Reference Integrity**: Table (Reference | Target | Exists | Status)
- Checks: Named refs, Numbered refs, Anchor links, Cross-file refs
- Per `rules-universal.md` Reference Integrity Rules section

**Flowchart Validation** (if diagrams exist): Table (Check | Status | Notes)
- Checks: Diagram-text consistency, All paths have endpoints, No infinite loops, Decision completeness
- Per `rules-universal.md` Diagram & Flowchart Rules section

**Script Quality** (if scripts exist): Table (Script | Type | Shebang | Error Handling | Dependencies | Status)
- Per `type-skill.md` Script Integrity Verification section
- Type column: Runtime/Dev/Helper (only Runtime requires documentation)

**Reference Loading Guidance** (if references exist): Table (Reference | Has "When to Read" | Conditions Specific | Status)
- Per `cross-progressive-loading.md` Reference File Audit section

#### Plugin Subsections

**Structure Validation**: Table (Check | Expected | Actual | Status)
- Checks: Manifest location, Component locations, Naming conventions, Path variables
- Per `type-plugin.md` Plugin Structure section

**Security Check**: Table (Check | Status | Notes)
- Checks: No hardcoded secrets, No exposed credentials, Path traversal prevention, Input validation
- Per `rules-universal.md` Security & Compliance Rules section

**Design Coherence**: Table (Principle | Status | Notes)
- Check principles from `cross-design-coherence.md`
- Include red flags if detected: god files, scattered rules, circular deps

**Progressive Loading**: Table (Level | Actual | Target | Status)
- Levels: L1-L4 per `cross-progressive-loading.md`
- Note anti-patterns if detected: metadata bloat, monolithic body, essential in L3

**Component Prompt Quality**: Table (Component | Type | Triggers Clear | Body Quality | Status)
- Components: Commands, Agents with prompt bodies
- Per `type-plugin.md` Command/Agent quality sections

**Component Summary**: Table (Component | Count | Issues)
- Components: Commands, Agents, Hooks, MCP Servers, LSP Servers
- For Hooks: note invalid matchers or missing scripts
- For MCP/LSP: note invalid JSON or path issues

#### Composite Subsections

**Audit Scope Summary**: Table (Category | Count | Details)
- Categories: Files Scanned, Components Found, Rules Extracted
- Purpose: Show audit coverage for transparency
- Rules Extracted: count behavioral, constraint, format rules found across all files

**Cross-File Review**: Includes:
- Reference Integrity: Table (Source | Target | Status)
- Terminology Consistency: Table (Concept | Terms Used | Status) - only if issues found
- Rule Layering: Table (Rule | Location | Level | Status) - per `cross-composite.md`
- Note global rules not propagated to local files if detected

**Process Logic**: Table (Check | Status | Notes)
- Checks: All scenarios covered, Main flow clear, No dead loops, No duplicate invocations
- Per `ref-checklist.md` Dimension 5.2 Process Logic section

**Rule Logic**: Table (Check | Status | Notes)
- Checks: No rule conflicts, No rule duplication, Rules properly categorized, Rule priority clear
- Per `ref-checklist.md` Dimension 5.1 Rule Logic section
- If conflicts found, note conflict type: same-file, cross-file, or principle-rule

**Rules**:
- Include only applicable subsections for the audit type
- Omit empty subsections (e.g., no Script Quality if no scripts, no Flowchart if no diagrams)
- Show check results only, NO conclusion statements
- Use ✅/⚠️/❌ for status

---

### 3. Issue Inventory

#### Issue Statistics
Table with columns: Category | Count

Categories: 🔴 Must Fix, 🟡 Should Fix, 🟢 Optional, ⚪ Filtered, **Total**

#### Issue Breakdown by Dimension (Optional)
Table with columns: Dimension | 🔴 | 🟡 | 🟢 | Total

**Dimensions**:
| Code | Dimension | Examples |
|------|-----------|----------|
| D0.1 | Cross-Component | Broken cross-refs, terminology inconsistent |
| D0.2 | Design Coherence | Rule conflicts, scattered rules, red flags |
| D0.3 | Progressive Loading | Content misplacement, L1 bloat, orphan refs |
| D0.4 | Naming & Numbering | Non-sequential, format inconsistent |
| D0.5 | Reference Integrity | Broken refs, circular deps |
| D0.6 | Diagram & Flowchart | Path mismatch, no endpoints |
| D0.7 | Language Expression | Ambiguity, unclear wording |
| D0.8 | Security & Compliance | Hardcoded secrets, path traversal |
| D5.1 | Rule Logic | Conflicts, duplication |
| D5.2 | Process Logic | Dead loops, missing scenarios |
| D-ST | Structure | Missing required fields |
| D-SZ | Size | Exceeds limits |
| D-OT | Other | Miscellaneous issues |

**Note**: Only include this breakdown when multiple dimensions have issues.

#### 3.1 Confirmed Issues

Group by severity level (🔴 → 🟡 → 🟢)

Table with columns: # | File | Line | Issue Summary | Dimension | Fix Type

**Fix Types** (priority order):
```
DELETE > MERGE > RESTRUCTURE > MODIFY > ADD
```

#### 3.2 Filtered Issues

> Issues excluded after 4-point verification. Listed for transparency.

Table with columns: # | File | Line | Issue Description | Filter Reason

**Filter Reason Categories**:
| Code | Reason | Description |
|------|--------|-------------|
| FR-SC | No Scenario | Cannot describe concrete failure |
| FR-DS | Design Choice | Valid design decision |
| FR-AI | AI Capable | AI can infer from context |
| FR-TH | Below Threshold | Below severity threshold |
| FR-OPT | Optional | Optional element not required |
| FR-TOL | Within Tolerance | Within acceptable range (e.g., ≤10% over) |

**Numbering**: Confirmed use 1,2,3... Filtered use F1,F2,F3...

**Rules**:
- Issue Statistics at the TOP of this section
- Each row ≤20 words
- This is the ONLY place filtered issues appear
- Details go to Section 4

---

### 4. Fix & Optimization Proposals

#### 4.1 Fix Proposals (🔴 Must Fix, 🟡 Should Fix)

**Grouping**: By file (use 📄 marker)

**Per issue format**:

```
#### Issue #N: [Title] — [Severity Icon] [Severity Level]

**Location**: [File:Lines]

**Problem**: [Description of what's wrong and why it matters]

**Impact**: [Severity assessment]

**Current**:
```text
[Original content]
```

**Proposal A**: [Brief description] — Recommended
```text
[Fixed content option A]
```

**Proposal B**: [Brief description]
```text
[Fixed content option B]
```
```

#### 4.2 Optimization Proposals (🟢 Optional)

Same format as 4.1, with additional field:

**Benefit**: [Why this improvement helps]

**Rules**:
- 4.1 contains only 🔴 and 🟡 issues
- 4.2 contains only 🟢 issues
- Multiple proposals per issue allowed, mark recommended with "— Recommended"
- Each issue has: Location, Problem, Impact, Current, Proposal(s)
- Code blocks ready for copy-paste
- Use `---` separator between issues

---

### 5. Conclusion

**Required subsections (in order)**:

#### Verification Statistics
Single line: `Scanned X suspected issues → Verified Y → Filtered Z`

#### Quality Judgment
Table with columns: Judgment | Criteria | Result

**Judgment criteria**:
| Judgment | Condition |
|----------|-----------|
| ✅ Pass | No 🔴 Must Fix issues |
| ⚠️ Needs Work | Has 🔴 Must Fix issues |
| ❌ Fail | Multiple severe 🔴 issues affecting core functionality |

#### Overall Verdict
One sentence summarizing: confirmed count, filtered count, overall quality, main issue areas
- For composite systems: briefly note the core design philosophy observed

#### Recommended Actions (Report Ends Here)
List ALL issues with their recommended proposal:

| # | File:Line | Issue | Recommended Action |
|---|-----------|-------|-------------------|
| 1 | `SKILL.md:45` | Missing error handling | Add error handling section |
| 2 | `rules.md:123` | Rule conflict | Modify to resolve conflict |
| ... | ... | ... | ... |

**Rules**:
- This is the ONLY conclusion location
- Verification Statistics comes FIRST
- Quality Judgment comes SECOND
- Overall Verdict is ONE sentence
- Recommended Actions table is the final output of the entire report

---

## Reference Tables

### Rating Scale

| Stars | Score | Meaning |
|-------|-------|---------|
| ⭐⭐⭐⭐⭐ | 5/5 | Excellent - No issues |
| ⭐⭐⭐⭐☆ | 4/5 | Good - Minor issues only |
| ⭐⭐⭐☆☆ | 3/5 | Average - Some issues |
| ⭐⭐☆☆☆ | 2/5 | Below Average - Significant issues |
| ⭐☆☆☆☆ | 1/5 | Poor - Major issues |

### Severity Levels

| Level | Icon | Criteria |
|-------|------|----------|
| Must Fix | 🔴 | Function broken, or ≥60% executors fail |
| Should Fix | 🟡 | Quality impact, or ≥40% suboptimal results |
| Optional | 🟢 | Enhances experience, not required |
| Filtered | ⚪ | Did not pass 4-point verification |

---

## Output Rules

### File Creation
- Report >300 lines → create separate file
- Naming: `audit-{target}-{date}.md`

### No Issues Case
When no issues found:
- Section 3: Statistics all 0, show "✅ No issues found" and "✅ No filtered issues"
- Section 4: Show "✅ No fixes or optimizations needed"
- Section 5: Quality Judgment is "✅ Pass", Verdict states "no issues", Recommended Actions shows "无需操作 - 该技能符合所有审计标准。" (report ends here)
