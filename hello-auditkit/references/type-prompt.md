# Prompt Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Execution Required**: Execute each check table below. Output evidence for each category.

## Table of Contents

- [Overview](#overview)
- [Structure Validation](#structure-validation)
- [Content Quality](#content-quality)
- [LLM Prompting Best Practices](#llm-prompting-best-practices)
- [Common Issues](#common-issues)

---

## Overview

**Applies to**: Standalone LLM prompts, system prompts, instruction text

**Key focus areas**:
- Verbosity constraints
- Scope boundaries
- Output format specification
- Ambiguity handling

---

## Structure Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Verbosity constraints | Explicit length limits specified | Warning |
| Scope boundaries | Clear "do not" constraints | Warning |
| Ambiguity handling | Instructions for unclear cases | Info |
| Output format | Specified structure/format | Warning |
| Grounding | "Based on context" hedging for uncertain claims | Info |

---

## Content Quality

### Good Prompt Patterns

```markdown
# Explicit constraints
Respond in ≤3 sentences.

# Scope limits
Only address the specific question asked. No extra features.

# Ambiguity handling
If unclear, ask 1-2 clarifying questions.

# Output format
Return as JSON with fields: status, result, errors.

# Grounding
Based on the provided context, [conclusion].
```

### Bad Prompt Patterns

| Pattern | Problem |
|---------|---------|
| "Do it well" | Vague, non-actionable |
| No length constraints | Unbounded verbosity |
| No scope boundaries | Feature creep |
| Absolute claims | No grounding |
| "Be helpful" | Too generic |

---

## LLM Prompting Best Practices

### Core Principles (GPT-5/Claude)

1. **Explicit over implicit**: Articulate preferences clearly
2. **Constraint-driven**: Use explicit scope, verbosity, format constraints
3. **Verification-oriented**: Add self-check steps for high-risk outputs
4. **Minimal interpretation**: "If ambiguous, choose simplest valid interpretation"

### Verbosity Control

| Context | Constraint |
|---------|------------|
| Simple yes/no | ≤2 sentences |
| Default responses | 3-6 sentences or ≤5 bullets |
| Complex tasks | 1 overview + ≤5 tagged bullets |
| Long-form content | Explicit word/section limits |

### Scope Discipline

Prevent feature creep:
- "Implement EXACTLY and ONLY what requested"
- "No extra features, no added components"
- Forbid inventing elements unless requested
- Clear boundaries: what IS and IS NOT in scope

### Long-Context Handling (>10k tokens)

1. Produce internal outline of relevant sections first
2. Re-state user constraints before answering
3. Anchor claims to specific sections with quotes
4. Break into phases if necessary

### Ambiguity & Hallucination Prevention

| Strategy | Implementation |
|----------|----------------|
| Clarification | Ask 1-3 questions OR present 2-3 interpretations |
| Hedging | "Based on the provided context..." |
| Uncertainty | Never fabricate exact figures when uncertain |
| Missing data | Set missing fields to null rather than guessing |
| Grounding | Reference specific sections/quotes |

### Tool Usage Guidelines

| Guideline | Severity |
|-----------|----------|
| Prefer tools over internal knowledge for fresh data | Info |
| Parallelize independent reads | Info |
| After writes, restate: what changed, where, validation | Warning |
| Explicit tool selection criteria | Info |

### Agentic Updates

- Brief updates (1-2 sentences) only at major phases
- Avoid narrating routine tool calls
- Each update must include concrete outcomes
- No "thinking out loud" unless debugging

### Structured Extraction

| Check | Requirement | Severity |
|-------|-------------|----------|
| Schema provided | Always provide JSON shape | Warning |
| Field distinction | Required vs optional marked | Warning |
| Null handling | Missing → null, not guessed | Warning |
| Array bounds | Min/max items specified | Info |

### Freedom Level Matching

| Task Type | Freedom | Constraint Style |
|-----------|---------|------------------|
| Creative/flexible | High | Guidelines only |
| Code generation | Medium | Patterns + flexibility |
| Data extraction | Low | Strict schema |
| Safety-critical | Very Low | Explicit scripts |

---

## Common Issues

### Should Flag

| Issue | Severity |
|-------|----------|
| Contradictory instructions | Fatal |
| Impossible constraints | Fatal |
| Missing critical context | Fatal |
| No verbosity constraints for open-ended tasks | Severe |
| No scope boundaries | Severe |
| Ambiguous output format for structured tasks | Severe |
| No error handling instructions | Severe |
| Vague instructions ("do it well") | Warning |
| Missing examples for complex tasks | Warning |
| No hedging guidance for uncertain cases | Warning |
| Overly long without structure | Warning |

### Should NOT Flag

| Pattern | Reason |
|---------|--------|
| Simple prompts without constraints | Not needed for simple tasks |
| Style preferences | Design choice |
| Reasonable interpretation choices | Valid |
| Missing optional elements | Optional |

---

## Audit Checklist

### Fatal
- [ ] No contradictory instructions
- [ ] No impossible constraints
- [ ] Critical context present

### Severe
- [ ] Verbosity constraints specified
- [ ] Scope boundaries defined
- [ ] Output format clear
- [ ] Error handling addressed

### Warnings
- [ ] Instructions are specific, not vague
- [ ] Examples provided for complex tasks
- [ ] Hedging guidance for uncertain cases
- [ ] Well-structured if long

### Info
- [ ] Could benefit from more examples
- [ ] Could add self-check steps
- [ ] Could specify output more precisely
