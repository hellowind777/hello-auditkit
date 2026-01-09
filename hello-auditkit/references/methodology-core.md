# Audit Methodology Core

> **Dual Application**: The principles in this document serve TWO purposes:
> 1. **As audit standards**: When auditing other skills, check if they follow these principles
> 2. **As self-compliance**: This audit system itself follows these principles
>
> When auditing, verify that the audited content adheres to: Occam's Razor, AI Capability awareness, Fix Priority (DELETE > ADD), and necessity-based additions.

## Table of Contents

- [4-Point Core Verification](#4-point-core-verification)
- [Occam's Razor: Correct Application](#occams-razor-correct-application)
- [Conciseness Principle](#conciseness-principle)
- [Freedom Level Matching](#freedom-level-matching)
- [AI Capability Model](#ai-capability-model)
- [Fix Priority Hierarchy](#fix-priority-hierarchy)
- [Necessity Threshold](#necessity-threshold)

---

## 4-Point Core Verification

**Before marking ANY issue, it MUST pass all 4 checks:**

### Check 1: Concrete Scenario Test

| Question | Pass Criteria |
|----------|---------------|
| Can you construct a specific scenario where this causes clear negative consequences? | Must describe complete execution steps and failure point |
| If NO → Not an issue, discard | |
| If YES → Continue to Check 2 | |

### Check 2: Design Scope Verification

| Question | Pass Criteria |
|----------|---------------|
| Is this scenario within the design scope? | Exclude extreme edge cases, theoretical possibilities |
| If NO → Not an issue, discard | |
| If YES → Continue to Check 2b | |

**CRITICAL**: Before applying any audit rule, first understand the audited content's:
- **Core purpose**: What is it designed to do?
- **Design principles**: What trade-offs did the author make?
- **Domain characteristics**: Does the domain require special considerations?

Only then judge whether the audit rule applies to this specific content.

### Check 2b: Functional Capability Audit

**CRITICAL PREREQUISITE**: Before evaluating functional capability, the auditor MUST first understand the target domain. For domain-specific skills, acquire domain knowledge (via WebSearch, references, or user input) before assessment.

**For any content that generates outputs or performs tasks, evaluate whether it truly has the capability to achieve its stated purpose:**

| Question | Potential Issue If |
|----------|-------------------|
| Does it understand the domain's core concepts? | Uses fixed templates without domain understanding |
| Can it handle complex/varied scenarios? | Only works for simple/fixed cases |
| Are outputs dynamically generated based on input? | Hardcoded values, fixed structures, preset results |
| Does it have necessary knowledge to make decisions? | Missing knowledge base or decision logic |
| Can it adapt to different requirements? | One-size-fits-all approach |

**Universal Anti-Patterns (apply to any content type):**

| Anti-Pattern | Indicator | Impact |
|--------------|-----------|--------|
| Fixed template | Same output structure regardless of input | Cannot handle varied scenarios |
| Hardcoded values | Preset numbers, positions, or results | Incorrect for different inputs |
| Missing calculation/logic | Results preset instead of computed | Fundamentally wrong outputs |
| Oversimplified model | Linear/simple logic for complex domain | Cannot represent real complexity |
| Lack of domain knowledge | No understanding of domain concepts | Outputs lack accuracy |

**Audit approach**:
1. First understand what the content claims to do (from description/purpose)
2. Then evaluate whether its implementation can actually achieve that
3. If gap exists between claimed capability and actual capability → Flag as functional deficiency

### Check 3: Design Intent Judgment

| Question | Pass Criteria |
|----------|---------------|
| Is this a design flaw or a design choice? | Can you find a reasonable design rationale? |
| If design choice (intentional) → Not an issue, discard | |
| If design flaw (unintentional error) → Continue to Check 4 | |
| **Note**: Missing necessary constraints is NOT a design choice | If ≥30% would misunderstand, still flag |

### Check 4: Negative Consequence Assessment

| Issue Type | Threshold |
|------------|-----------|
| Fatal | Execution completely fails (cannot continue) |
| Severe | ≥60% of executors make serious errors |
| Semantic Ambiguity | ≥3 reasonable but conflicting interpretations |
| Expression Standards | ≥40% misunderstand OR reading time +40% |
| Structure | Content scattered in ≥4 locations OR change requires ≥4 syncs |
| Robustness | ≥20% failure rate in common scenarios |
| Optimization | ≥30% improvement AND <10% cost |

If unclear or below threshold → Discard
If clear and meets threshold → Mark as issue

### Verification Transparency

- Record which checks passed/failed for each suspected issue
- If >80% of a category discarded → reconsider scan criteria
- Final output must include: "Scanned X, verified Y, discarded Z"

---

## Occam's Razor: Correct Application

### Common Misunderstanding

❌ **Wrong**: "Fewer is always better" (minimalism for its own sake)
❌ **Wrong**: "Add rules to prevent all possible issues" (defensive over-engineering)

✅ **Correct**: "Do not multiply entities **beyond necessity**" — the key is judging NECESSITY

### The Problem: Addition Bias

Most audit systems suffer from **addition bias**:
- "Add a rule for X"
- "Add a constraint to prevent Y"
- "Add an example showing Z"

This leads to **bloated, over-constrained systems**.

### The Correct Approach

**Fix the structure, not the symptoms.**

Fix Priority (highest to lowest):
```
1. DELETE    - Remove unnecessary content
2. MERGE     - Combine redundant elements
3. RESTRUCTURE - Reorganize for clarity
4. MODIFY    - Change existing content
5. ADD       - Only if absolutely necessary (LAST RESORT)
```

---

## Conciseness Principle

> "Context window is a shared resource."

### Core Concept

Context window is shared among: system prompts, conversation history, skill metadata, user requests, and tool outputs.

### Self-Check Questions

Before adding ANY content, ask:
1. "Does AI really need this explanation?"
2. "Is this worth its token cost?"
3. "Can a concise example replace lengthy text?"

### Information Placement

| Rule | Requirement | Severity |
|------|-------------|----------|
| Single source of truth | Info exists in ONE place only | Warning |
| No duplication | Same content not in body AND references | Warning |
| Prefer examples | Concise examples over lengthy explanations | Info |
| Remove AI-known content | Don't explain what AI already knows | Warning |

### Applies To

- **Prompts**: No over-explanation of common concepts
- **Memory files**: Concise, actionable instructions
- **Skills**: Body ≤500 lines, use references for details
- **Plugins**: Component descriptions brief, details in bodies
- **Commands/Agents**: Descriptions include triggers, not implementation

---

## Freedom Level Matching

### Core Concept

Match constraint specificity to task fragility and variability.

### Freedom Levels

| Level | When to Apply | Implementation | Example |
|-------|---------------|----------------|---------|
| **High** | Multiple valid approaches, context-dependent | Text instructions | Code style suggestions |
| **Medium** | Preferred patterns exist, some variation OK | Pseudo-code, parameterized | API call templates |
| **Low** | Fragile operations, consistency critical | Specific scripts, few params | PDF form filling |

### Analogy

AI explores a path:
- **Narrow cliff bridge** → Needs specific guardrails (low freedom)
- **Open field** → Multiple routes acceptable (high freedom)

### Audit Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Fragile ops with high freedom | Should use specific scripts | Severe |
| Simple tasks over-constrained | Should allow flexibility | Warning |
| Missing freedom guidance | When to follow strictly vs adjust | Info |

### Applies To

- **Prompts**: Match verbosity constraints to task complexity
- **Skills**: Scripts for fragile ops, guidelines for flexible tasks
- **Plugins/Hooks**: Specific matchers for critical flows
- **Commands**: Structured output for data extraction, flexible for creative tasks

---

## AI Capability Model

### Default Assumption

AI executors have strong contextual understanding and can infer meaning from context and common sense.

### AI Trust Levels

| Trust Level | When to Apply | Rule Density |
|-------------|---------------|--------------|
| **High trust** | Standard coding tasks | Minimal rules |
| **Medium trust** | Domain-specific tasks | Moderate rules |
| **Low trust** | Safety-critical tasks | More explicit rules |

**Default**: High trust. Only reduce trust with justification.

### Balance Principle

1. **Identify issues first**: Assume issue exists, then verify if AI capability exempts it
2. **Burden of proof**: To exempt, must prove "AI can infer correct understanding"
3. **Necessity threshold**: If removing constraint causes ≥30% to misunderstand → Necessary

---

## Fix Priority Hierarchy

### Priority 1: DELETE (Highest)

**Question**: Can this issue be fixed by REMOVING something?

| Scenario | Fix |
|----------|-----|
| Redundant rule exists | Delete the redundant copy |
| Unnecessary constraint | Remove the constraint |
| Over-explanation | Delete the explanation |
| Outdated content | Remove entirely |
| Duplicate information | Keep one, delete others |

### Priority 2: MERGE

**Question**: Can this issue be fixed by COMBINING elements?

| Scenario | Fix |
|----------|-----|
| Scattered related rules | Merge into one section |
| Multiple similar files | Combine into one file |
| Fragmented documentation | Consolidate |
| Overlapping responsibilities | Merge components |

### Priority 3: RESTRUCTURE

**Question**: Can this issue be fixed by REORGANIZING?

| Scenario | Fix |
|----------|-----|
| Confusing organization | Restructure hierarchy |
| Wrong level of abstraction | Move content to correct level |
| Poor separation of concerns | Reorganize by responsibility |
| Inverted disclosure order | Reorder sections |

### Priority 4: MODIFY

**Question**: Can this issue be fixed by CHANGING existing content?

| Scenario | Fix |
|----------|-----|
| Unclear wording | Rewrite for clarity |
| Incorrect information | Correct the error |
| Inconsistent naming | Rename to be consistent |
| Wrong constraint level | Adjust (MUST→SHOULD) |

### Priority 5: ADD (Last Resort)

**Before adding ANYTHING, verify ALL:**
- [ ] AI cannot infer from context?
- [ ] Cannot fix by removing conflicting content?
- [ ] Cannot fix by restructuring?
- [ ] Causes ≥30% failure rate without it?
- [ ] Not already implied by existing content?

**If ALL checked → Addition may be justified**

### When ADD is Necessary (Exceptions)

Despite the "ADD as last resort" principle, the following are considered **necessary additions**:

| Category | Examples | Why Necessary |
|----------|----------|---------------|
| Official standards | API parameters, protocol specs, format definitions from official docs | Cannot be inferred, must be exact |
| Safety-critical rules | Security constraints, data validation, access control | Risk of harm if omitted |
| Necessary prohibition rules | "Do NOT" lists for scope control, feature creep prevention | Prevents unintended behavior |
| Necessary clarifying examples | When rule is ambiguous without example | Reduces misinterpretation |

**Key principle**: "Necessary" means removal would cause ≥30% misunderstanding or functional failure.

**Applies equally to auditing**: When auditing other skills, do NOT flag necessary additions as violations of Occam's Razor.

---

## Necessity Threshold

### Quantified Thresholds

| Scenario | Necessary? | Reasoning |
|----------|------------|-----------|
| AI fails >30% without constraint | Yes | Clear necessity |
| AI fails 10-30% without constraint | Maybe | Weigh cost/benefit |
| AI fails <10% without constraint | No | AI can handle it |
| Content AI can infer from context | No | Trust AI capability |
| Edge case <5% occurrence | No | Handle as exception |

### Size Thresholds

**SKILL.md body** (official requirement):

| Range | Status | Action |
|-------|--------|--------|
| ≤500 lines | Ideal | No action |
| 500-550 (≤10% over) | Acceptable | **NOT an issue** |
| 550-625 (10-25% over) | Review | Info only |
| >625 lines | Optimize | Warning |

**Reference files**: No official limit. Evaluate based on content nature (see `rules-universal.md`).

### Anti-Patterns to Avoid

| Anti-Pattern | Why Wrong | Better |
|--------------|-----------|--------|
| "Add a Note" | Hides real issue | Move important info where visible |
| "Add an Example" | Compensates for bad writing | Rewrite rule clearly |
| "Add a Constraint" | Symptoms over cause | Fix root cause |
| "Add Documentation" | May be unnecessary | Question if behavior needed |
| "Add Cross-Reference" | Creates coupling | MERGE related content |

---

## Summary

| Principle | Key Point |
|-----------|-----------|
| **4-Point Check** | All issues must pass 4 verification steps |
| **Occam's Razor** | "If necessary" is the key, not "fewer is better" |
| **AI Trust** | AI can infer most things from context |
| **Fix Hierarchy** | DELETE > MERGE > RESTRUCTURE > MODIFY > ADD |
| **Addition Test** | All 5 criteria must pass before adding |
| **Size Tolerance** | ≤10% over is NOT an issue |
